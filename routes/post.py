from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Response
from schemas.post import post_entity, posts_entity
from models.post import Post
from config.db import connection


post = APIRouter()



@post.get("/posts", response_model=list, tags=["posts"])
async def get_all_posts() -> list:
    try:
        posts = posts_entity(connection.local.post.find())
        return posts
    except:
        return HTTPException(status_code=404, detail="There are no posts for the moment")



@post.post("/post/new", response_model=str, tags=["posts"])
async def create_post(post: Post, user_id: str):
    try:
        new_post = dict(post)
        user_owner = connection.local.user.find_one({"_id": ObjectId(user_id)})
        user_owner["_id"] = str(user_owner["_id"])
        new_post["author_id"] = user_owner
        print(new_post)
        connection.local.post.insert_one(new_post).inserted_id
        post_entity(new_post)
        return Response(status_code=201, content="Post created successfully")
    except:
        return HTTPException(status_code=400, detail="Somenthing went wrong, try it again later")
    


@post.get("/post/{id}", response_model=Post, tags=["posts"])
async def get_single_post(id: str):
   try:
       post = connection.local.post.find_one({"_id": ObjectId(id)})
       return post
   except:
    return HTTPException(status_code=404, detail="Post not found")



@post.delete("/post/{id}", response_model=str, tags=["posts"])
async def delete_post(id: str):
    try:
        connection.local.post.find_one_and_delete({"_id": ObjectId(id)})
        return Response(status_code=200, content="Post deleted successfully")
    except:
        return HTTPException(status_code=404, detail="Post not found")
    
            
    
@post.put("/post/{id}")
async def uptaded_post(id: str, post_data: Post, user_id: Optional[str] = None):
    post_dict = dict(post_data)
    try: 
        if user_id == None:
            post = connection.local.post.find_one({"_id": ObjectId(id)})
            post_dict["author_id"] = post["author_id"] if post["author_id"] != None else { "name": "No author" }
            connection.local.post.find_one_and_update({"_id": ObjectId(id)}, {"$set": post_dict})
            return Response(status_code=200, content="Post uptaded successfully")
        else:
            user_to_relate = connection.local.user.find_one({"_id": ObjectId(user_id)})
            post_dict["author_id"] = user_to_relate
            connection.local.post.find_one_and_update({"_id": ObjectId(id)}, {"$set": post_dict})
            return Response(status_code=200, content="Post uptaded successfully")
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail="Post not found")
    