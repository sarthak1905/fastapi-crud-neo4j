from pydantic import BaseModel

class UserDto(BaseModel):
    first_name: str
    last_name: str
    ph_number: str
    username: str

class PostDto(BaseModel):
    author: str
    has_media: bool
    content: str
    likes: int
    comments: list
    shares: int

class LocationDto(BaseModel):
    city: str
    country: str
    zip_code: int

class GroupChatDto(BaseModel):
    members: list