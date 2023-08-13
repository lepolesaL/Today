from bson import ObjectId
from database import db

class BaseRepository:
    def __init__(self, collection_name):
        self.collection = db[collection_name]

    def count_documents(self, filter={}):
        return self.collection.count_documents(filter)

    def drop(self):
        self.collection.drop()

    def insert_many(self, documents):
        return self.collection.insert_many(documents)
    
    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return str(result.inserted_id)
    
    def find_all(self):
        return list(self.collection.find())

    def find_by_id(self, id: str):
        return self.collection.find_one({'_id': ObjectId(id)})

    def create(self, data: dict):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, id: str, data: dict):
        result = self.collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        return result.modified_count > 0

    def delete(self, id: str):
        result = self.collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0

    def create_many(self, documents: list):
        # Convert Task objects to dictionaries and insert them into the collection
        document_dicts = [document.dict() for document in documents]
        result = self.collection.insert_many(document_dicts)
        return result.inserted_ids  # Return the list of inserted IDs
    
    def update_many(self, documents: list):
        for document in documents:
            document_dict = document.dict(exclude_unset=True)  # Exclude unset fields
            document_id = document_dict.pop('id', None)  # Get the ID and remove it from the dict
            if document_id:
                self.collection.update_one({'_id': ObjectId(document_id)}, {'$set': document_dict})
    