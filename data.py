import json
import os

class Database():
    def __init__(self, name):
        self.filepath = 'data/' + name + 'DB.json'
        if os.path.exists(self.filepath): # if file exists do nothing
            pass
        else: # if file does not exist create blank file
            with open(self.filepath, 'w+') as f:
                print('[!] ',self.filepath, 'is missing, adding new entry')
                f.write(json.dumps({}))
    
    def get_database(self):
        try:
            with open(self.filepath, 'r') as f: # Return database as dict
                db = json.load(f)
                return db
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filepath, 'w+') as f:
                print('[!] ',self.filepath, ' lost during operation, recreating')
                f.write(json.dumps({}))
            return {}
    
    def save_database(self, db): # Delete database and save it again
        os.remove(self.filepath)
        with open(self.filepath, 'w+') as f:
            json.dump(db, f)
    
    def saveToDatabase(self, index, key, value): # Pulls dict from db file, then saves items to internal dict and saves to file
        db = self.get_database()
        if index not in db:
            db[index] = {}
        db[index][key] = value
        self.save_database(db)
    
    def getFromDatabase(self, index, key):
        db = self.get_database()
        value = db[index][key]
        return value