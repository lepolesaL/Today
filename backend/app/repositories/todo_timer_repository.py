from bson import ObjectId
from pymongo import DESCENDING
from .base_repository import BaseRepository

class TodoTimerRepository(BaseRepository):
   
    def __init__(self):
        super().__init__('todotimers')
        
    def find_one_by_todo_id(self, todo_id: str):
        result = self.collection.find_one({"todo_id": ObjectId(todo_id)}, sort=[("position", DESCENDING)])
        if result:
            return result
        else:
            return None
    
    def update_todo_timer(self, id: str, todo_id: str, status: str, accumulated_time: int):
        result = self.collection.update_one({'_id': ObjectId(id), 'todo_id': ObjectId(todo_id)}, {'$set': {'status': status, 'accumulated_time': accumulated_time}})
        return result