import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient("mongodb://superheroes_mongodb:27017")
    db = client["superheroes_db"]
    collection = db["superheroes"]

    exact_matches = {
        "Cyborg": "https://yoolk.ninja/wp-content/uploads/2019/07/DC-Comics-Cyborg-1024x819.png",
        "Wonder Woman": "https://yoolk.ninja/wp-content/uploads/2021/03/DC-Comics-Wonder-Woman-1024x819.png",
        "Green Lantern": "https://yoolk.ninja/wp-content/uploads/2021/03/DC-Comics-Green-Lantern-1024x819.png",
        "Martian Manhunter": "https://yoolk.ninja/wp-content/uploads/2021/03/DC-Comics-Martian-Manhunter-2-1024x819.png",
        "Harley Quinn": "https://yoolk.ninja/wp-content/uploads/2021/03/DC-Comics-Harley-Queen-1024x819.png",
        "Iron Man": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Iron-Man-1024x819.png",
        "Captain America": "https://yoolk.ninja/wp-content/uploads/2019/07/marvel-captain-america-1024x819.png",
        "Black Widow": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Black-Widow-1024x819.png",
        "Doctor Strange": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-DrStrange-1024x819.png",
        "Black Panther": "https://yoolk.ninja/wp-content/uploads/2019/07/marvel-black-panther-1024x819.png",
        "Ant Man": "https://yoolk.ninja/wp-content/uploads/2020/11/marvel-Ant-Man-1024x819.png",
        "Scarlet Witch": "https://yoolk.ninja/wp-content/uploads/2020/11/Marvel-Scarlet-Witch-1-1024x819.png"
    }

    cursor = collection.find({})
    async for hero in cursor:
        name = hero["name"]
        if name in exact_matches:
            print(f"Applying exact match for {name}")
            await collection.update_one({"_id": hero["_id"]}, {"$set": {"images": [exact_matches[name]]}})

if __name__ == "__main__":
    asyncio.run(main())
