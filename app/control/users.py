from fastapi import APIRouter, HTTPException
from ..models import User, Location
from ..dtos import UserDto, LocationDto


router = APIRouter(prefix= '/user')

def get_payload(user):
    user_payload = {"first_name": user.first_name,
                    "last_name": user.last_name,
                    "ph_number": user.ph_number,
                    "username": user.username}
    return user_payload


@router.get("/list")
async def list_users():
    #users =[]
    #for user in User.nodes.all():
    #    user_payload = get_payload(user)
    #    users.append(user_payload)
    #return users
    return [user.to_json() for user in User.nodes.all()]


@router.get("/{username}")
async def get_user(username: str):
    user = User.nodes.get_or_none(username = username)
    if user is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    return user


@router.post("/create")
async def create_user(user: UserDto):
    user_exists = User.nodes.get_or_none(username = user.username)
    if user_exists:
        raise HTTPException(status_code=400, detail="USERNAME_TAKEN")
    
    user_exists = User(first_name = user.first_name, 
                        last_name = user.last_name, 
                        ph_number = user.ph_number, 
                        username  = user.username).save()
    
    user_payload = get_payload(user)
    return {"user": user_payload}


@router.put("/update/{username}")
async def update_user(user: UserDto):
    user_exists = User.nodes.get_or_none(username= user.username)
    
    if user_exists is None:
        raise HTTPException(status=400, detail="NO_SUCH_USER")

    user_exists = User(first_name= user.first_name,
                        last_name= user.last_name,
                        ph_number= user.ph_number,
                        username= user.username).save()
    
    user_payload = get_payload(user)

    return {"user": user_payload}

@router.put("/{username}/add_location")
async def add_location(username: str, location: LocationDto):
    user_exists = User.nodes.get_or_none(username=username)
    if user_exists is None:
        raise HTTPException(status=404, detail="USER_NOT_FOUND")
    location_exists = Location.nodes.get_or_none(city=location.city,
                                                 country=location.country,
                                                 zip_code=location.zip_code)
    if location_exists is None:
        location_exists = Location(city=location.city,
                                   country=location.country,
                                   zip_code=location.zip_code).save()

    user_exists.residence.connect(location_exists)

    return {}

@router.put("/{username}/add_friend")
async def add_friend(username: str, friend: str):
    if username == friend:
        raise HTTPException(status=400, detail="SAME_USERNAME")
    
    user_exists = User.nodes.get_or_none(username= username)
    friend_exists = User.nodes.get_or_none(username= friend)

    if user_exists is None or friend_exists is None:
        raise HTTPException(status= 400, detail="USERNAME_INVALID")

    user_exists.friend.connect(friend_exists)

    return {}


@router.delete("/delete/{username}")
async def delete_user(username: str):
    user_exists = User.nodes.get_or_none(username= username)
    if user_exists is None:
        raise HTTPException(status=404, detail="USER_NOT_FOUND")
    
    user_exists.delete()
    return {}