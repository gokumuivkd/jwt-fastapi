from sqlmodel import create_engine, Session
#import asyncpg
#from sqlmodel.ext.asyncio.session import AsyncSession
#from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

#postgresserverconnectionstring = "postgresql+asyncpg://postgres:postgres@localhost/dbname"
postgresserverconnectionstring = "postgresql://postgres:postgres@localhost/dbname"
engine = create_engine(postgresserverconnectionstring, echo=True)
#engine = create_async_engine(postgresserverconnectionstring, echo=True)
#async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
def get_session():
    with Session(engine) as session:
        yield session


# `dbname` to be updated by self.
