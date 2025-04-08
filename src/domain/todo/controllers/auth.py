import jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from domain.common.controller.base import BaseController


class AuthController(BaseController):

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    jwt_sign_secret = "secret"
    jwt_sign_alg = "HS256"

    _mocked_users = {
        "teste1": "teste1",
        "teste2": "teste2"
    }

    def __init__(self, *, router: APIRouter):
        super().__init__(router=router)

        self.router.add_api_route(
            "",
            self._get_token,
            methods=["POST"],
            description=f"Available users and its passwords: `{self._mocked_users}`"
        )


    def _get_token(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        if (
            not self._mocked_users.get(form_data.username) or
            form_data.password != self._mocked_users.get(form_data.username)
        ):
            return JSONResponse(
                content={"error": "Incorrect username or password"},
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        access_token = jwt.encode({"sub": form_data.username}, self.jwt_sign_secret, self.jwt_sign_alg)
        return JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "bearer"
            }
        )
