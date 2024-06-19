import uvicorn

from fastapi import FastAPI
from config import Config
from info.router import router as router_info


api = FastAPI(
    title='DeliveryAPI By Reques6e',
    version='0.1.0',
    redoc_url=None,
)

api.include_router(router_info)


if __name__ == "__main__":
    uvicorn.run(
        app='main:api', 
        host=Config.RUN_HOST, 
        port=Config.RUN_PORT,
        reload=Config.RUN_RELOAD
    )