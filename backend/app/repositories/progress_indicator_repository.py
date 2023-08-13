from .base_repository import BaseRepository
from bson import ObjectId

class ProgressIndicatorRepository(BaseRepository):
    def __init__(self):
        super().__init__('progressindicator')

    def get_current_indicator(self):
       return self.collection.find_one({})
    
    def update_status(self, status: str):
        return self.collection.find_one_and_update({}, {'$set': {"progress_status": status}})