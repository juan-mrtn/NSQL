# ✈ Airport Explorer – TP #6 NSQL

A full-stack application for exploring airports using **MongoDB**, **Redis GEO**, **Redis Popularity**, **FastAPI**, and **Leaflet.js**, orchestrated with **Docker Compose**.

---

## Project Structure

```
airports-project/
├── docker-compose.yml
├── data/
│   └── data_trasport.json        # Airport dataset
├── backend/
│   ├── Dockerfile
│   ├── main.py                   # FastAPI app + seeding logic
│   └── requirements.txt
└── frontend/
    ├── index.html                # Leaflet.js map UI
    └── nginx.conf                # Nginx reverse proxy config
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- Git (optional).

---

## Quick Start

### 1. Clone / extract the project

```bash
cd airports-project
```

### 2. Start all services

```bash
docker-compose up --build
```

Docker will:
- Pull `mongo:7`, `redis:7-alpine`, `nginx:alpine` images.
- Build the FastAPI backend image.
- On first run, the backend automatically seeds MongoDB and Redis from `data_trasport.json`.

### 3. Open the application

| Service  | URL                          |
|----------|------------------------------|
| Frontend | http://localhost:3000         |
| Backend API | http://localhost:8000      |
| API Docs | http://localhost:8000/docs    |

---

## API Reference

### CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/airports` | List all airports |
| `POST` | `/airports` | Create airport (MongoDB + Redis GEO) |
| `GET`  | `/airports/{iata}` | Get airport details + **+1 popularity** |
| `PUT`  | `/airports/{iata}` | Update airport |
| `DELETE` | `/airports/{iata}` | Delete from MongoDB + Redis GEO + Redis Popularity |

### Geospatial & Popularity

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/airports/nearby?lat=&lng=&radius_km=` | Nearby airports via Redis GEOSEARCH |
| `GET`  | `/airports/popular?limit=10` | Top airports by visit count (ZREVRANGE) |

---

## Manual Data Import (alternative)

If you prefer to import via `mongoimport`:

```bash
# Copy file into running mongo container
docker cp data/data_trasport.json mongo-airports:/tmp/data_trasport.json

# Import (the file uses newline-delimited JSON objects)
docker exec -it mongo-airports mongoimport \
  --db airport_db \
  --collection airports \
  --drop \
  --file /tmp/data_trasport.json
```

---

## Stopping the project

```bash
docker-compose down          # stop containers, keep data volumes
docker-compose down -v       # stop + delete volumes (full reset)
```

---

## Architecture Notes

- **MongoDB** stores all airport documents with a unique index on `iata_faa`.
- **redis-geo** holds `airports-geo` (a Redis GEO Sorted Set). Used by `GEOSEARCH` for nearby queries.
- **redis-pop** holds `airport_popularity` (a ZSET scored by visit count). TTL resets to 86 400 s (1 day) on every read or increment.
- **Backend seeding** runs on startup via FastAPI's `lifespan` hook; it is idempotent — re-running when data already exists is a no-op.
- **Frontend** proxies all `/api/*` calls through Nginx to the backend, avoiding CORS issues.
