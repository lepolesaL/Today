from datetime import datetime
from typing import List, Optional
from models.base_model import BaseModelWithConfig
from models.timestamp_mixin import TimeStampMixin
from models.task import Task
from models.todo_timer import TodoTimerOut
from models.comment import Comment
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from .py_object import PyObjectId
    
class Todo(BaseModelWithConfig):
    id: Optional[PyObjectId] = Field(alias='_id')
    title: str
    description: str
    status: str # Enum
    project_id: Optional[PyObjectId]

class TodoIn(TimeStampMixin, Todo):
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

class TodoOut(Todo):
    accumulated_time: Optional[int] = 0
    num_tasks: Optional[int] = 0
    num_completed_tasks: Optional[int] = 0
class TodoUpdate(BaseModel, TimeStampMixin):
    description: Optional[str]
    status: Optional[str]
    new_tasks: Optional[list] = Field(default=[])
    updated_tasks: Optional[list] = Field(default=[])
    new_comments: Optional[list]  = Field(default=[])
    updated_comments: Optional[list]  = Field(default=[])
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class TodoId(BaseModel):
    id: str

class TodoEvent(BaseModel):
    type: str
        