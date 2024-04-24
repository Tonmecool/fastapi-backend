from uuid import UUID
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket
from punq import Container

from infra.message_brokers.base import BaseMessageBroker
from logic.init import init_container
from settings.config import Config


router = APIRouter(tags=['chats'])


@router.websocket("/{chat_oid}/")
async def messages_endpoint(
    chat_oid: UUID,
    websocket: WebSocket,
    container: Container = Depends(init_container),
):
    await websocket.accept()
    config: Config = container.resolve(Config)

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start_consuming(
        topic=config.new_messages_received_topic.format(chat_oid=chat_oid),
    )

    while True:
        try:
            await websocket.send_json(await message_broker.consume())
        finally:
            break

    await message_broker.stop_consuming()
    await websocket.close()
