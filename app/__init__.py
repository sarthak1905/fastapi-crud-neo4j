from fastapi import FastAPI

from app import models
from app.control import routers

app = FastAPI()

@app.get('/')
async def index():
    return {'Hello': 'Welcome!'}

for router in routers:
    app.include_router(router)