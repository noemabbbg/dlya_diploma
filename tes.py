import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://noema:658Vobisi@check.8n3yvam.mongodb.net/?retryWrites=true&w=majority")
db=client["Check"]

def add_chapter_by_u_name(u_name, chapter_number, chapter_data):
    new = db["smanhwa"]
    document = new.find_one({"u_name": u_name})
    
    if document:
        chapters = document.get("chapters", {})
        chapters[chapter_number] = chapter_data
        new_number_of_chapters = int(document.get("number_of_chapters", 0)) + 1
        new.update_one(
            {"u_name": u_name},
            {"$set": {"chapters": chapters, "number_of_chapters": str(new_number_of_chapters)}}
        )
        print("Chapter added successfully.")
    else:
        print(f"No document found with u_name: {u_name}")


add_chapter_by_u_name("Девушка рядом со мной слишком элегантна", '4', 'testtesttest')