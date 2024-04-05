from typing import Iterable
from punq import Container

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from application.api.messages.schemas import ChatDetailSchema, CreateChatRequestSchema, CreateChatResponseSchema, CreateMessageResponseSchema, CreateMessageSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import init_container
from logic.mediator import Mediator
from logic.queries.messages import GetChatDetailQuery


router = APIRouter(tags=['Chat'])


@router.post(
    '/', 
    # response_model=CreateChatResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    description='endpoint creates a new chat. if the chat already exists, an exception 400 is raised',
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    }
)
async def create_chat_handler(schema: CreateChatRequestSchema, container=Depends(init_container)) -> CreateChatResponseSchema:
    ''' Creates a new chat '''
    mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    '/{chat_oid}/messages', 
    status_code=status.HTTP_201_CREATED,
    description='creates a new message in a chat',
    responses={
        status.HTTP_201_CREATED: {'model': CreateMessageSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageSchema, 
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    ''' Creates a new message '''
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand( 
                text=schema.text, 
                chat_oid=chat_oid,
            )
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    
    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    '/{chat_oid}/',
    status_code=status.HTTP_200_OK,
    description='retrieves a chat',
    responses={
        status.HTTP_200_OK: {'model': ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    }
)
async def get_chat_with_messages_handler(
    chat_oid: str, 
    container: Container = Depends(init_container)
) -> ChatDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    
    return ChatDetailSchema.from_entity(chat)
