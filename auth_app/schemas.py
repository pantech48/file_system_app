from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True
