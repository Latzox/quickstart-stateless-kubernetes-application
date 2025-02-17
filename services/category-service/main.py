from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Category Service")

class Category(BaseModel):
    name: str

categories_db = ["General", "Work", "Personal", "Shopping"]

@app.get("/categories/")
def list_categories():
    return categories_db

@app.post("/categories/")
def add_category(category: Category):
    categories_db.append(category.name)
    return {"message": f"Category '{category.name}' added"}
