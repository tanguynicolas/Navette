# Navette API

## Initial setup

```shell
python3 -m venv .venv
source .venv/bin/activate

pip install fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings sqlalchemy alembic
pip freeze > requirements.txt
```

```shell
# Base dirs and files
mkdir alembic src tests templates # add requirements for multi env
touch .env .gitignore logging.ini alembic.ini templates/index.html

# Base dirs and fils in src
(cd src && \
touch config.py models.py exceptions.py database.py main.py)

# Package
mkdir src/user
(cd src/user && \
touch router.py schemas.py models.py dependencies.py config.py constants.py exceptions.py service.py utils.py ../tests/user)
```

## Setup

```shell
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cd src
uvicorn main:app --reload
```

## Travaux

- quand on récupère toutes les cities / users, afficher uniquement leur nom unique
- avec ce nom unique, une requete via ce nom unique permet de récup toutes les infos sur le city/user (remplacer get_user_by_id par get_user_by_email ?)
- plutôt que de re spécifier à chaque fois les types à passer aux functions, utiliser les types du schéma en question
