from pydantic import BaseModel

class PointStructure(BaseModel):
    id: int
    name: str
    description: str
    city_id: int

class PointCreate(BaseModel):
    name: str
    description: str
    city_id: int