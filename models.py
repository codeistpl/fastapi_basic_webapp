from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from py_object_id import PyObjectId
from bson import ObjectId
from datetime import datetime


class UpdateUser(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_name: str = Field(...)
    real_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_name": "jdo",
                "real_name": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "example",
            }
        }


class User(UpdateUser):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str = Field(...)
    created_at: datetime
    last_login: datetime
    active: bool = Field(default=True)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_name": "jdo",
                "real_name": "Jane Doe",
                "email": "jdoe@example.com",
                "created_at": "today",
            }
        }
