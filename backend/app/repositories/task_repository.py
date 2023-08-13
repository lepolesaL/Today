from .base_repository import BaseRepository
from bson import ObjectId

class TaskRepository(BaseRepository):
   
    def __init__(self):
        super().__init__('tasks')
    
    def count_completed_by_todo_id(self, todo_id: str):
        return  self.count_documents({"todo_id": todo_id, "status": True})
    
    def count_by_todo_id(self, todo_id: str):
        return self.count_documents({"todo_id": todo_id})
    
    def find_by_todo_id(self, todo_id: str):
        return list(self.collection.find({"todo_id": ObjectId(todo_id)}))
    