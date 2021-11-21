from pydantic import BaseModel, constr, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: constr(min_length=3, max_length=50)
    email: EmailStr
    #is_active: Optional[bool]


class UserCreate(UserBase):
    password: constr(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserDelete(UserLogin):
    pass


class UserUpdateAttr(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]


class UserUpdate(UserLogin):
    user: UserUpdateAttr


class User(UserBase):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

