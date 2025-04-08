from pydantic import Field

from domain.todo.controllers.schemas.request.todo_schema_request import TODOCreateRequest


class TODOCreateResponse(TODOCreateRequest):
    id: int = Field(..., gt=0)
    user: str


class TODOUpdateResponse(TODOCreateResponse):
    pass


class TODOReadResponse(TODOCreateResponse):
    pass