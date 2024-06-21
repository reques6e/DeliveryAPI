from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: int
    age: int
    password: int
    admin: Optional[int] = 0
    block: Optional[int] = 0
    group: str
    city: int
    address: str
    phone: int
    reg_date: int
    passport: Optional[str] = None