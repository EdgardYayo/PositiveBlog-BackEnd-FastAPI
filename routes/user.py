from fastapi import APIRouter, HTTPException, Response
from config.db import connection
from schemas.user import user_entity, users_entity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId

user = APIRouter()



@user.get("/user/all", response_model=list, tags=["users"])
def get_all_users():
    try:
        users = users_entity(connection.local.user.find())
        return users 
    except:
        return HTTPException(status_code=404, detail="There are no users at the moment")


@user.post("/user/new", response_model=str, tags=["users"])
def create_user(user: User):
    try:
        new_user = dict(user)
        new_user["password"] = sha256_crypt.encrypt(new_user["password"])
        print(new_user)
        connection.local.user.insert_one(new_user).inserted_id
        user_entity(new_user)
        return Response(status_code=201, content="User created successfully")
    except:
        return HTTPException(status_code=400, detail="Somenthing went wrong, try it again later")


@user.get("/user/{id}", response_model=User, tags=["users"])
def get_user(id: str):
   try:
       return user_entity(connection.local.user.find_one(ObjectId(id)))
   except:
       return HTTPException(status_code=404, detail="User not found")


@user.put("/user/{id}", response_model=str, tags=["users"])
def update_user(id: str, user: User):
    try:
        user_to_updated = user_entity(connection.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)}))
        user_to_updated["password"] = sha256_crypt.encrypt(user_to_updated["password"])
        return Response(status_code=200, content="User updated successfully")
    except:
        return HTTPException(status_code=404, detail="User not found")


@user.delete("/user/{id}", response_model=str, tags=["users"])
async def delete_user(id: str):
    try:
        user_entity(connection.local.user.find_one_and_delete({"_id": ObjectId(id)}))
        return Response(status_code=200, content="User deleted successfully")
    except:
        return HTTPException(status_code=404, detail="User not found")