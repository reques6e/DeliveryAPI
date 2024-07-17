from pydantic import BaseModel
from typing import Optional


class PointStructure(BaseModel):
    id: int
    name: str
    description: str
    city_id: int

class PointCreate(BaseModel):
    name: str
    description: str
    city_id: int

class PointUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    city_id: Optional[int] = None