import sqlite3
import contextlib

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings, env_file="users/.env", extra="ignore"):
    database: str
    logging_config: str

def get_db():
    with contextlib.closing(sqlite3.connect(settings.database)) as db:
        db.row_factory = sqlite3.Row
        yield db

settings = Settings()
app = FastAPI()

@app.post("/register")
def register_user(db: sqlite3.Connection = Depends(get_db)):
    return {}

@app.post("/login")
def login(db: sqlite3.Connection = Depends(get_db)):
    return {}

@app.get("/checkpwd/{userName}")
def login(userName: str, db: sqlite3.Connection = Depends(get_db)):
    return {}