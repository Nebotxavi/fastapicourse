from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from . import models
from .database import engine 
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return {'message': "Hello world"}

# ---------------------
# --- DB CONNECTION ---
# ---------------------

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#         password='123123', cursor_factory=RealDictCursor )
#         cursor = conn.cursor()
#         print('Database connection was successfull')
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print('Error: ', error)
#         time.sleep(2)