from pytest import fixture

from punq import Container

from infra.repositories.messages.base import BaseChatsRepository
from logic.mediator.base import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope='function')
def container() -> Container:
    return init_dummy_container()


@fixture(scope='function')
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture(scope='function')
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(BaseChatsRepository)
