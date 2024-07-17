from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    age: int
    phone: int
    city: int
    address: str
    password: str

class UserStructure(BaseModel):
    id: int
    username: str
    age: int
    password: str
    admin: Optional[int] = 0
    block: Optional[int] = 0
    user_group: str 
    city: int
    address: str
    phone: int
    reg_date: int
    passport: Optional[str] = None
    token: str

class UserAuth(BaseModel):
    phone: int
    password: str

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    age: Optional[int] = None
    password: Optional[str] = None
    admin: Optional[int] = 0
    block: Optional[int] = 0
    user_group: Optional[str]  = None
    city: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[int] = None
    passport: Optional[str] = None
