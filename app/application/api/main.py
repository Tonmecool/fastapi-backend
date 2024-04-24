from contextlib import asynccontextmanager
from fastapi import FastAPI

from application.api.lifespan import close_message_broker, init_message_broker
from application.api.messages.handlers import router as message_router
from application.api.messages.websockets.messages import router as message_ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()
    yield
    await close_message_broker()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kafka Chat",
        docs_url="/api/docs",
        description="У семьи каннибалов умер родственник - и грустно и вкусно. Слава спасибо",
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(message_router, prefix='/chats')
    app.include_router(message_ws_router, prefix='/chats')

    return app
