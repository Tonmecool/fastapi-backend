from fastapi import FastAPI


def create_app():
    return FastAPI(
        title="Kafka Chat",
        docs_url="/api/docs",
        description="У семьи каннибалов умер родственник - и грустно и вкусно. Слава спасибо",
        debug=True,
    )
