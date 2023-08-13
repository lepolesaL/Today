from datetime import datetime
from typing import Optional
from models.base_model import BaseModelWithConfig
from models.timestamp_mixin import TimeStampMixin
from pydantic import BaseModel, Field
from bson import ObjectId
  
 
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')   
    
class TodoTimer(TimeStampMixin, BaseModelWithConfig):
    id: Optional[PyObjectId] = Field(alias='_id')
    status: str
    accumulated_time: int = 0
    todo_id: Optional[PyObjectId]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    
    def create(self, todo_id: PyObjectId = None):
        self.todo_id = todo_id if todo_id != None else self.todo_id
        self.create_timestamp()
        return self
    
    # def update(self):
    #     self.modified_at = datetime.now()
    #     return self

class TodoTimerOut(BaseModel):
    status: str
    accumulated_time: int = 0

# class CreateTodoTimer(TodoTimer):
#     @validator('created_at', always=True)
#     def set_created_at(cls, v, values):
#         if values['id'] is None:
#           return datetime.now()
#         else:
#             return v
    
    # @classmethod
    # def create
    # # @validator('modified_at', always=True)
    # # def set_modified_at(cls, v, values):
    # #     if values['id'] is not None:
    # #         return datetime.now()
    # #     else:
    # #         return v

class TodoTimerId(BaseModel):
    id: str

class TodoTimerUpdate(BaseModel, TimeStampMixin):
    status: str
    accumulated_time: Optional[int]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]