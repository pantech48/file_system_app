from urllib import request
from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, FastAPI, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import jwt
import datetime

from .database import get_db
from auth_app.utils import hash_sha256_password
from config.config_parser import config


app = FastAPI()
security = HTTPBasic()


@app.post('/user')
async def create_user(payload: schemas.User, db: Session = Depends(get_db)):
    """ This function is used to create a new user"""
    try:
        hashed_password = hash_sha256_password(payload.password)
        user = models.User(username=payload.username, password=hashed_password, email=payload.email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"uuid": user.id, "username": user.username, "email": user.email}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with username {payload.username} already exists")


@app.put('/user')
async def update_user_password(payload: schemas.User, db: Session = Depends(get_db)):
    """ This function is used to update a user password"""
    try:
        hashed_password = hash_sha256_password(payload.password)
        user = db.query(models.User).filter(models.User.username == payload.username).first()
        user.password = hashed_password
        db.commit()
        db.refresh(user)
        return {"username": user.username}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with username {payload.username} does not exist")


@app.delete('/user')
async def delete_user(payload: schemas.User, db: Session = Depends(get_db)):
    """ This function is used to delete a user """
    try:
        user = db.query(models.User).filter(models.User.username == payload.username).first()
        db.delete(user)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with username {payload.username} does not exist")


@app.get('/login')
async def login(payload: schemas.User,
                credentials: HTTPBasicCredentials = Depends(security),
                db: Session = Depends(get_db)):
    """ This function is used to log a user with username and password """
    try:
        user = db.query(models.User).filter(models.User.username == credentials.username).first()
        token = jwt.encode({"user_id": user.id,
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           config()["AUTH"]["secret_key"],
                           algorithm="HS256")
        return {"token": token}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with username {payload.username} does not exist")