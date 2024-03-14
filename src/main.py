# root of the project, which inits the FastAPI app

from fastapi import FastAPI

from user.router import *

app = FastAPI()

@app.get("/livez")
def alive():
    return("I'm alive!")

app.include_router(router)
