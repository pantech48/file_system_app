from fastapi import FastAPI, HTTPException
import aiosqlite

from auth_app.db_utils import db_create_user_table, db_create_user, db_update_user_password, db_delete_user, db_get_user, \
    make_connection
from auth_app.utils import hash_sha256_password


app = FastAPI()
db_name = "auth_app.db"

db_create_user_table(db_name)


@app.post("/user")
async def create_user(username: str, password: str, email: str):
    async with aiosqlite.connect(db_name) as db:
        existing_user = await db_get_user(db, username)
        if await existing_user.fetchone():
            raise HTTPException(status_code=400, detail="Choose another username, this username already exists")

        hashed_password = hash_sha256_password(password)
        await db_create_user(db, username, hashed_password, email)
        return {"username": username, "email": email}


@app.put("/user")
async def update_user_password(username: str, password: str):
    async with aiosqlite.connect(db_name) as db:
        hashed_password = hash_sha256_password(password)
        await db_update_user_password(db, username, hashed_password)
        return {"username": username}


@app.delete("/user")
async def delete_user(username: str):
    async with aiosqlite.connect(db_name) as db:
        await db_delete_user(db, username)
        return {"username": username}


@app.get("/user")
async def get_user(username: str):
    async with aiosqlite.connect(db_name) as db:
        user = await db_get_user(db, username)
        return await user.fetchone()


