from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from punq import Container

from application.api.messages.filters import (
    GetAllChatsFilters,
    GetMessagesFilters,
)
from application.api.messages.schemas import (
    AddTelegramListenerResponseSchema,
    AddTelegramListenerSchema,
    ChatDetailSchema,
    ChatListenerListItemSchema,
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageResponseSchema,
    CreateMessageSchema,
    GetAllChatsQueryResponseSchema,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import (
    AddTelegramListenerCommand,
    CreateChatCommand,
    CreateMessageCommand,
    DeleteChatCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import (
    GetAllChatsListenersQuery,
    GetAllChatsQuery,
    GetChatDetailQuery,
    GetMessagesQuery,
)


router = APIRouter(tags=['Chat'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='endpoint creates a new chat. if the chat already exists, an exception 400 is raised',
    description='endpoint creates a new chat. if the chat already exists, an exception 400 is raised',
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    """Creates a new chat."""
    mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    '/{chat_oid}/messages',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': CreateMessageSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='creates a new message in a chat',
    description='creates a new message in a chat',
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageSchema,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Creates a new message."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(
                text=schema.text,
                chat_oid=chat_oid,
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    '/{chat_oid}/',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='retrieves a chat',
    description='retrieves a chat',
)
async def get_chat_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> ChatDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return ChatDetailSchema.from_entity(chat)


@router.get(
    '/{chat_oid}/messages',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': GetMessagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='get all messages in chat',
    description='get all messages in chat',
)
async def get_chat_messages_handler(
    chat_oid: str,
    filters: GetMessagesFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetMessagesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(chat_oid=chat_oid, filters=filters.to_infra()),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return GetMessagesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[MessageDetailSchema.from_entity(message) for message in messages],
    )


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': GetAllChatsQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='Get all working chats',
    description='get all working chats',
)
async def get_all_chats_handler(
    filters: GetAllChatsFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetAllChatsQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chats, count = await mediator.handle_query(
            GetAllChatsQuery(filters=filters.to_infra()),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return GetAllChatsQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[ChatDetailSchema.from_entity(chat) for chat in chats],
    )


@router.delete(
    '/{chat_oid}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='deletes a chat',
    description='deletes a chat',
)
async def delete_chat_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(DeleteChatCommand(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


@router.post(
    '/{chat_oid}/listeners/',
    status_code=status.HTTP_201_CREATED,
    summary='add telegram support listener to chat',
    description='add telegram support listener to chat',
    operation_id='addTelegramListenerToChat',
    response_model=AddTelegramListenerResponseSchema,
)
async def add_listener_handler(
    chat_oid: str,
    schema: AddTelegramListenerSchema,
    container: Container = Depends(init_container),
) -> AddTelegramListenerResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        listener, *_ = await mediator.handle_command(
            AddTelegramListenerCommand(
                chat_oid=chat_oid,
                telegram_chat_id=schema.telegram_chat_id,
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return AddTelegramListenerResponseSchema.from_entity(listener)


@router.get(
    '/{chat_oid}/listeners/',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': ChatListenerListItemSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    summary='Get all listeners in chat',
    description='Get all listeners in chat',
    operation_id='getAllChatListeners',
)
async def get_all_chat_listeners_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> list[ChatListenerListItemSchema]:
    mediator: Mediator = container.resolve(Mediator)

    try:
        listeners = await mediator.handle_query(
            GetAllChatsListenersQuery(chat_oid=chat_oid),
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return [ChatListenerListItemSchema.from_entity(chat_listener=listener) for listener in listeners]
