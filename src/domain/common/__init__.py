""" Commons python objects used by other domains. """
import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from starlette import status
from typing_extensions import Annotated

from config.exception import GeneralException
from domain.todo.controllers.auth import AuthController


def get_request_user(token: Annotated[str, Depends(AuthController.oauth2_scheme)]):
    try:
        jwt_claims = jwt.decode(token, AuthController.jwt_sign_secret, AuthController.jwt_sign_alg)
    except InvalidTokenError:
        raise GeneralException(
            content="Invalid JWT",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    username = jwt_claims["sub"]
    return username
