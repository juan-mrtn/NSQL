from fastapi import APIRouter, HTTPException, Body, status
from typing import List
from models import SuperheroCreate, SuperheroUpdate, SuperheroInDB
from database import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/", response_description="Add new superhero", response_model=SuperheroInDB, status_code=status.HTTP_201_CREATED)
async def create_superhero(superhero: SuperheroCreate = Body(...)):
    db = get_db()
    new_superhero = await db["superheroes"].insert_one(superhero.model_dump())
    created_superhero = await db["superheroes"].find_one({"_id": new_superhero.inserted_id})
    return created_superhero

@router.get("/", response_description="List all superheroes", response_model=List[SuperheroInDB])
async def list_superheroes():
    db = get_db()
    superheroes = await db["superheroes"].find().to_list(1000)
    return superheroes

@router.get("/{id}", response_description="Get a single superhero", response_model=SuperheroInDB)
async def show_superhero(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    superhero = await db["superheroes"].find_one({"_id": ObjectId(id)})
    if superhero is not None:
        return superhero
    raise HTTPException(status_code=404, detail="Superhero not found")

@router.put("/{id}", response_description="Update a superhero", response_model=SuperheroInDB)
async def update_superhero(id: str, superhero: SuperheroUpdate = Body(...)):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    superhero_dict = {k: v for k, v in superhero.model_dump().items() if v is not None}
    
    if len(superhero_dict) >= 1:
        update_result = await db["superheroes"].update_one(
            {"_id": ObjectId(id)}, {"$set": superhero_dict}
        )
        if update_result.modified_count == 1:
            if (
                updated_superhero := await db["superheroes"].find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_superhero

    if (existing_superhero := await db["superheroes"].find_one({"_id": ObjectId(id)})) is not None:
        return existing_superhero

    raise HTTPException(status_code=404, detail="Superhero not found")

@router.delete("/{id}", response_description="Delete a superhero")
async def delete_superhero(id: str):
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    delete_result = await db["superheroes"].delete_one({"_id": ObjectId(id)})
    
    if delete_result.deleted_count == 1:
        return {"message": "Superhero deleted successfully"}

    raise HTTPException(status_code=404, detail="Superhero not found")
