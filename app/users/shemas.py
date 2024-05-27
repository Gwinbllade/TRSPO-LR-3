from pydantic import BaseModel, EmailStr
from typing import Optional



class SUserInfo(BaseModel):
    username: str
    email: EmailStr
    role: str
    class Config:
        orm_mode = True


class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    role: str

    class Config:
        orm_mode = True


class SUserAuth(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class SUserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class SUserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
