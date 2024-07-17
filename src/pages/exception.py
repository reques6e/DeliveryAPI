from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from utils import JSONBuildResponse

class FastAPIExceptionHandlers:
    def __init__(self, app: FastAPI):
        self.app = app
        self.register_handlers()

    def register_handlers(self):
        @self.app.exception_handler(404)
        async def custom_404_handler(request: Request, exc):
            return JSONResponse(
                content=JSONBuildResponse(
                    error=1,
                    message='Страница не найдена'
                ).json()
            )