from pydantic import BaseModel
from bson import ObjectId

class BaseModelWithConfig(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def dict(self, *args, **kwargs):
        dict_representation = super().dict(*args, **kwargs)
        if "_id" in dict_representation:
            dict_representation["id"] = str(dict_representation.pop("_id"))
        return dict_representation