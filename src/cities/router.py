import random

from fastapi.responses import JSONResponse
from fastapi import APIRouter

from database import DataBase
from utils import JSONBuildResponse

from cities.models import CityStructure, CityCreate

router = APIRouter(
    prefix='/cities',
    tags=['Cities']
)

db = DataBase()

@router.get('/')
async def cities():
    cities = await db.cities_get()
    if cities:
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message='Все города.',
                cities=cities
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message='В данный момент нет ни одного города.',
                cities=None
            ).json(),
            status_code=200
        )       

@router.post('/create')
async def city_create(
    data: CityCreate
):
    structure = CityStructure(
        id=random.randint(10000000, 99999999),
        name=data.name,
        description=data.description
    )
    if await db.city_create(structure):
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message=f'Город {data.name} создан успешно'
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Создать город {data.name} не удалось.'
            ).json(),
            status_code=500
        )
    
@router.delete('/delete')
async def city_create(
    id: int
):
    if await db.city_get(id):
        if await db.city_delete(id):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=0,
                    message=f'Город успешно удалён.'
                ).json(),
                status_code=200
            )
        else:
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message=f'Не удалось удалить город.'
                ).json(),
                status_code=500
            )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Город не найден.'
            ).json(),
            status_code=404
        )