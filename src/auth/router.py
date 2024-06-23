import time
import random
import uuid

from fastapi.responses import JSONResponse
from fastapi import APIRouter

from auth.manager import UserManager
from auth.models import UserStructure, UserCreate

from utils import JSONBuildResponse

router = APIRouter(
    prefix='/account',
    tags=['Account']
)


@router.get('/info')
async def info(
    id: int
):
    rs = await UserManager().user_info(id)
    if rs:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message='Информация о пользователе.',
                id=rs.id,
                username=rs.username,
                age=rs.age,
                block=rs.block,
                user_group=rs.user_group,
                city=rs.city,
                address=rs.address,
                phone=rs.phone,
                reg_date=rs.reg_date,
                passport=rs.passport,
                token=rs.token
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message='Я не смог найти пользователя с user id {}.'.format(id)
            ).json(),
            status_code=404
        )        

@router.post('/create')
async def create(
    data: UserCreate
):
    structure = UserStructure(
        id=random.randint(10000000, 99999999),
        username=data.username,
        age=data.age,
        password=data.password,
        block=0,
        user_group='user',
        city=data.city,
        address=data.address,
        phone=data.phone,
        reg_date=int(time.time()),
        passport=None,
        token=UserManager.jwt_generate({'sjskasdklasd': f'{uuid.uuid4()}', 'password': f'{data.password}', 'gdfghdfasd': f'{uuid.uuid4()}'})
    )
    if await UserManager().user_create(structure):
        return JSONResponse(
            content=JSONBuildResponse(
                error=0,
                message='Создал нового пользователя.',
                id=structure.id,
                username=structure.username,
                age=structure.age,
                block=structure.block,
                user_group=structure.user_group,
                city=structure.city,
                address=structure.address,
                phone=structure.phone,
                reg_date=structure.reg_date,
                passport=structure.passport,
                token=structure.token
            ).json(),
            status_code=200
        )
    else:
        return JSONResponse(
            content=JSONBuildResponse(
                error=1,
                message='Создать пользователя не удалось.'
            ).json(),
            status_code=500
        )

@router.put('/edit')
async def info(
    id: int
):
    # TODO update
    ...


@router.delete('/delete')
async def info(
    id: int
):
    if await UserManager().user_info(id):
        if await UserManager().user_delete(id):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=0,
                    message='Пользователь удалён'
                ).json(),
                status_code=200
            ) 
        else:
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message='Не удалось удалить пользователя'
                ).json(),
                status_code=500
            ) 
    else:
        return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message='Пользователь не найден'
                ).json(),
                status_code=404
            ) 