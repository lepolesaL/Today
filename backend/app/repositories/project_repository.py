from .base_repository import BaseRepository

class ProjectRepository(BaseRepository):
   
   def __init__(self):
        super().__init__('projects')