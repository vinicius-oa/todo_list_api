from typing import Type

from starlette import status
from typing_extensions import List

from config.exception import GeneralException
from domain.common.repository.exceptions import RepositoryException
from domain.todo.controllers.schemas.request.todo_schema_request import TODOCreateRequest, TODOUpdateRequest
from domain.todo.enums import ExceptionErrorMsgs
from domain.todo.repositories.entities import TODOEntity
from infra.base import DatabaseABC


class TODORepository:
    def __init__(self, *, database: DatabaseABC, entity: Type[TODOEntity]):
        self._database = database
        self._entity = entity


    def create_todo(
        self,
        value: TODOCreateRequest
    ) -> TODOEntity:
        try:
            with self._database.get_connection() as conn:
                entity = self._entity(user=value._user, **value.model_dump())
                conn.add(entity)
                conn.flush()
                conn.expunge(entity)
        except GeneralException as e:
            raise e from e
        else:
            return entity

    def read_todo(self, user: str) -> List[TODOEntity]:
        with self._database.get_connection() as conn:
            entities = conn.query(self._entity).filter(self._entity.user == user).all()
            if entities:
                for e in entities:
                    conn.expunge(e)

        if not entities:
            raise RepositoryException(
                content=ExceptionErrorMsgs.NOT_ONE_TODO,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return entities

    def update_todo(
        self,
        id_: int,
        value: TODOUpdateRequest
    ) -> TODOEntity:
        with self._database.get_connection() as conn:
            entity: TODOEntity = conn.query(
                self._entity
            ).filter(self._entity.id == id_, self._entity.user == value._user).first()
            if entity:
                values_to_update = value.model_dump(exclude_none=True)
                for v in values_to_update:
                    setattr(entity, v, values_to_update[v])
                conn.flush()
                conn.refresh(entity)
                conn.expunge(entity)

        if not entity:
            raise RepositoryException(
                content=ExceptionErrorMsgs.TODO_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return entity


    def delete_todo(self, id_: int, user: str):
        with self._database.get_connection() as conn:
            entity: TODOEntity = conn.query(
                self._entity
            ).filter(self._entity.id == id_, self._entity.user == user).first()
            if entity:
                conn.delete(entity)

        if not entity:
            raise RepositoryException(
                content=ExceptionErrorMsgs.TODO_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
