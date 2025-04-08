from domain.todo.controllers.schemas.request.todo_schema_request import TODOCreateRequest, TODOUpdateRequest
from domain.todo.repositories.todo_repository import TODORepository


class TODOService:

    def __init__(self, *, repository: TODORepository):
        self._repository = repository


    def create_todo(self, value: TODOCreateRequest):
        return self._repository.create_todo(value)

    def update_todo(self, id_: int, value: TODOUpdateRequest):
        return self._repository.update_todo(id_, value)

    def delete_todo(self, id_: int, user: str):
        self._repository.delete_todo(id_, user)

    def read_todo(self, user: str):
        return self._repository.read_todo(user)
