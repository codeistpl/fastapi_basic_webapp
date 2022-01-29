from pydantic import BaseModel
from py_object_id import PyObjectId


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: PyObjectId
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    user_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
