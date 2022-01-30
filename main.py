from datetime import datetime
from fastapi import FastAPI, Body, status, HTTPException
from models import User, UpdateUser
from database import db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from hashlib import sha512

app = FastAPI()

users_collection = db["users"]
salt = "lka;dsjf a89u"


@app.post("/", response_description="Add new user", response_model=User)
async def create_user(user: UpdateUser = Body(...)):
    user = jsonable_encoder(user)
    user["active"] = False
    user["hashed_password"] = sha512(str(user["password"] + salt).encode()).hexdigest()
    user.pop("password")
    user["created_at"] = datetime.now().isoformat()
    new_user = await users_collection.insert_one(user)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@app.get("/", response_description="List all users", response_model=List[User])
async def list_users():
    users = await users_collection.find().to_list(1000)
    return users


@app.get("/{id}", response_description="Get a single user", response_model=User)
async def show_user(id: str):
    if (user := await users_collection.find_one({"_id": id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"user {id} not found")


@app.put("/{id}", response_description="Update a user", response_model=User)
async def update_user(id: str, user: UpdateUser = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await users_collection.update_one({"_id": id}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := await users_collection.find_one({"_id": id})
            ) is not None:
                return updated_user

    if (existing_user := await users_collection.find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"user {id} not found")


@app.delete("/{id}", response_description="Delete a user")
async def delete_user(id: str):
    delete_result = await users_collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"user {id} not found")
