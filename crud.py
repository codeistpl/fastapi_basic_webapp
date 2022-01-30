from fastapi import HTTPException
from bson import ObjectId

import models
import schemas
from hashlib import sha512


def get_user(user_id: int):
    user = models.User.objects.all().filter(id=user_id).first()
    return user.pydantic() if user else None


def get_users(skip: int = 0, limit: int = 100):
    users = models.User.objects.all().skip(skip).limit(limit)
    print([user.pydantic() for user in users])
    return [schemas.User(**user.pydantic()) for user in users]


def create_user(user: schemas.UserCreate) -> schemas.User:
    db_user = models.User.objects.only("email").filter(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User.objects.only("user_name").filter(user_name=user.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="User name already registered")

    hashed_password = sha512(str(user.password + "this is salt").encode()).hexdigest()
    db_user = models.User(
        user_name=user.user_name, email=user.email, hashed_password=hashed_password
    )
    db_user.save()
    return schemas.User(**db_user.pydantic())


def get_items(skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
