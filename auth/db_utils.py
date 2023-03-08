import aiosqlite
import uuid


async def make_connection(db):
    async with aiosqlite.connect(db) as db:
        return db


async def db_create_user_table(db):
    async with aiosqlite.connect(db) as db:
        await db.execute(f"""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id {str(uuid.uuid4())} NOT NULL,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            email TEXT NOT NULL """)
        await db.commit()


async def db_create_user(db, username, password, email):
    async with aiosqlite.connect(db) as db:
        await db.execute(f"""INSERT INTO users (username, password, email)
                            VALUES (?, ?, ?)""", (username, password, email))
        await db.commit()


async def db_update_user_password(db, username, password):
    async with aiosqlite.connect(db) as db:
        await db.execute(f"""UPDATE users SET password = ? WHERE username = ?""", (password, username))
        await db.commit()


async def db_delete_user(db, username):
    async with aiosqlite.connect(db) as db:
        await db.execute(f"""DELETE FROM users WHERE username = ?""", (username,))
        await db.commit()


async def db_get_user(db, username):
    async with aiosqlite.connect(db) as db:
        await db.execute(f"""SELECT * FROM users WHERE username = ?""", (username,))
        await db.commit()
