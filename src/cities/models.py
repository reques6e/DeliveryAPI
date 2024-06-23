from pydantic import BaseModel

class CityStructure(BaseModel):
    id: int
    name: str
    description: str

class CityCreate(BaseModel):
    name: str
    description: str