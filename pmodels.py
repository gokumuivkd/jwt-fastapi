from pydantic import BaseModel, field_validator, field_serializer

class BM_User(BaseModel):
    """
    Serialization model with validation of the User table.
    """
    username : str|None  
    password: str
    name : str|None 
    phone : int
    email : str|None

    @field_validator('phone')
    @classmethod
    def check_phone(cls, value):
        """check whether a number is a phone number"""
        if value <6000000000 or value >9999999999:
            return ValueError("phone number must be of 10 digits and greater than 5999999999")
            
        return value 
    
class BM_LoginHistory(BaseModel):
    """
    Serialization model of the LoginHistory table.
    """
    username : str|None 
    sessionid: str|None
    token:str|None

class BM_Token(BaseModel):
    """
    Serialization model for Token Usecase.
    """
    access_token: str 
    token_type: str = "bearer"

class BM_Param_UserName(BaseModel):
    """
    Serialization model for Login Purpose only. See Login API Implementation from api.py.
    """
    username : str|None  
class BM_Param_Password(BaseModel):
    """
    Serialization model for Login Purpose only. See Login API Implementation from api.py.
    """
    password : str

class BM_Param_UserEmail(BaseModel):
    """
    Serialization model for Login Purpose only. See Login API Implementation from api.py.
    """
    email : str