import random

from fastapi.responses import JSONResponse
from fastapi import APIRouter

from database import DataBase
from utils import JSONBuildResponse

from cities.models import CityStructure, CityCreate

router = APIRouter(
    prefix='/point',
    tags=['Pickup point']
)

db = DataBase()

@router.get('/')
async def point_get(
    id: int
):
    # TODO update
    ...

