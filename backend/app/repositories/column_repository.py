from bson import ObjectId
from .base_repository import BaseRepository

class ColumnRepository(BaseRepository):
   
   def __init__(self):
        super().__init__('todocolumns')
      
   def update_todos(self, id: str, todos: list):
      return self.collection.update_one({'_id': ObjectId(id)}, {'$set': {'todos': todos}})
   
   def find_by_name(self, name: str):
        return self.collection.find_one({'name': name})

   def update_todos_by_name(self, name: str, todos: list):
        return self.collection.update_one({'name': name}, {'$set': {'todos': todos}})
   