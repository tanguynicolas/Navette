# root of the project, which inits the FastAPI app

from fastapi import FastAPI

from config import settings
from user.router import router as user

app = FastAPI()

app.include_router(user, prefix="/api/v1", tags=["navette_v1"])

@app.get("/livez")
def alive():
    return("I'm alive!")

@app.get("/info")
def info():
    return{
        "Database host": settings.db_host,
        "Database username": settings.db_user
    }
