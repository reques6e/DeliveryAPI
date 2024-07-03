from pydantic import BaseModel
from typing import Optional


class CityStructure(BaseModel):
    id: int
    name: str
    description: str

class CityCreate(BaseModel):
    name: str
    description: str

class CityUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None