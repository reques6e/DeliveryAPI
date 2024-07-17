import asyncio
import uvicorn

from fastapi import FastAPI
from config import Config
from database import DataBase

from pages.exception import FastAPIExceptionHandlers

from pages.info.router import router as router_info
from pages.auth.router import router as router_auth
from pages.city.router import router as router_cities
from pages.point.router import router as router_points
from pages.order.router import router as router_orders

api = FastAPI(
    title='DeliveryAPI By Reques6e',
    version='0.1.0',
    redoc_url=None,
    description='DeliveryAPI - https://github.com/reques6e/DeliveryAPI'
)

db = DataBase()

FastAPIExceptionHandlers(api)

api.include_router(router_auth)
api.include_router(router_cities)
api.include_router(router_points)
api.include_router(router_orders)
api.include_router(router_info)

if __name__ == "__main__":
    asyncio.run(db.table_create())

    uvicorn.run(
        app='main:api', 
        host=Config.RUN_HOST, 
        port=Config.RUN_PORT,
        reload=Config.RUN_RELOAD
    )