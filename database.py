from sqlmodel import SQLModel,Field
import uuid

class User(SQLModel,table = True):
    id: uuid.UUID|None = Field(default_factory=uuid.uuid4,primary_key=True)
    username : str|None  = Field()
    password: str = Field()
    name : str|None = Field(default='')
    phone : str|None = Field(default='')
    email : str|None = Field(default='')

class LoginHistory(SQLModel,table = True):
    id: int|None = Field(primary_key=True)
    username : str|None  = Field()
    sessionid: str|None = Field()
    token:str|None = Field()

class Token(SQLModel):
    access_token: str
    token_type: str


def get_metadata():
    return SQLModel.metadata