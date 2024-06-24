import uvicorn

from fastapi import FastAPI
from config import Config

from info.router import router as router_info
from auth.router import router as router_auth
from cities.router import router as router_cities
from point.router import router as router_point

api = FastAPI(
    title='DeliveryAPI By Reques6e',
    version='0.1.0',
    redoc_url=None,
    description='DeliveryAPI - https://github.com/reques6e/DeliveryAPI'
)

api.include_router(router_auth)
api.include_router(router_cities)
api.include_router(router_point)
api.include_router(router_info)

if __name__ == "__main__":
    uvicorn.run(
        app='main:api', 
        host=Config.RUN_HOST, 
        port=Config.RUN_PORT,
        reload=Config.RUN_RELOAD
    )