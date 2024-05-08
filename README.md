# Navette API

API for a university carpooling application called Navette. Project for University of Picardie (Amiens, France) - Master Degree.

## Initial setup

```shell
python3 -m venv .venv
source .venv/bin/activate

pip install fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings sqlalchemy psycopg2-binary alembic
pip freeze > requirements.txt
```

## Setup

```shell
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

touch .env
```

## Migration

Adapt `.env` file before if necessary.

```shell
alembic revision --autogenerate [-m ""]
alembic upgrade head
```

# Run locally

Adapt `.env` file before if necessary.

```shell
docker compose -f docker-compose-local.yml up -d 
uvicorn src.main:app --reload
```
