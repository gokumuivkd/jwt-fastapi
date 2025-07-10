from pydantic import BaseModel
import uuid

class BM_User(BaseModel):
    username : str|None  
    password: str 
    name : str|None 
    phone : str|None
    email : str|None
    
    

class BM_LoginHistory(BaseModel):
    username : str|None  
    sessionid: str|None 
    token:str|None 

class BM_Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class BM_Login(BaseModel):
    username : str|None  
    password: str 
