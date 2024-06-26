# FastAPI + Kafka DDD chat with MongoDB

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Tonmecool/fastapi-backend.git
   cd fastapi-backend

2. Install all required packages in `Requirements` section.

3. **Create network for all services**
   ```bash
   docker network create --driver bridge --attachable backend


### Implemented Commands

* `make all` - up all application and database infra
* `make app` - up application
* `make app-logs` - follow the logs in app container
* `make app-down` - down application
* `make app-shell` - go to contenerized interactive shell (bash)
* `make test` - run tests
* `make storages` - up database infra
* `make storages-down` - down database infra

## Go to telegram bot microservice

[telegram-bot-for-fastapi-backend](https://github.com/Tonmecool/telegram-bot-for-fastapi-backend) (docs in work)