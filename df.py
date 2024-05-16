from webbrowser import get
import pymongo
from pymongo import MongoClient
from downloader import P 
class ReprDict(dict):
    def __repr__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.items())
client = MongoClient("mongodb+srv://noema:658Vobisi@check.8n3yvam.mongodb.net/?retryWrites=true&w=majority")
db=client["Check"]
manhwa_data = db['smanhwa']
manhwa_chapters = db['ex']

def add_u_title_list(url):
    u_list = db['u_list']
    existing_url = u_list.find_one({"url": url})
    
    if existing_url is None:
        u_list.insert_one({"url": url})
        print('added')
    else:
         print('exist')


def get_u_title_list():
     u_list = db['u_list']
     urls = list(u_list.find({}))
     return [url['url'] for url in urls]

print(get_u_title_list())

def add_manhwa_by_scraper(name, test_dict):
     manhwa_scrapped = db['smanhwa']
     manhwa_scrapped.insert_one({
        "name": name,
        "u_name": P.u_name,
        "picture": P.title_picture,
        "description": P.description,
        "number_of_chapters": P.number_of_chapters,
        "release_year":P.release_year ,
        "genres": P.genres,
        "manhwa_state": P.manhwa_state,
        "chapters": test_dict
     })

def register_user(user_id):
    new = db["users"]
    if  new.count_documents({'user_id': f"{user_id}"}) == 0:
       a = new.insert_one({"user_id" : f"{user_id}", 'selected_manhwa': 'zero', 'selected_chapter':1})


def selected_manhwa(manhwa_name, user_id):
    new = db["users"]
    new.update_one({"user_id" : f"{user_id}"}, {"$set":{"selected_manhwa":manhwa_name}})
    #new.update({'user_id': user_id}, {"$set": { "selected_manhwa": manhwa_name }} )

def selected_chapter(user_id):
    new = db['users']
    users = list(new.find({"user_id" : f"{user_id}"})) 
    
    return [user['selected_chapter'] for user in users]


# find по всем манхвам -> берем список жанров у произведения и делаеим сравнение -> если совпадает добавляем.
'''
def available_genres():
    new = db['genres']
    genres = list(new.find({}))
    return [user['genre'] for user in genres]
'''
def available_genres():
    new = db['smanhwa']
    genres = list(new.find({}, {'genres':1, '_id':0}))

    return [genre for sublist in genres for genre in sublist['genres']]


def available_manhwa():
    new = db['smanhwa']
    manhwa = list(new.find({}))
    def_list =  [user['name'] for user in manhwa]
    u_list = [user['u_name'] for user in manhwa]
    return def_list

def user_bookmarks():   ####доделать как будет добавлено 
    new = db['users']
    manhwa = list(new.find({}))
    def_list =  [user['name'] for user in manhwa]
    u_list = [user['u_name'] for user in manhwa]
    return def_list


def u_available_manhwa():
    new = db['smanhwa']
    manhwa = list(new.find({}))
    u_list = [user['u_name'] for user in manhwa]
    return u_list


def add_genre(genres):
    new = db['genres']
    genre_list = genres.split(', ')
    i=0
    while i<len(genre_list):
        genre = genre_list[i]
        if  new.count_documents({'genre': genre}) == 0:
            new.insert_one({'genre': genre})
        i+=1

def find_manhwa_genre(genre_name):
    genre_db = db['genres']
    manhwa_db = db['smanhwa']
    genres = list(genre_db.find({}))
    accepted_manhwa = []
    manhwa_genres = list(manhwa_db.find({})) # передавать в какой то последовательности список манхв
   
    genre_list = [user['genre'] for user in genres]
    #manhwa_genre_list = [(manhwa_genres['genres'])]
    manhwa_genre_list = [user['genres'] for user in manhwa_genres]
    all_manhwa =  [user['name'] for user in manhwa_genres]
    
    k=0
   
    while k<len(all_manhwa):
        manhwa_genres = list(manhwa_db.find({'name':all_manhwa[k]}))
        
        manhwa_name = []
        for user in manhwa_genres:
            manhwa_name.append(user['name'])

       
        #manhwa_name = [user['name'] for user in manhwa_genres]
        #manhwa_genre_list = manhwa_genres[0]
        nwe = []
        for user in manhwa_genres:
            nwe.append(user['genres'])
        ab = (str(nwe).replace('[', '').replace(']', '').replace(', ', ' ').replace("'", ''))
        nwe = ab.split()
       
        k+=1
        i=0
       
        while i<len(nwe):
            
            if nwe[i] == genre_name:
                
                manhwa_name = str(manhwa_name).replace("['", "").replace("']", "")
                accepted_manhwa.append((manhwa_name))
            i+=1
        

    return accepted_manhwa

            #if manhwa_genre_list[i] == genre_name:
               # accepted_manhwa.append()
    

def u_find_manhwa_genre(genre_name):
    genre_db = db['genres']
    manhwa_db = db['smanhwa']
    genres = list(genre_db.find({}))
    accepted_manhwa = []
    manhwa_genres = list(manhwa_db.find({})) # передавать в какой то последовательности список манхв
   
    genre_list = [user['genre'] for user in genres]
    #manhwa_genre_list = [(manhwa_genres['genres'])]
    manhwa_genre_list = [user['genres'] for user in manhwa_genres]
    all_manhwa =  [user['u_name'] for user in manhwa_genres]
    
    k=0
   
    while k<len(all_manhwa):
        manhwa_genres = list(manhwa_db.find({'u_name':all_manhwa[k]}))
        
        manhwa_name = []
        for user in manhwa_genres:
            manhwa_name.append(user['u_name'])

       
        #manhwa_name = [user['name'] for user in manhwa_genres]
        #manhwa_genre_list = manhwa_genres[0]
        nwe = []
        for user in manhwa_genres:
            nwe.append(user['genres'])
        ab = (str(nwe).replace('[', '').replace(']', '').replace(', ', ' ').replace("'", ''))
        nwe = ab.split()
       
        k+=1
        i=0
       
        while i<len(nwe):
            
            if nwe[i] == genre_name:
                
                manhwa_name = str(manhwa_name).replace("['", "").replace("']", "")
                accepted_manhwa.append((manhwa_name))
            i+=1
        

    return accepted_manhwa 
    
# сравниваю жанр произведения со всеми жанрами.
ik = u_find_manhwa_genre('приключения')
print(ik)








def update_selected_chapter(user_id, selected_chapter):
    new = db['users']
    new.update_one({"user_id" : f"{user_id}"}, {"$set":{"selected_chapter":selected_chapter}})
    






def get_chapters(manhwa_name, chapter_number): # сбитая нумерация глав + manhwa_name не используется. по manhwa_name найти object id и по нему идти в таблицу.
    manhwa_data = db['smanhwa']
    manhwa_id = manhwa_data.find_one({"name": manhwa_name[0]}, {"chapters": 1})
    print(manhwa_id['chapters'][str(chapter_number)])
    
    
   
    #chapter_id = [user['chapter_id'] for user in chapter_id]
   
    return manhwa_id['chapters'][str(chapter_number)]






'''




    manhwa_data = db['smanhwa']
    
    photo =  manhwa_data.find_one({'name': manhwa_name }, { '_id':1})
    photo_new = str(photo).replace('{', '').replace('}', '').replace("'", '').replace(":", '').replace("_id", '').replace(" ", '')
    
    buffer_data = db[photo_new]
    photo =  list(buffer_data.find({'chapter_number': chapter_number}))
    #print([user['chapter_id'] for user in photo])
    #return [user['chapter_id'] for user in photo]
    chapter_id = buffer_data.find_one({'chapter_number': chapter_number}, {'chapter_id':1, '_id':0})

    photo_new = str(chapter_id).replace('{', '').replace('}', '').replace("'", '').replace(":", '').replace("chapter_id", '').replace(" ", '')
    return photo_new
    '''





def get_all_users_identificators(): 
        new = db['smanhwa']
        users = list(new.find())
        return [user['_id'] for user in users]



def get_selected_manhwa(user_id):
    new = db['users']
    photo =  list(new.find({'user_id': f"{user_id}" }))
    return [user['selected_manhwa'] for user in photo]
    photo = new.find_one({'user_id': f"{user_id}" }, {'selected_manhwa':1, '_id':0})
    photo_new = str(photo).replace('{', '').replace('}', '').replace("'", '').replace(":", '').replace("selected_manhwa", '').replace(" ", '')
    return photo_new




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

def add_chapters_to_storage(name, chapter_number, chapter_id): #либо хреначить по манхва ид либо по нейму  
    manhwa_chapters = db[f"{name}"]
    manhwa_chapters.insert_one({
        'chapter_number': chapter_number,
        'chapter_id': chapter_id
    })

def add_to_storage( name, picture,description, number_of_chapters,release_year,genres,manhwa_state):
        manhwa_data.insert_one({
            'name': name,
            'picture': picture,
            'description': description,
            'number_of_chapters': number_of_chapters,
            'release_year': release_year,
            'genres': genres,
            'manhwa_state': manhwa_state,
            'default_chap_name': ''
        })


def find_document(collection, elements):
        users = collection.find(elements)
        return [user['name'] for user in users]
    
def manhwa_id(collection, elements):
        users = collection.find(elements)
        return [user['_id'] for user in users]

def find_document_id(collection, elements, elements_2, multiple=True):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements, elements_2)
        return [r for r in results]
        
    else:
            return collection.find_one(elements, elements_2)
            #return collection.find_one(elements)




def get_photo(manhwa_name):
    manhwa_data = db['smanhwa']
    #photo =  manhwa_data.find_one({'name': manhwa_name }, {'picture':1, '_id':0})
    users = list(manhwa_data.find({"name" : manhwa_name })) 
    return [user['picture'] for user in users]

    photo_new = str(photo).replace('{', '').replace('}', '').replace("'", '').replace(":", '').replace("picture", '').replace(" ", '')
    #return photo_new
def get_description(manhwa_name):
    manhwa_data = db['smanhwa']
    photo =  list(manhwa_data.find({'name': manhwa_name }))
    return [user['description'] for user in photo]
    #return photo_new

def get_number_of_chap(manhwa_name):
    manhwa_data = db['smanhwa']
    photo =  list(manhwa_data.find({'name': manhwa_name }))
    return [user['number_of_chapters'] for user in photo]
    photo =  manhwa_data.find_one({'name': manhwa_name }, {'number_of_chapters':1, '_id':0})
    photo_new = str(photo).replace('{', '').replace('}', '').replace("'", '').replace(":", '').replace("number_of_chapters", '').replace(" ", '')
    return photo_new

def get_manhwa_genres(manhwa_name):
    manhwa_data = db['smanhwa']
    photo =  list(manhwa_data.find({'name': manhwa_name }))
    return [user['genres'] for user in photo]
    

def get_release_year(manhwa_name):
    manhwa_data = db['smanhwa']
    photo =  list(manhwa_data.find({'name': manhwa_name }))
    return [user['release_year'] for user in photo]

def get_manhwa_state(manhwa_name):
    manhwa_data = db['smanhwa']
    photo =  list(manhwa_data.find({'name': manhwa_name }))
    return [user['manhwa_state'] for user in photo]
    


