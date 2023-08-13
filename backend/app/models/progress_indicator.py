from datetime import datetime
from typing import Optional
from models.base_model import BaseModelWithConfig
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from enum import Enum
from .py_object import PyObjectId

class ProgressStatus(Enum):
    GOOD = 'good'
    BAD  = 'bad'
    MODERATE = 'moderate'
    WORSE = 'worse'
    


class ProgressIndicator(BaseModelWithConfig):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    progress_status: str
    
class ProgressIndicatorOut(BaseModel):
    id: str
    progress_status: str

    @classmethod
    def from_db_model(cls, db_model: ProgressIndicator):
        return cls(
            id=str(db_model.id),
            progress_status=db_model.progress_status
        )