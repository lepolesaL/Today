from bson import ObjectId
from .base_repository import BaseRepository

class CommentRepository(BaseRepository):
    def __init__(self):
        super().__init__('comments')
    
    def find_by_todo_id(self, todo_id: str):
        return list(self.collection.find({"todo_id": ObjectId(todo_id)}))