from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path
from pydantic import WithJsonSchema
from starlette import status
from typing_extensions import Annotated, List

from config.di import DI
from config.exception import GeneralException
from domain.common import get_request_user
from domain.common.controller.base import BaseController
from domain.common.controller.docs.additional_responses import (
    HTTP_500_STATUS_CODE_RESPONSE as RESPONSE_500
)
from domain.todo.controllers.schemas.request.todo_schema_request import TODOCreateRequest, TODOUpdateRequest
from domain.todo.controllers.schemas.response.todo_schema_response import (
    TODOCreateResponse,
    TODOUpdateResponse,
    TODOReadResponse
)
from domain.todo.enums import ExceptionErrorMsgs
from domain.todo.services.todo_service import TODOService


class TODOController(BaseController):

    def __init__(self, *, router: APIRouter):
        super().__init__(router=router)

        self.router.add_api_route(
            "",
            self._create_todo,
            response_model=TODOCreateResponse,
            methods=["POST"],
            responses={status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500}
        )

        self.router.add_api_route(
            "/{id_}",
            self._update_todo,
            methods=["PATCH"],
            response_model=TODOUpdateResponse,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                GeneralException.CONTENT_PREFIX:
                                    ExceptionErrorMsgs.TODO_NOT_FOUND
                            }
                        }
                    },
                }
            }
        )

        self.router.add_api_route(
            "/{id_}",
            self._delete_todo,
            methods=["DELETE"],
            response_model=Annotated[None, WithJsonSchema(json_schema={"type": "null"})],
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                GeneralException.CONTENT_PREFIX:
                                    ExceptionErrorMsgs.TODO_NOT_FOUND
                            }
                        }
                    },
                }
            }
        )

        self.router.add_api_route(
            "",
            self._read_todo,
            methods=["GET"],
            response_model=List[TODOReadResponse],
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                GeneralException.CONTENT_PREFIX:
                                    ExceptionErrorMsgs.NOT_ONE_TODO
                            }
                        }
                    },
                },
            }
        )

    @staticmethod
    @inject
    def _create_todo(
        payload: TODOCreateRequest,
        user: Annotated[str, Depends(get_request_user)],
        service: TODOService = Depends(Provide[DI.todo_service]),
    ):
        payload._user = user
        return service.create_todo(payload)

    @staticmethod
    @inject
    def _update_todo(
        id_: Annotated[int, Path(..., gt=0)],
        payload: TODOUpdateRequest,
        user: Annotated[str, Depends(get_request_user)],
        service: TODOService = Depends(Provide[DI.todo_service])
    ):
        payload._user = user
        return service.update_todo(id_, payload)

    @staticmethod
    @inject
    def _delete_todo(
        id_: Annotated[int, Path(..., gt=0)],
        user: Annotated[str, Depends(get_request_user)],
        service: TODOService = Depends(Provide[DI.todo_service]),
    ):
        service.delete_todo(id_, user)

    @staticmethod
    @inject
    def _read_todo(
        user: Annotated[str, Depends(get_request_user)],
        service: TODOService = Depends(Provide[DI.todo_service]),
    ):
        return service.read_todo(user)