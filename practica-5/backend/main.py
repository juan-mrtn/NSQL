from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router as superhero_router
from seeder import seed_data
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed data on startup
    await seed_data()
    yield
    # Cleanup on shutdown

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173", # Vite default port
    "http://127.0.0.1:5173",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For simplicity in dev, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(superhero_router, prefix="/api/superheroes", tags=["superheroes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Superheroes API"}
