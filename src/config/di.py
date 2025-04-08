from dependency_injector import containers, providers

from domain.todo.repositories.entities import TODOEntity
from domain.todo.repositories.todo_repository import TODORepository
from domain.todo.services.todo_service import TODOService
from infra.sqlite import SqliteDatabase


class DI(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["domain.todo.controllers.todo_controller"]
    )

    database_driver = providers.Singleton(SqliteDatabase, dns="sqlite:///:memory:")
    todo_repository = providers.Singleton(
        TODORepository,
        database=database_driver,
        entity=TODOEntity
    )
    todo_service = providers.Singleton(
        TODOService,
        repository=todo_repository
    )