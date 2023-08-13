from .base_repository import BaseRepository
from bson import ObjectId

class TodoRepository(BaseRepository):
    
    def __init__(self):
        super().__init__('todos')
    # Add more specific methods as needed
    def find_by_project_id(self, project_id: str):
        return list(self.collection.find({"project_id": ObjectId(project_id)}))