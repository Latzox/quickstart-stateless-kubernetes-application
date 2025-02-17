from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="User Service")

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

users_db = []

@app.post("/users/register", response_model=User)
def register_user(user: User):
    users_db.append(user)
    return user

@app.get("/users/list")
def list_users():
    return users_db
