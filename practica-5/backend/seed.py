import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def seed_data():
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    db = client.superheroes_db
    collection = db.superheroes

    # Limpiamos lo que haya para no duplicar
    await collection.delete_many({})

    heroes = [
        # MARVEL (10 mínimos)
        {"nombre": "Spider-Man", "nombre_real": "Peter Parker", "anio_aparicion": 1962, "casa": "Marvel", "biografia": "Un joven picado por una araña radiactiva...", "imagenes": ["https://yoolk.ninja/wp-content/uploads/2021/05/Charavatar-Spider-Man.png"], "equipamiento": ["Lanza telarañas"]},
        {"nombre": "Iron Man", "nombre_real": "Tony Stark", "anio_aparicion": 1963, "casa": "Marvel", "biografia": "Genio, millonario, playboy y filántropo...", "imagenes": ["https://yoolk.ninja/wp-content/uploads/2021/05/Charavatar-Iron-Man.png"], "equipamiento": ["Armadura Mark 85"]},
        {"nombre": "Captain America", "nombre_real": "Steve Rogers", "anio_aparicion": 1941, "casa": "Marvel", "biografia": "El primer vengador, símbolo de libertad...", "imagenes": ["https://yoolk.ninja/wp-content/uploads/2021/05/Charavatar-Captain-America.png"], "equipamiento": ["Escudo de Vibranium"]},
        # ... (Acá completaríamos hasta los 40)
        
        # DC (10 mínimos)
        {"nombre": "Batman", "nombre_real": "Bruce Wayne", "anio_aparicion": 1939, "casa": "DC", "biografia": "El caballero de la noche de Gotham...", "imagenes": ["https://yoolk.ninja/wp-content/uploads/2021/05/Charavatar-Batman.png"], "equipamiento": ["Batarangs", "Batimovil"]},
        {"nombre": "Superman", "nombre_real": "Clark Kent", "anio_aparicion": 1938, "casa": "DC", "biografia": "El último hijo de Krypton...", "imagenes": ["https://yoolk.ninja/wp-content/uploads/2021/05/Charavatar-Superman.png"], "equipamiento": ["Capa"]},
        {"nombre": "Wonder Woman", "nombre_real": "Diana Prince", "anio_aparicion": 1941, "casa": "DC", "biografia": "Princesa de las Amazonas...", "imagenes": ["https://yoolk.ninja/wp-content/uploads/2021/05/Charavatar-Wonder-Woman.png"], "equipamiento": ["Lazo de la verdad"]},
    ]

    await collection.insert_many(heroes)
    print(f"✅ Se cargaron {len(heroes)} superhéroes con éxito.")

if __name__ == "__main__":
    asyncio.run(seed_data())