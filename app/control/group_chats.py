from fastapi import APIRouter, HTTPException
from ..models import GroupChat, User
from ..dtos import GroupChatDto

import uuid, json

router = APIRouter(prefix= '/groups')

def get_payload(group):
    group_payload = {"group_id": group.group_id,
                     "members": group.members,
                     "no_of_members": len(group.members)}
    return group_payload


@router.get("/list")
async def list_groups():
    return [json.dumps(group.__properties__) for group in GroupChat.nodes.all()]


@router.post("/create")
async def create_group():
    group_new = GroupChat(group_id=uuid.uuid4()).save()

    group_payload = get_payload(group_new)

    return group_payload

@router.put("/add_member/{group_id}/{username}")
async def add_member(group_id: str, username: str):
    group_exists = GroupChat.nodes.get_or_none(group_id=group_id)
    user_exists = User.nodes.get_or_none(username=username)
    if user_exists is None or group_exists is None:
        raise HTTPException(status_code=400, detail="INVALID_INFORMATION")

    group_exists.membership.connect(user_exists)
    group_exists.members.append(user_exists.username)

    group_exists.save()

    return {}

@router.delete("/delete/{group_id}")
async def delete_group(group_id: str):
    group_exists = GroupChat.nodes.get_or_none(group_id=group_id)
    if user_exists is None:
        raise HTTPException(status_code=400, detail="INVALID_INFORMATION")

    group_exists.delete()

    return {}