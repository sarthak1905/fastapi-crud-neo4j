from . import users
from . import posts
from . import locations
from . import group_chats
from . import trends

routers = [
    users.router,
    posts.router,
    locations.router,
    group_chats.router,
    trends.router
]
