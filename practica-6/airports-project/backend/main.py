"""
Airport API – FastAPI + Motor (MongoDB async) + Redis (geo & popularity)
"""

import asyncio
import json
import logging
import os
import re
from contextlib import asynccontextmanager
from typing import List, Optional

import redis.asyncio as aioredis
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment / Config
# ---------------------------------------------------------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "airport_db")
REDIS_GEO_HOST = os.getenv("REDIS_GEO_HOST", "localhost")
REDIS_GEO_PORT = int(os.getenv("REDIS_GEO_PORT", 6379))
REDIS_POP_HOST = os.getenv("REDIS_POP_HOST", "localhost")
REDIS_POP_PORT = int(os.getenv("REDIS_POP_PORT", 6380))
DATA_FILE = os.getenv("DATA_FILE", "/app/data/data_trasport.json")

GEO_KEY = "airports-geo"
POP_KEY = "airport_popularity"
POP_TTL = 86400  # 1 day in seconds

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class AirportBase(BaseModel):
    name: str
    city: str
    iata_faa: str
    icao: Optional[str] = None
    lat: float
    lng: float
    alt: Optional[float] = None
    tz: Optional[str] = None


class AirportCreate(AirportBase):
    pass


class AirportUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    icao: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    alt: Optional[float] = None
    tz: Optional[str] = None


class AirportOut(AirportBase):
    id: Optional[str] = Field(None, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def doc_to_out(doc: dict) -> dict:
    """Convert a MongoDB document to a serialisable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


def parse_newline_json(filepath: str) -> List[dict]:
    """
    The data file contains newline-separated JSON objects (not a JSON array).
    Parse them all and return a list of dicts.
    """
    records: List[dict] = []
    raw = open(filepath, "r", encoding="utf-8").read()

    # Split on object boundaries: find each {...} block
    # The file has objects separated by whitespace (no commas, no array wrapper)
    decoder = json.JSONDecoder()
    pos = 0
    raw = raw.strip()
    while pos < len(raw):
        # skip whitespace
        while pos < len(raw) and raw[pos] in " \t\r\n":
            pos += 1
        if pos >= len(raw):
            break
        try:
            obj, end_pos = decoder.raw_decode(raw, pos)
            records.append(obj)
            pos = end_pos
        except json.JSONDecodeError:
            pos += 1  # skip bad char and try again

    return records


# ---------------------------------------------------------------------------
# Seeding
# ---------------------------------------------------------------------------

async def seed_data(db, redis_geo, redis_pop):
    """Load airports from the JSON file into MongoDB and Redis on first run."""
    if not os.path.exists(DATA_FILE):
        log.warning("Data file not found: %s – skipping seed.", DATA_FILE)
        return

    count = await db.airports.count_documents({})
    if count > 0:
        log.info("MongoDB already has %d airports – skipping seed.", count)
        # Still make sure Redis GEO is populated (in case Redis was reset)
        geo_count = await redis_geo.zcard(GEO_KEY)
        if geo_count == 0:
            log.info("Redis GEO is empty – re-seeding geospatial data …")
            await _seed_redis_geo(db, redis_geo)
        return

    log.info("Seeding data from %s …", DATA_FILE)
    airports = parse_newline_json(DATA_FILE)
    log.info("Parsed %d airports from file.", len(airports))

    # Deduplicate by iata_faa: keep first occurrence, skip duplicates
    seen_iata = set()
    deduplicated = []
    for airport in airports:
        iata = airport.get("iata_faa")
        if not iata:
            # If no IATA code, ensure key is removed for sparse index and add it
            if "iata_faa" in airport:
                del airport["iata_faa"]
            deduplicated.append(airport)
        elif iata not in seen_iata:
            seen_iata.add(iata)
            deduplicated.append(airport)
        else:
            log.debug("Skipping duplicate airport with IATA code: %s", iata)
    
    log.info("After deduplication: %d unique airports (removed %d duplicates).", 
             len(deduplicated), len(airports) - len(deduplicated))

    # ---- MongoDB ----
    result = await db.airports.insert_many(deduplicated)
    log.info("Inserted %d airports into MongoDB.", len(result.inserted_ids))

    # ---- Redis GEO ----
    await _seed_redis_geo(db, redis_geo)

    # ---- Redis Popularity – empty ZSET ----
    # We create it with a dummy member then remove it so the key exists.
    # (Redis doesn't store empty ZSETs; we just leave it to be created on
    #  first access instead – this is fine and idiomatic.)
    log.info("Seed complete.")


async def _seed_redis_geo(db, redis_geo):
    """Populate Redis GEO from MongoDB documents."""
    pipeline = redis_geo.pipeline()
    async for doc in db.airports.find(
        {"lat": {"$exists": True}, "lng": {"$exists": True}},
        {"iata_faa": 1, "lat": 1, "lng": 1}
    ):
        iata = doc.get("iata_faa")
        lat = doc.get("lat")
        lng = doc.get("lng")
        if iata and lat is not None and lng is not None:
            pipeline.geoadd(GEO_KEY, [lng, lat, iata])
    await pipeline.execute()
    count = await redis_geo.zcard(GEO_KEY)
    log.info("Redis GEO populated with %d airports.", count)


# ---------------------------------------------------------------------------
# App lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    log.info("Connecting to MongoDB …")
    app.state.mongo_client = AsyncIOMotorClient(MONGO_URL)
    app.state.db = app.state.mongo_client[MONGO_DB]

    # Create unique index on iata_faa (sparse to allow multiple null values)
    try:
        await app.state.db.airports.create_index("iata_faa", unique=True, sparse=True)
    except OperationFailure as e:
        log.warning("Index conflict detected for 'iata_faa'. Recreating index... (%s)", e)
        await app.state.db.airports.drop_index("iata_faa_1")
        await app.state.db.airports.create_index("iata_faa", unique=True, sparse=True)

    log.info("Connecting to Redis GEO …")
    app.state.redis_geo = aioredis.Redis(
        host=REDIS_GEO_HOST, port=REDIS_GEO_PORT, decode_responses=True
    )

    log.info("Connecting to Redis Popularity …")
    app.state.redis_pop = aioredis.Redis(
        host=REDIS_POP_HOST, port=REDIS_POP_PORT, decode_responses=True
    )

    # Seed on first launch
    await seed_data(app.state.db, app.state.redis_geo, app.state.redis_pop)

    yield

    # --- Shutdown ---
    app.state.mongo_client.close()
    await app.state.redis_geo.aclose()
    await app.state.redis_pop.aclose()
    log.info("Connections closed.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Airport API",
    description="REST API for airports using MongoDB + Redis GEO + Redis Popularity",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Shortcuts
def db():
    return app.state.db

def redis_geo():
    return app.state.redis_geo

def redis_pop():
    return app.state.redis_pop


# ---------------------------------------------------------------------------
# CRUD Endpoints
# ---------------------------------------------------------------------------

@app.post("/airports", response_model=dict, status_code=201)
async def create_airport(airport: AirportCreate):
    """Create a new airport in MongoDB and Redis GEO."""
    data = airport.model_dump()

    # Check for duplicate
    existing = await db().airports.find_one({"iata_faa": airport.iata_faa})
    if existing:
        raise HTTPException(status_code=409, detail=f"Airport {airport.iata_faa} already exists.")

    result = await db().airports.insert_one(data)
    data["_id"] = str(result.inserted_id)

    # Add to Redis GEO
    await redis_geo().geoadd(GEO_KEY, [airport.lng, airport.lat, airport.iata_faa])

    return data


@app.get("/airports/popular", response_model=list)
async def get_popular_airports(limit: int = Query(10, ge=1, le=100)):
    """
    Return the most visited airports (highest popularity score).
    Resets TTL on each call to keep the window rolling.
    """
    # ZREVRANGE: highest score first
    results = await redis_pop().zrevrange(POP_KEY, 0, limit - 1, withscores=True)

    # Refresh TTL on every read
    if results:
        await redis_pop().expire(POP_KEY, POP_TTL)

    output = []
    for iata, score in results:
        doc = await db().airports.find_one({"iata_faa": iata}, {"_id": 0})
        if doc:
            doc["visits"] = int(score)
            output.append(doc)
        else:
            output.append({"iata_faa": iata, "visits": int(score)})

    return output


@app.get("/airports/nearby", response_model=list)
async def get_nearby_airports(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius: float = Query(100, description="Search radius in kilometres"),
):
    """Return airports within radius_km of (lat, lng) using Redis GEORADIUS."""
    results = await redis_geo().georadius(
        GEO_KEY,
        longitude=lng,
        latitude=lat,
        radius=radius,
        unit="km",
        withcoord=True,
        withdist=True,
        sort="ASC",
        count=50,
    )

    output = []
    for item in results:
        # item = (member, distance, (lng, lat))
        iata, distance, (r_lng, r_lat) = item
        doc = await db().airports.find_one({"iata_faa": iata}, {"_id": 0})
        if doc:
            doc["distance_km"] = round(distance, 2)
            output.append(doc)

    return output


@app.get("/airports", response_model=list)
async def list_airports(skip: int = 0, limit: int = Query(5000, le=10000)):
    """Return all airports stored in MongoDB."""
    cursor = db().airports.find({}, {"_id": 0}).skip(skip).limit(limit)
    return [doc async for doc in cursor]


@app.get("/airports/{iata_code}", response_model=dict)
async def get_airport(iata_code: str):
    """
    Retrieve a specific airport by IATA code.
    Increments its popularity counter in Redis and refreshes the TTL.
    """
    iata_code = iata_code.upper()
    doc = await db().airports.find_one({"iata_faa": iata_code}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Airport '{iata_code}' not found.")

    # Increment popularity +1
    await redis_pop().zincrby(POP_KEY, 1, iata_code)
    # Refresh TTL (rolling 1-day window)
    await redis_pop().expire(POP_KEY, POP_TTL)

    return doc


@app.put("/airports/{iata_code}", response_model=dict)
async def update_airport(iata_code: str, payload: AirportUpdate):
    """Update an airport's data in MongoDB (and Redis GEO if coordinates changed)."""
    iata_code = iata_code.upper()
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update.")

    result = await db().airports.find_one_and_update(
        {"iata_faa": iata_code},
        {"$set": update_data},
        return_document=True,
        projection={"_id": 0},
    )
    if not result:
        raise HTTPException(status_code=404, detail=f"Airport '{iata_code}' not found.")

    # If coordinates changed, update Redis GEO
    if "lat" in update_data or "lng" in update_data:
        await redis_geo().geoadd(GEO_KEY, [result["lng"], result["lat"], iata_code])

    return result


@app.delete("/airports/{iata_code}", status_code=200)
async def delete_airport(iata_code: str):
    """Delete an airport from MongoDB, Redis GEO, and Redis Popularity."""
    iata_code = iata_code.upper()
    result = await db().airports.delete_one({"iata_faa": iata_code})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Airport '{iata_code}' not found.")

    # Remove from Redis GEO
    await redis_geo().zrem(GEO_KEY, iata_code)
    # Remove from Redis Popularity
    await redis_pop().zrem(POP_KEY, iata_code)

    return {"message": f"Airport '{iata_code}' deleted successfully."}


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)
