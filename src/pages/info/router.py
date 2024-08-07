from fastapi.responses import JSONResponse
from fastapi import APIRouter


router = APIRouter(
    prefix='/info',
    tags=['Info']
)


@router.get('/')
async def info():
    return JSONResponse(
        content={'1': '2'},
        status_code=200
    )