"""handles all classes as table"""
import uuid
from pydantic import ConfigDict
from sqlmodel import Column, SQLModel,Field, \
Constraint,CheckConstraint,UniqueConstraint,ForeignKeyConstraint,PrimaryKeyConstraint, BigInteger



class User(SQLModel, table=True):
    """
    Defines a User Table using SQLModel
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str | None = Field(default=None, unique=True)
    password: str = Field()
    name: str | None = Field(default='')
    phone: int | None = Field(default=None, sa_column=Column(BigInteger) )
    email: str | None = Field(default='', unique=True)

    __table_args__ = (
        CheckConstraint("phone >= 6000000000 AND phone <= 9999999999"),
        UniqueConstraint("username"),
        UniqueConstraint("phone"),
        UniqueConstraint("email"),
    )
    

class LoginHistory(SQLModel,table = True):
    """
    defines LoginHistory Table using SQLModel
    Stores sessionid if there is any  and username and token once some user logs in 
    """
    id: int|None = Field(primary_key=True)
    username : str|None  = Field()
    sessionid: str|None = Field(default_factory=uuid.uuid4)
    token:str|None = Field()



class Token(SQLModel):
    """
    To let serialize the object to send as response in return to api calls 
    showing accesstoken or bearer token to the user.
    Used while Signup and Login.
    """
    access_token: str
    token_type: str




def get_metadata():
    """gets the metadata in the same runtime."""
    return SQLModel.metadata