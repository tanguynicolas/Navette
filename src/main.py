# root of the project, which inits the FastAPI app

from fastapi import FastAPI

from config import settings
from user.router import router

app = FastAPI()

app.include_router(router, prefix="/user", tags=["user"])

@app.get("/livez")
def alive():
    return("I'm alive!")

@app.get("/info")
def info():
    return{
        "Database username": settings.db_user
    }
