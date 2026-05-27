from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
import os

app = FastAPI(title="Superhéroes API")

# --- 1. CONFIGURACIÓN DE CORS ---
# Esto permite que nuestro frontend en React (puerto 5173) se comunique con la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción se pone la URL exacta del front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. CONEXIÓN A MONGODB ---
# Usamos la variable de entorno que definimos en el docker-compose.yml
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/superheroes_db")
client = AsyncIOMotorClient(MONGO_URL)
db = client.superheroes_db
collection = db.superheroes

# --- 3. MODELOS DE DATOS (PYDANTIC) ---
# Validamos que los datos cumplan con los requerimientos de la práctica
class HeroeBase(BaseModel):
    nombre: str
    nombre_real: Optional[str] = None
    anio_aparicion: int
    casa: str
    biografia: str
    equipamiento: Optional[List[str]] = []
    imagenes: List[str]

class HeroeResponse(HeroeBase):
    id: str # Mongo usa "_id" (ObjectId), lo mapeamos a un string "id" para React

# --- 4. RUTAS CRUD ---

# GET: Obtener todos los superhéroes (o filtrar por casa)
@app.get("/api/heroes", response_model=List[HeroeResponse])
async def get_heroes(casa: Optional[str] = None):
    query = {}
    if casa:
        # Búsqueda insensible a mayúsculas/minúsculas para "Marvel" o "DC"
        query["casa"] = {"$regex": f"^{casa}$", "$options": "i"} 
        
    heroes = []
    cursor = collection.find(query)
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        heroes.append(doc)
    return heroes

# GET: Obtener un superhéroe por ID (Para la vista de detalle)
@app.get("/api/heroes/{id}", response_model=HeroeResponse)
async def get_heroe(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
        
    doc = await collection.find_one({"_id": ObjectId(id)})
    if doc:
        doc["id"] = str(doc["_id"])
        return doc
    raise HTTPException(status_code=404, detail="Superhéroe no encontrado")

# POST: Crear un nuevo superhéroe
@app.post("/api/heroes", response_model=HeroeResponse)
async def create_heroe(heroe: HeroeBase):
    # Convertimos el modelo a diccionario
    heroe_dict = heroe.model_dump()
    nuevo_doc = await collection.insert_one(heroe_dict)
    
    # Lo buscamos para devolverlo tal cual quedó en la base
    doc_creado = await collection.find_one({"_id": nuevo_doc.inserted_id})
    doc_creado["id"] = str(doc_creado["_id"])
    return doc_creado

# PUT: Actualizar un superhéroe
@app.put("/api/heroes/{id}", response_model=HeroeResponse)
async def update_heroe(id: str, heroe: HeroeBase):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
        
    resultado = await collection.update_one(
        {"_id": ObjectId(id)}, {"$set": heroe.model_dump()}
    )
    
    if resultado.modified_count == 1 or resultado.matched_count == 1:
        doc_actualizado = await collection.find_one({"_id": ObjectId(id)})
        doc_actualizado["id"] = str(doc_actualizado["_id"])
        return doc_actualizado
        
    raise HTTPException(status_code=404, detail="Superhéroe no encontrado")

# DELETE: Eliminar un superhéroe
@app.delete("/api/heroes/{id}")
async def delete_heroe(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
        
    resultado = await collection.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 1:
        return {"mensaje": "Superhéroe eliminado con éxito"}
        
    raise HTTPException(status_code=404, detail="Superhéroe no encontrado")