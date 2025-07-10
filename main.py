from fastapi import FastAPI
import json
from api import api_router
from sqlmodel import SQLModel
from db import engine

app = FastAPI()
app.include_router(api_router)

















#=================OPENAPI BELOW==================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    with open("openapi.json", "r") as f:
        app.openapi_schema = json.load(f)

    return app.openapi_schema

app.openapi = custom_openapi


