from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
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