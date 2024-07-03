from pydantic import BaseModel
from typing import Optional


class OrderStructure(BaseModel):
    id: int
    city_id: int
    point_id: int
    description: str
    img: str
    date: int
    active: int

class OrderCreate(BaseModel):
    city_id: int
    point_id: int
    description: str
    img: str

class OrderUpdate(BaseModel):
    id: int
    city_id: Optional[int] = None
    point_id: Optional[int] = None
    description: Optional[str] = None
    img: Optional[str] = None
    active: Optional[int] = None