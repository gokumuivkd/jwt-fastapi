"""to be used once since sqlmodel.metadata.create_all() is some 
special method call"""
from database import SQLModel
from db import engine

def create_db_and_tables():
    """metadata creation"""
    SQLModel.metadata.create_all(engine)  


if __name__ == "__main__":
    create_db_and_tables()
