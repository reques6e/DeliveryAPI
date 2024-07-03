import random

from fastapi.responses import JSONResponse
from fastapi import APIRouter

from database import DataBase
from utils import JSONBuildResponse

from city.models import CityStructure, CityCreate, CityUpdate


router = APIRouter(
    prefix='/city',
    tags=['City']
)

db = DataBase()

@router.get('/')
async def city_get(
    id: int
):
    city = await db.city_get(id)
    if city:
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message=f'Город с id {id}',
                city=city
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Город с id {id} не найден.',
                city=None
            ).json(),
            status_code=404
        ) 

@router.get('/all')
async def cities_get():
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
            status_code=404
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
                message=f'Город {data.name} создан успешно',
                id=structure.id
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

@router.put('/edit')
async def city_edit(
    data: CityUpdate
):
    if await db.city_get(data.id):
        if await db.city_update(data):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=0,
                    message=f'Город с ID {data.id} был обновлён.'
                ).json(),
                status_code=200
            )
        else:
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message=f'Произошла ошибка при обновлении города с ID {data.id}'
                ).json(),
                status_code=500
            )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Город с ID {data.id} не найден.'
            ).json(),
            status_code=404
        )

@router.delete('/delete')
async def city_delete(
    id: int
):
    """
    ```py 
    Обратите внимание

    При удалении города так же удаляются и другие привязанные к нему детали: Пункты выдачи, заказы и т.д
    ```

    """

    if await db.city_get(id):
        points = await db.find_point_by_city(id)
        if points:
            for point in points:
                await db.point_delete(point[0])
        
        users = await db.get_users_by_city(id)
        if users:
            await db.update_city_in_users(
                old_city_id=id,
                new_city_id=0
            )

        orders = await db.get_orders_by_city(id)
        if orders:
            for order in orders:
                await db.order_delete(order[0])

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