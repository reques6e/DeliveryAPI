import random

from fastapi.responses import JSONResponse
from fastapi import APIRouter

from database import DataBase
from utils import JSONBuildResponse

from point.models import PointStructure, PointCreate, PointUpdate

router = APIRouter(
    prefix='/point',
    tags=['Pickup point']
)

db = DataBase()

@router.get('/')
async def point_get(
    id: int
):
    point = await db.point_get(id)
    if point:
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message=f'Пункт выдачи с id {id}',
                point=point
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Пункт выдачи с id {id} не найден.',
                order=None
            ).json(),
            status_code=404
        ) 
    
@router.get('/all')
async def points_get():
    points = await db.points_get()
    if points:
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message='Все пункты выдачи.',
                point=points
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message='В данный момент нет ни одного пункта выдачи.',
                point=None
            ).json(),
            status_code=200
        )  

@router.post('/create')
async def point_create(
    data: PointCreate
):
    structure = PointStructure(
        id=random.randint(10000000, 99999999),
        name=data.name,
        description=data.description,
        city_id=data.city_id
    )
    if await db.city_get(data.city_id):
        if await db.point_create(structure):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=0,
                    message=f'Пункт выдачи {data.name} создан успешно',
                    point_id=structure.id
                ).json(),
                status_code=200
            )
        else:
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message=f'Создать пункт выдачи {data.name} не удалось.'
                ).json(),
                status_code=500
            )
    return JSONResponse(
        content=JSONBuildResponse(
            error=1,
            message=f'Город c id {data.city_id} не найден.'
        ).json(),
        status_code=404
    )

@router.put('/edit')
async def point_edit(
    data: PointUpdate
):
    if await db.point_get(data.id):
        if data.city_id:
            if await db.city_get(data.city_id):
                pass
            else:
                return JSONResponse(
                    content=JSONBuildResponse(
                        error=0,
                        message=f'Город с ID {data.city_id} не найден.'
                    ).json(),
                    status_code=404
                )

        if await db.point_update(data):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=0,
                    message=f'Пункт выдачи с ID {data.id} был обновлён.'
                ).json(),
                status_code=200
            )
        else:
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message=f'Произошла ошибка при обновлении пункта выдачи с ID {data.id}'
                ).json(),
                status_code=500
            )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Пункт выдачи с ID {data.id} не найден.'
            ).json(),
            status_code=404
        )


@router.delete('/delete')
async def point_delete(
    id: int
):
    """
    ```py 
    Обратите внимание

    При удалении пункта выдачи так же удаляются и другие привязанные к нему детали: Заказы
    ```

    """

    if await db.point_get(id):
        orders = await db.get_orders_by_point(id)
        if orders:
            for order in orders:
                await db.order_delete(order[0])

        if await db.point_delete(id):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=0,
                    message=f'Пункт выдачи успешно удалён.'
                ).json(),
                status_code=200
            )
        else:
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message=f'Не удалось удалить пункт выдачи.'
                ).json(),
                status_code=500
            )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message=f'Пункт выдачи не найден.'
            ).json(),
            status_code=404
        )