import sqlite3
import contextlib

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings

import base64
import hashlib
import secrets
import json
from datetime import datetime, timedelta
import os 
import sys
#from jose import JWTError, jwt

ALGORITHM = "pbkdf2_sha256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings(BaseSettings, env_file="users/.env", extra="ignore"):
    database: str
    logging_config: str

class User(BaseModel):
    username : str
    password : str
    roles : List[str]


def get_db():
    with contextlib.closing(sqlite3.connect(settings.database)) as db:
        db.row_factory = sqlite3.Row
        yield db

settings = Settings()
app = FastAPI()

# given 260000 - modified to 600000 based on research
def get_hashed_pwd(password, salt=None, iterations=600000):
    if salt is None:
        salt = secrets.token_hex(16)
    assert salt and isinstance(salt, str) and "$" not in salt
    assert isinstance(password, str)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
    return "{}${}${}${}".format(ALGORITHM, iterations, salt, b64_hash)


def verify_password(password, password_hash):
    if (password_hash or "").count("$") != 3:
        return False
    algorithm, iterations, salt, b64_hash = password_hash.split("$", 3)
    iterations = int(iterations)
    assert algorithm == ALGORITHM
    compare_hash = get_hashed_pwd(password, salt, iterations)
    return secrets.compare_digest(password_hash, compare_hash)

'''def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt'''

def expiration_in(minutes):
    creation = datetime.datetime.now(tz=datetime.timezone.utc)
    expiration = creation + datetime.timedelta(minutes=minutes)
    return creation, expiration


def generate_claims(username, user_id, roles):
    _, exp = expiration_in(20)

    claims = {
        "aud": "krakend.local.gd",
        "iss": "auth.local.gd",
        "sub": username,
        "jti": str(user_id),
        "roles": roles,
        "exp": int(exp.timestamp()),
    }
    '''token = {
        "access_token": claims,
        "refresh_token": claims,
        "exp": int(exp.timestamp()),
    }'''

    output = json.dumps(claims, indent=4)
    return output

@app.post("/register")
def register_user(user_data: User, db: sqlite3.Connection = Depends(get_db)):
    """Register a new user."""
    username = user_data.username
    userpwd = user_data.password
    roles = [role.strip() for role in user_data.roles.split(",")]

    # check that the username is not already taken
    user_exists = db.execute(f"SELECT * FROM Registrations WHERE username = ?",(username,)).fetchone()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already used, try a new username")

    # create new user
    hashed_pwd = get_hashed_pwd(userpwd)
    cursor = db.execute(f"INSERT INTO Registrations (Username, UserPassword) VALUES  (?,?)", (username, hashed_pwd))
    user_id =  cursor.lastrowid #db.execute("SELECT UserId from Registrations ORDER BY UserId DESC LIMIT 1").fetchone()[0]

    for role in roles:
        db.execute(f"INSERT INTO Roles (Rolename) VALUES ()", (role,))
        role_id = db.execute("SELECT RoleId from Roles ORDER BY RoleId DESC LIMIT 1").fetchone()[0]
        db.execute("INSERT INTO UserRoles (RoleId, UserId) VALUES (?, ?)", (role_id, user_id))
    db.commit()
    return {"status" : "200 OK","message": f"User {username} successfully registered with role {roles}."}

@app.post("/login")
def login(user_data: User, db: sqlite3.Connection = Depends(get_db)):
    """Login an existing user and generate JWT token for future requests."""
    username = user_data.username
    userpwd = user_data.password
    userrole = user_data.roles

    user_verify = db.execute(f"SELECT * FROM Registrations WHERE username = ?",(username,)).fetchone()[0]

    if user_verify is None or not verify_password(userpwd, user_verify[2]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    roles = db.execute(f"SELECT roles.rolename FROM roles JOIN userroles ON roles.roleid = userroles.roleid WHERE userroles.user_id=?",(user_verify[0],)).fetchall()
    roles = [row[0] for row in roles]
    if userrole not in roles:
        raise HTTPException(status_code=400, detail="Role not registered for the given user") 
    
    '''token_expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires=token_expiry)
    db.execute(f"UPDATE Registrations SET BearerToken = ? WHERE username = ?",(access_token, username))
    db.commit()'''

    # if successful, then return JWT Claims
    jwt_claims = generate_claims(username, user_verify[0], roles)
    # sign this jwt_claim in krakend config
    return {jwt_claims}

@app.get("/checkpwd")
def checkpwd(user_data: User, db: sqlite3.Connection = Depends(get_db)):
    """Check if the password is correct or not."""
    username = user_data.username
    userpwd = user_data.password
    user_verify = db.execute(f"SELECT * FROM Registrations WHERE username = ?",(username,)).fetchone()[0]

    if user_verify is None or not verify_password(userpwd, user_verify[2]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"status" : "200 OK"}