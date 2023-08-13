from datetime import datetime
from typing import List, Optional
from models.base_model import BaseModelWithConfig
from models.task import Task
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from .py_object import PyObjectId
    
class Comment(BaseModelWithConfig):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    text: str
    todo_id: Optional[PyObjectId]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    
    def create(self, todo_id: ObjectId = None):
        self.todo_id = todo_id if todo_id != None else self.todo_id
        self.created_at = datetime.now()
        return self

class CommentIn(Comment):
    @validator('created_at', always=True)
    def set_created_at(cls, v, values):
        if values['id'] is None:
          return datetime.now()
        else:
            return v
    
    @validator('modified_at', always=True)
    def set_modified_at(cls, v, values):
        if values['id'] is not None:
            return datetime.now()
        else:
            return v

class CommentId(BaseModel):
    id: str
