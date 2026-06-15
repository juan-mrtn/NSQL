import asyncio
import re
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    with open('yoolk_images.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["superheroes_db"]
    collection = db["superheroes"]

    cursor = collection.find({})
    async for hero in cursor:
        name = hero["name"]
        house = hero["house"]
        
        # Build regex for fuzzy match
        search_term = name.replace(" ", "").replace("-", "").lower()
        if search_term == "spiderman": search_term = "spiderman"
        
        best_match = None
        for url in urls:
            url_lower = url.lower()
            if house.lower() in url_lower or "dc-comics" in url_lower:
                if search_term in url_lower:
                    best_match = url
                    break
                    
        # If no strict house match, look anywhere
        if not best_match:
            for url in urls:
                if search_term in url.lower():
                    best_match = url
                    break
        
        if best_match:
            print(f"Updating {name} -> {best_match}")
            await collection.update_one({"_id": hero["_id"]}, {"$set": {"images": [best_match]}})
        else:
            # Fallback format to 1024x819
            formatted_name = name.replace(' ', '-').replace("'", "")
            fallback = f"https://yoolk.ninja/wp-content/uploads/2019/07/{house}-{formatted_name}-1024x819.png"
            print(f"Fallback {name} -> {fallback}")
            await collection.update_one({"_id": hero["_id"]}, {"$set": {"images": [fallback]}})

if __name__ == "__main__":
    asyncio.run(main())
