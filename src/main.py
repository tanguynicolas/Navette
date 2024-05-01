# root of the project, which inits the FastAPI app

from fastapi import FastAPI

from .config import database_settings
from .auth.router import router as auth
from .city.router import router as city
from .zone.router import router as zone
from .user.router import router as user

app = FastAPI(title="Navette")

app.include_router(auth, prefix="/api/v1/auth", tags=["auth"])
app.include_router(city, prefix="/api/v1/city", tags=["city"])
app.include_router(zone, prefix="/api/v1/city/{city_id}/zone", tags=["zone"])
app.include_router(user, prefix="/api/v1/user", tags=["user"])

@app.get("/livez")
def alive():
    return("I'm alive!")

@app.get("/info")
def info():
    database_type = "sqlite" if database_settings.enable_sqlite == True else "postgres"

    return{
        "Database type": database_type,
        "Database host": database_settings.hostname,
        "Database username": database_settings.username
    }
