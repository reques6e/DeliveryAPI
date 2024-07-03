import random
import time

from fastapi.responses import JSONResponse
from fastapi import APIRouter

from database import DataBase
from utils import JSONBuildResponse

from order.models import OrderStructure, OrderCreate, OrderUpdate

router = APIRouter(
    prefix='/order',
    tags=['Order']
)

db = DataBase()

@router.get('/')
async def order(
    id: int
):
    order = await db.order_get(id)
    if order:
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message=f'Заказ с id {id}',
                order=order
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Заказ с id {id} не найден.',
                order=None
            ).json(),
            status_code=404
        ) 
    
@router.get('/all')
async def orders():
    orders = await db.orders_get()
    if orders:
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message='Все заказы.',
                orders=orders
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message='В данный момент нет ни одного заказа.',
                order=None
            ).json(),
            status_code=404
        ) 

@router.post('/create')
async def order_create(
    data: OrderCreate
):
    if await db.city_get(data.city_id):
        pass
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Город с id {data.city_id} не найден.'
            ).json(),
            status_code=404
        )

    if await db.point_get(data.point_id):
        pass
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Пункт выдачи с id {data.point_id} не найден.'
            ).json(),
            status_code=404
        )
    
    structure = OrderStructure(
        id=random.randint(10000000, 99999999),
        city_id=data.city_id,
        point_id=data.point_id,
        description=data.description,
        img=data.img,
        date=int(time.time()),
        active=1
    )
    if await db.order_create(structure):
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message=f'Заказ с ID {structure.id} создан успешно',
                order_id=structure.id
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Заказ с ID {data.id} не удалось.'
            ).json(),
            status_code=500
        )

@router.put('/edit')
async def order_edit(
    data: OrderUpdate
):
    if await db.orders_get(data.id):
        if await db.order_update(data):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=0,
                    message=f'Заказ с ID {data.id} был обновлён.'
                ).json(),
                status_code=200
            )
        else:
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message=f'Произошла ошибка при обновлении заказа с ID {data.id}'
                ).json(),
                status_code=500
            )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'заказ с ID {data.id} не найден.'
            ).json(),
            status_code=404
        )

@router.delete('/delete')
async def order_delete(
    id: int
):
    if await db.order_get(id):
        if await db.order_delete(id):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=0,
                    message='Заказ удалён'
                ).json(),
                status_code=200
            ) 
        else:
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message='Не удалось удалить заказ'
                ).json(),
                status_code=500
            ) 
    else:
        return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message='Заказ не найден'
                ).json(),
                status_code=404
            ) 