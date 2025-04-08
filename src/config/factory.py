""" WebApp Setup. """
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse

from config.di import DI
from config.exception import GeneralException
from domain.todo.controllers.auth import AuthController
from domain.todo.controllers.todo_controller import TODOController


@asynccontextmanager
async def lifespan(_: FastAPI):
    dependencies = DI()
    dependencies.database_driver().setup_database()
    yield


def create_app() -> FastAPI:
    app_ = FastAPI(title="TODO List API", lifespan=lifespan)
    app_.include_router(
        TODOController(
            router=APIRouter(
                prefix="/todo",
                tags=["TODO List"]
            )
        ).router
    )
    app_.include_router(
        AuthController(
            router=APIRouter(
                prefix="/token",
                tags=["Auth Token"]
            )
        ).router
    )
    return app_


app = create_app()


@app.middleware("http")
async def check_auth_header(request: Request, call_next):
    if request.url.path == "/todo":
        if not request.headers.get("Authorization"):
            return JSONResponse(content={"error": "Missing Authorization header"}, status_code=status.HTTP_401_UNAUTHORIZED)

    response = await call_next(request)
    return response


@app.exception_handler(GeneralException)
def general_exception_handler(request: Request, exc: GeneralException): # noqa
    return JSONResponse(
        content=exc.content,
        status_code=exc.status_code
    )

