from fastapi import FastAPI

from application.api.messages.handlers import router as message_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kafka Chat",
        docs_url="/api/docs",
        description="У семьи каннибалов умер родственник - и грустно и вкусно. Слава спасибо",
        debug=True,
    )
    app.include_router(message_router, prefix='/chat')

    return app
