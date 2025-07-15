from fastapi import FastAPI
import json
from api import api_router
from sqlmodel import SQLModel

app = FastAPI()
app.include_router(api_router)

# CRITICAL SECTION
def custom_openapi():
    """function always needed to make sure custom openapi_schema is properly established and assigned"""
    if app.openapi_schema:
        return app.openapi_schema

    with open("openapi.json", "r") as f:
        app.openapi_schema = json.load(f)

    return app.openapi_schema

#app.openapi = custom_openapi


