# Navette API

## Initial setup

```shell
python3 -m venv .venv
source .venv/bin/activate

pip install fastapi "uvicorn[standard]" pydantic[email]
pip freeze > requirements.txt
```

```shell
# Base dirs and files
mkdir alembic src tests templates # add requirements for multi env
touch .env .gitignore logging.ini alembic.ini

# Base dirs and fils in src
(cd src && \
touch config.py models.py exceptions.py database.py main.py)

# Package
mkdir src/api
(cd src/api && \
touch router.py schemas.py models.py dependencies.py config.py constants.py exceptions.py service.py utils.py)
```

## Setup

```shell
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cd src
uvicorn main:app --reload
```
