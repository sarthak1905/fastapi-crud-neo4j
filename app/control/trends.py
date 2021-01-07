from fastapi import APIRouter, HTTPException
from ..models import Trending, Post
from ..dtos import GroupChatDto

import uuid

router = APIRouter(prefix= '/trends')

def get_payload(trend):
    trend_payload = {"trend_id": trend.trend_id,
                     "likes": trend.likes,
                     "comments": trend.comments,
                     "shares": trend.shares}
    return trend_payload

@router.get("/list")
async def list_trends():
    trends=[]
    for trend in Trending.nodes.all():
        trend_payload = get_payload(trend)
        trends.append(trend_payload)
    return trends

@router.post("/create")
async def create_trend(post_id: str):
    post_exists = Post.nodes.get_or_none(post_id=post_id)
    if post_exists is None:
        raise HTTPException(status_code=404, detail="POST_DOES_NOT_EXIST")

    trend_new = Trend(trend_id=uuid.uuid4(), 
                      likes=len(post_exists.likes),
                      comments=len(post_exists.comments),
                      shares=len(post_exists.shares)).save()
    
    trend_new.popular.connect(post_exists)

    trend_payload = get_payload(trend_new)

    return trend_payload


@router.delete("/delete/{trend_id}")
async def delete_trend(trend_id: str):
    trend_exists = Trend.nodes.get_or_none(trend_id=trend_id)
    if trend_exists is None:
        raise HTTPException(status_code=404, detail="TREND_DOES_NOT_EXIST")

    trend_exists.delete()

    return {}
