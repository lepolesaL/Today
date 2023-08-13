from datetime import datetime
from typing import List, Optional
from models.base_model import BaseModelWithConfig
from models.todo import Todo
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from .py_object import PyObjectId   
    
class Project(BaseModelWithConfig):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    
    name: str
    description: str
    color: str # Enum
    # todos: Optional[List[Todo]]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    

class ProjectIn(Project):
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

# class ProjectUpdate(BaseModel):
#     description: str
#     new_tasks: Optional[list]
#     updated_tasks: Optional[list]
#     comments: Optional[list]


class ProjectId(BaseModel):
    id: str

