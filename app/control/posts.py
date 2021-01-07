from fastapi import APIRouter, HTTPException
from ..models import Post, User
from ..dtos import PostDto

import uuid

router = APIRouter(prefix= '/post')

def get_payload(post):
    post_payload = {"post_id": post.post_id,
                    "author": post.author,
                    "has_media": post.has_media,
                    "content": post.content,
                    "likes": post.likes,
                    "comments": post.comments,
                    "shares": post.shares}
    return post_payload


@router.get("/list")
async def list_posts():
    posts = []
    for post in Post.nodes.all():
        post_payload = get_payload()
        posts.append(post_payload)
    return posts


@router.post("/create")
async def create_post(post: PostDto):
    author_exists = User.nodes.get_or_none(username= post.author)
    if author_exists is None:
        raise HTTPException(status_code=404, detail="AUTHOR_NOT_FOUND")

    post_new = Post(post_id = uuid.uuid4(),
                    has_media = post.has_media, 
                    content = post.content, 
                    likes = post.likes, 
                    comments  = post.comments,
                    shares = post.shares).save()
    
    post_new.author.connect(post.author)
    post_payload = get_payload(post_new)
    return {"post": post_payload}


@router.put("/update")
async def update_post(post: PostDto, id: int):
    post_exists = Post.nodes.get_or_none(id= id)
    if post_exists is None:
        raise HTTPException(status=404, detail="POST_NOT_FOUND")
    
    post_exists = Post(has_media = post.has_media, 
                    content = post.content, 
                    likes = post.likes, 
                    comments  = post.comments,
                    shares = post.shares).save()
    
    post_exists.author.connect(post.author)
    
    post_payload = get_payload(post_exists)

    return {"post" : post_payload}


@router.delete("/delete")
async def delete_post(id: int):
    post_exists = Post.nodes.get_or_none(id = id)
    if post_exists is None:
        raise HTTPException(status= 404, detail="POST_NOT_FOUND")
    
    post_exists.delete()

    return {}