from datetime import datetime
from typing import Optional
from models.column import PyObjectId
from models.base_model import BaseModelWithConfig
from pydantic import BaseModel, Field, validator
from bson import ObjectId
  

    
class Task(BaseModelWithConfig):
    id: Optional[PyObjectId] = Field(alias='_id')
    title: str
    status: bool
    todo_id: PyObjectId

# class TodoIn(Todo):
#     @validator('created_at', always=True)
#     def set_created_at(cls, v, values):
#         if values['id'] is None:
#           return datetime.now()
#         else:
#             return v
    
#     @validator('modified_at', always=True)
#     def set_modified_at(cls, v, values):
#         if values['id'] is not None:
#             return datetime.now()
#         else:
#             return v

# class TodoUpdate(BaseModel):
#     description: str
#     task_list: Optional[list]
#     comments: Optional[list]


# class TodoId(BaseModel):
#     id: str
        