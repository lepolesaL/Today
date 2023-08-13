from datetime import datetime
from typing import Optional
from models.base_model import BaseModelWithConfig
from pydantic import BaseModel, Field, validator
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
    
class Column(BaseModelWithConfig):
    id: Optional[PyObjectId] = Field(alias='_id')
    col_ref: str
    name: str
    color: str # Enum
    todos: list
