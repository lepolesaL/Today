from datetime import datetime
from typing import Optional

class TimeStampMixin:
    # created_at: Optional[datetime]
    # modified_at: Optional[datetime]
    # def __init__(self):
        # self.created_at: Optional[datetime]
        # self.modified_at: Optional[datetime]
        
    def create_timestamp(self):
        self.created_at =  datetime.now()
        self.modified_at = datetime.now()
    
    def update_timestamp(self):
        self.modified_at = datetime.now()