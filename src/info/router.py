from fastapi.responses import JSONResponse
from fastapi import APIRouter

from utils import JSONBuildResponse

router = APIRouter(
    prefix='/info',
    tags=['Info']
)


@router.get('/')
async def info():
    return JSONResponse(
        content=JSONBuildResponse(
            error=0,
            message=''
        ),
        status_code=200
    )