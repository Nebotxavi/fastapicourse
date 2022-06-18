from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import models
from .database import engine, get_db 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# -----------------
# --- MODEL -------
# -----------------

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None #

# ---------------------
# --- DB CONNECTION ---
# ---------------------

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='123123', cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print('Database connection was successfull')
        break
    except Exception as error:
        print("Connecting to database failed")
        print('Error: ', error)
        time.sleep(2)



my_posts = [
     {
        "title": "top beaches in Oropesa",
        "content": "check out these awesome beaches",
        "published": False,
        "rating": 4,
        "id": 1
    },
     {
        "title": "top beaches in Castello",
        "content": "check out these awesome beaches",
        "published": False,
        "rating": 4,
        "id": 2
    },
]
# -----------------
# --- FUNCTIONS ---
# -----------------

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
# Use case: post = find(lambda item: item['id'] == id, my_posts)

# -----------------
# --- ENDPOINTS ---
# -----------------

@app.get('/')
async def root():
    cursor.execute(""" SELECT * FROM posts """)
    return cursor.fetchall()

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # return cursor.fetchall()
    posts = db.query(models.Post).all()
    return {'data': posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    # (post.title, post.content, post.published) )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'data': new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")

    return {'post_detail': post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING *""", (str(id)) )
    # deleted_post = cursor.fetchone()
    # conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s WHERE id = %s RETURNING *""", ( post.title, post.content, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")

    return {'data': updated_post}


