import json
from database import get_db

async def seed_data():
    db = get_db()
    count = await db["superheroes"].count_documents({})
    if count == 0:
        print("Seeding database with 40 superheroes...")
        
        exact_matches = {
            "Spiderman": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Spiderman-1024x819.png",
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
            "Scarlet Witch": "https://yoolk.ninja/wp-content/uploads/2020/11/Marvel-Scarlet-Witch-1-1024x819.png",
            "Batman": "https://yoolk.ninja/wp-content/uploads/2019/07/DC-Comics-batman-1024x819.png",
            "Superman": "https://yoolk.ninja/wp-content/uploads/2019/07/DC-Comics-Superman-1024x819.png",
            "Thor": "https://yoolk.ninja/wp-content/uploads/2019/07/marvel-thor-1024x819.png",
            "Hulk": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Hulk-1024x819.png",
            "Wolverine": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Wolverine-v2-def-1024x819.png",
            "Deadpool": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Deadpool-1-1024x819.png",
            "Vision": "https://yoolk.ninja/wp-content/uploads/2019/07/marvel-vision-1024x819.png",
            "Hawkeye": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Hawkeye-1024x819.png",
            "Daredevil": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Daredevil-1024x819.png",
            "Punisher": "https://yoolk.ninja/wp-content/uploads/2019/07/marvel-punisher-1024x819.png",
            "Groot": "https://yoolk.ninja/wp-content/uploads/2024/05/Marvel-Groot-1.png",
            "Venom": "https://yoolk.ninja/wp-content/uploads/2019/07/Marvel-Venom-alt-1024x819.png",
            "Flash": "https://yoolk.ninja/wp-content/uploads/2019/07/dc-flash-1024x819.png",
            "Aquaman": "https://yoolk.ninja/wp-content/uploads/2019/07/dc-aquaman-1024x819.png",
            "Shazam": "https://yoolk.ninja/wp-content/uploads/2019/07/dc-shazam-1024x819.png",
            "Joker": "https://yoolk.ninja/wp-content/uploads/2019/07/dc-joker-alt-1-1024x819.png",
            "Catwoman": "https://yoolk.ninja/wp-content/uploads/2021/03/DC-Comics-Catwoman-2-1024x819.png",
            "Darkseid": "https://yoolk.ninja/wp-content/uploads/2021/03/DC-Comics-Darkseid-1-1024x819.png"
        }

        def get_yoolk_avatar(name, house):
            if name in exact_matches:
                return exact_matches[name]
            formatted_name = name.lower().replace(' ', '-').replace("'", "")
            return f"https://yoolk.ninja/wp-content/uploads/2019/07/{house}-{formatted_name}-1024x819.png"

        superheroes = [
            # MARVEL (20)
            {
            "name": "Spiderman", "real_name": "Peter Parker", "appearance_year": 1962, "house": "Marvel",
            "biography": "Bitten by a radioactive spider, Peter Parker gained amazing powers and became Spiderman.",
            "equipment": ["Web-shooters", "Spider-Suit"],
            "images": [get_yoolk_avatar("Spiderman", "Marvel")]
        },
        {
            "name": "Iron Man", "real_name": "Tony Stark", "appearance_year": 1963, "house": "Marvel",
            "biography": "Genius, billionaire, playboy, philanthropist who built a high-tech suit to save the world.",
            "equipment": ["Iron Man Armor", "Repulsors"],
            "images": [get_yoolk_avatar("Iron Man", "Marvel")]
        },
        {
            "name": "Captain America", "real_name": "Steve Rogers", "appearance_year": 1941, "house": "Marvel",
            "biography": "A frail young man enhanced to the peak of human perfection by an experimental serum.",
            "equipment": ["Vibranium Shield"],
            "images": [get_yoolk_avatar("Captain America", "Marvel")]
        },
        {
            "name": "Thor", "real_name": "Thor Odinson", "appearance_year": 1962, "house": "Marvel",
            "biography": "The God of Thunder, who wields the enchanted hammer Mjolnir.",
            "equipment": ["Mjolnir", "Stormbreaker"],
            "images": [get_yoolk_avatar("Thor", "Marvel")]
        },
        {
            "name": "Hulk", "real_name": "Bruce Banner", "appearance_year": 1962, "house": "Marvel",
            "biography": "A scientist who transforms into a giant, green, rage-fueled monster when angry.",
            "equipment": [],
            "images": [get_yoolk_avatar("Hulk", "Marvel")]
        },
        {
            "name": "Black Widow", "real_name": "Natasha Romanoff", "appearance_year": 1964, "house": "Marvel",
            "biography": "A highly trained former KGB assassin and agent of S.H.I.E.L.D.",
            "equipment": ["Widow's Bite", "Glock 26"],
            "images": [get_yoolk_avatar("Black Widow", "Marvel")]
        },
        {
            "name": "Doctor Strange", "real_name": "Stephen Strange", "appearance_year": 1963, "house": "Marvel",
            "biography": "A former surgeon who becomes the Sorcerer Supreme to defend Earth against magical threats.",
            "equipment": ["Cloak of Levitation", "Eye of Agamotto"],
            "images": [get_yoolk_avatar("Doctor Strange", "Marvel")]
        },
        {
            "name": "Wolverine", "real_name": "Logan", "appearance_year": 1974, "house": "Marvel",
            "biography": "A mutant with animal-keen senses, enhanced physical capabilities, and a powerful regenerative ability.",
            "equipment": ["Adamantium Claws"],
            "images": [get_yoolk_avatar("Wolverine", "Marvel")]
        },
        {
            "name": "Black Panther", "real_name": "T'Challa", "appearance_year": 1966, "house": "Marvel",
            "biography": "The king and protector of the fictional African nation of Wakanda.",
            "equipment": ["Vibranium Suit", "Claws"],
            "images": [get_yoolk_avatar("Black Panther", "Marvel")]
        },
        {
            "name": "Deadpool", "real_name": "Wade Wilson", "appearance_year": 1991, "house": "Marvel",
            "biography": "A wisecracking mercenary with a rapid healing factor.",
            "equipment": ["Katanas", "Dual Pistols"],
            "images": [get_yoolk_avatar("Deadpool", "Marvel")]
        },
        {
            "name": "Captain Marvel", "real_name": "Carol Danvers", "appearance_year": 1968, "house": "Marvel",
            "biography": "An Air Force pilot who gained cosmic powers after being exposed to alien energy.",
            "equipment": [],
            "images": [get_yoolk_avatar("Captain Marvel", "Marvel")]
        },
        {
            "name": "Ant Man", "real_name": "Scott Lang", "appearance_year": 1979, "house": "Marvel",
            "biography": "A thief who uses a suit that allows him to shrink in size but increase in strength.",
            "equipment": ["Ant-Man Suit", "Pym Particles"],
            "images": [get_yoolk_avatar("Ant Man", "Marvel")]
        },
        {
            "name": "Scarlet Witch", "real_name": "Wanda Maximoff", "appearance_year": 1964, "house": "Marvel",
            "biography": "A powerful mutant who can harness chaos magic.",
            "equipment": [],
            "images": [get_yoolk_avatar("Scarlet Witch", "Marvel")]
        },
        {
            "name": "Vision", "real_name": "Vision", "appearance_year": 1968, "house": "Marvel",
            "biography": "An android created by Ultron, who later became an Avenger.",
            "equipment": ["Mind Stone"],
            "images": [get_yoolk_avatar("Vision", "Marvel")]
        },
        {
            "name": "Hawkeye", "real_name": "Clint Barton", "appearance_year": 1964, "house": "Marvel",
            "biography": "A master archer and highly skilled marksman.",
            "equipment": ["Bow", "Trick Arrows"],
            "images": [get_yoolk_avatar("Hawkeye", "Marvel")]
        },
        {
            "name": "Daredevil", "real_name": "Matt Murdock", "appearance_year": 1964, "house": "Marvel",
            "biography": "A blind lawyer by day who fights crime by night using his heightened senses.",
            "equipment": ["Billy Club"],
            "images": [get_yoolk_avatar("Daredevil", "Marvel")]
        },
        {
            "name": "Punisher", "real_name": "Frank Castle", "appearance_year": 1974, "house": "Marvel",
            "biography": "A vigilante who employs murder, kidnapping, and torture in his campaign against crime.",
            "equipment": ["Assault Rifles", "Combat Knives"],
            "images": [get_yoolk_avatar("Punisher", "Marvel")]
        },
        {
            "name": "Groot", "real_name": "Groot", "appearance_year": 1960, "house": "Marvel",
            "biography": "A sentient, tree-like creature who only speaks the phrase 'I am Groot'.",
            "equipment": [],
            "images": [get_yoolk_avatar("Groot", "Marvel")]
        },
        {
            "name": "Star Lord", "real_name": "Peter Quill", "appearance_year": 1976, "house": "Marvel",
            "biography": "An intergalactic adventurer and leader of the Guardians of the Galaxy.",
            "equipment": ["Element Guns", "Jet Boot Attachments"],
            "images": [get_yoolk_avatar("Star Lord", "Marvel")]
        },
        {
            "name": "Venom", "real_name": "Eddie Brock", "appearance_year": 1988, "house": "Marvel",
            "biography": "A sentient alien symbiote that bonds with a human host to survive.",
            "equipment": ["Symbiote Suit"],
            "images": [get_yoolk_avatar("Venom", "Marvel")]
        },

        # DC (20)
        {
            "name": "Batman", "real_name": "Bruce Wayne", "appearance_year": 1939, "house": "DC",
            "biography": "A billionaire philanthropist who fights crime in Gotham City utilizing his intellect and gadgets.",
            "equipment": ["Batarangs", "Batmobile", "Grappling Hook"],
            "images": [get_yoolk_avatar("Batman", "DC")]
        },
        {
            "name": "Superman", "real_name": "Clark Kent", "appearance_year": 1938, "house": "DC",
            "biography": "An alien from Krypton with immense powers, raised on Earth, who uses his abilities to help humanity.",
            "equipment": ["Kryptonian Suit"],
            "images": [get_yoolk_avatar("Superman", "DC")]
        },
        {
            "name": "Wonder Woman", "real_name": "Diana Prince", "appearance_year": 1941, "house": "DC",
            "biography": "An Amazonian warrior princess with superhuman strength, agility, and a magical lasso.",
            "equipment": ["Lasso of Truth", "Bracelets of Submission"],
            "images": [get_yoolk_avatar("Wonder Woman", "DC")]
        },
        {
            "name": "Flash", "real_name": "Barry Allen", "appearance_year": 1956, "house": "DC",
            "biography": "A forensic scientist who gained the power of super-speed after being struck by lightning.",
            "equipment": ["Flash Ring"],
            "images": [get_yoolk_avatar("Flash", "DC")]
        },
        {
            "name": "Aquaman", "real_name": "Arthur Curry", "appearance_year": 1941, "house": "DC",
            "biography": "The half-human, half-Atlantean king of the sea with the ability to communicate with marine life.",
            "equipment": ["Trident of Neptune"],
            "images": [get_yoolk_avatar("Aquaman", "DC")]
        },
        {
            "name": "Green Lantern", "real_name": "Hal Jordan", "appearance_year": 1959, "house": "DC",
            "biography": "A test pilot who is chosen by an alien ring to be a member of an intergalactic police force.",
            "equipment": ["Power Ring", "Power Battery"],
            "images": [get_yoolk_avatar("Green Lantern", "DC")]
        },
        {
            "name": "Cyborg", "real_name": "Victor Stone", "appearance_year": 1980, "house": "DC",
            "biography": "A former athlete whose body was rebuilt with advanced technology after a tragic accident.",
            "equipment": ["Cybernetic Enhancements", "Sonic Cannon"],
            "images": [get_yoolk_avatar("Cyborg", "DC")]
        },
        {
            "name": "Green Arrow", "real_name": "Oliver Queen", "appearance_year": 1941, "house": "DC",
            "biography": "A wealthy playboy who uses his archery skills to fight crime in Star City.",
            "equipment": ["Custom Bow", "Trick Arrows"],
            "images": [get_yoolk_avatar("Green Arrow", "DC")]
        },
        {
            "name": "Martian Manhunter", "real_name": "J'onn J'onzz", "appearance_year": 1955, "house": "DC",
            "biography": "The last survivor of Mars, possessing incredible powers like telepathy, shape-shifting, and flight.",
            "equipment": [],
            "images": [get_yoolk_avatar("Martian Manhunter", "DC")]
        },
        {
            "name": "Nightwing", "real_name": "Dick Grayson", "appearance_year": 1984, "house": "DC",
            "biography": "Batman's former protégé, the original Robin, who struck out on his own to become Nightwing.",
            "equipment": ["Escrima Sticks", "Wingdings"],
            "images": [get_yoolk_avatar("Nightwing", "DC")]
        },
        {
            "name": "Shazam", "real_name": "Billy Batson", "appearance_year": 1940, "house": "DC",
            "biography": "A young boy who can transform into a powerful adult superhero by shouting 'Shazam!'.",
            "equipment": [],
            "images": [get_yoolk_avatar("Shazam", "DC")]
        },
        {
            "name": "Joker", "real_name": "Unknown", "appearance_year": 1940, "house": "DC",
            "biography": "Batman's arch-nemesis, an unpredictable and chaotic criminal mastermind.",
            "equipment": ["Joker Venom", "Razor-sharp Playing Cards"],
            "images": [get_yoolk_avatar("Joker", "DC")]
        },
        {
            "name": "Harley Quinn", "real_name": "Harleen Quinzel", "appearance_year": 1992, "house": "DC",
            "biography": "A former psychiatrist who fell in love with the Joker and became his chaotic accomplice.",
            "equipment": ["Oversized Mallet", "Baseball Bat"],
            "images": [get_yoolk_avatar("Harley Quinn", "DC")]
        },
        {
            "name": "Lex Luthor", "real_name": "Lex Luthor", "appearance_year": 1940, "house": "DC",
            "biography": "Superman's greatest foe, a billionaire genius with an intense hatred for the Man of Steel.",
            "equipment": ["Warsuit", "Kryptonite"],
            "images": [get_yoolk_avatar("Lex Luthor", "DC")]
        },
        {
            "name": "Catwoman", "real_name": "Selina Kyle", "appearance_year": 1940, "house": "DC",
            "biography": "A highly skilled cat burglar and occasional ally (and romantic interest) to Batman.",
            "equipment": ["Whip", "Claws"],
            "images": [get_yoolk_avatar("Catwoman", "DC")]
        },
        {
            "name": "Bane", "real_name": "Unknown", "appearance_year": 1993, "house": "DC",
            "biography": "A brilliant and incredibly strong villain who famously broke Batman's back.",
            "equipment": ["Venom Enhancer"],
            "images": [get_yoolk_avatar("Bane", "DC")]
        },
        {
            "name": "Darkseid", "real_name": "Uxas", "appearance_year": 1970, "house": "DC",
            "biography": "The tyrannical ruler of Apokolips, whose ultimate goal is to conquer the universe.",
            "equipment": ["Omega Beams"],
            "images": [get_yoolk_avatar("Darkseid", "DC")]
        },
        {
            "name": "Supergirl", "real_name": "Kara Zor-El", "appearance_year": 1959, "house": "DC",
            "biography": "Superman's cousin, who shares his incredible Kryptonian powers.",
            "equipment": ["Kryptonian Suit"],
            "images": [get_yoolk_avatar("Supergirl", "DC")]
        },
        {
            "name": "Batgirl", "real_name": "Barbara Gordon", "appearance_year": 1967, "house": "DC",
            "biography": "The daughter of Commissioner Gordon, who fights crime alongside Batman.",
            "equipment": ["Batarangs", "Batcycle"],
            "images": [get_yoolk_avatar("Batgirl", "DC")]
        },
        {
            "name": "Red Hood", "real_name": "Jason Todd", "appearance_year": 2005, "house": "DC",
            "biography": "The second Robin, resurrected and operating as a lethal vigilante.",
            "equipment": ["Dual Pistols", "Combat Knives"],
            "images": [get_yoolk_avatar("Red Hood", "DC")]
        }
        ]
        await db["superheroes"].insert_many(superheroes)
        print("Seeding complete.")
