from neomodel import config 
from app import app
import uvicorn

print("Starting database...")
config.DATABASE_URL = 'bolt://neo4j:1234@127.0.0.1:7687'

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)