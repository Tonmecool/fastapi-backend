from faker import Faker
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from httpx import Response
import pytest


@pytest.mark.asyncio
async def test_create_chat_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for('create_chat_handler')
    title = faker.text(max_nb_chars=100)
    responce: Response = client.post(url=url, json={'title': title})

    assert responce.is_success
    json_data = responce.json()

    assert json_data['title'] == title


@pytest.mark.asyncio
async def test_create_chat_fail_text_too_long(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for('create_chat_handler')
    title = faker.text(max_nb_chars=1000)
    responce: Response = client.post(url=url, json={'title': title})

    assert responce.status_code == status.HTTP_400_BAD_REQUEST, responce.json()
    json_data = responce.json()

    assert json_data['detail']['error']


@pytest.mark.asyncio
async def test_create_chat_fail_text_empty(
    app: FastAPI,
    client: TestClient,
):
    url = app.url_path_for('create_chat_handler')
    responce: Response = client.post(url=url, json={'title': ''})

    assert responce.status_code == status.HTTP_400_BAD_REQUEST, responce.json()
    json_data = responce.json()

    assert json_data['detail']['error']
