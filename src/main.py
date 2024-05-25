# root of the project, which inits the FastAPI app

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .config import database_settings
from .auth.router import router as auth
from .city.router import router as city
from .zone.router import router as zone
from .stop.router import router as stop
from .user.router import router as user
from .travel.router import router as travel

app = FastAPI(
    title="Navette",
    description="API for a university carpooling application called Navette. Project for University of Picardie (Amiens, France) - Master Degree."
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

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

app.include_router(auth, prefix="/api/v1/auth", tags=["auth"])
app.include_router(city, prefix="/api/v1/city", tags=["city"])
app.include_router(zone, prefix="/api/v1/city/{city_id}/zone", tags=["zone"])
app.include_router(stop, prefix="/api/v1/city/{city_id}/stop", tags=["stop"])
app.include_router(user, prefix="/api/v1/user", tags=["user"])
app.include_router(travel, prefix="/api/v1/travel", tags=["travel"])
