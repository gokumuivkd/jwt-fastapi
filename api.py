from fastapi import APIRouter
from fastapi import  Body, Depends, HTTPException, Query, status,Form, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import  Session, select, modifier
from db import get_session
from database import LoginHistory, Token, User
from pmodels import BM_LoginHistory, BM_Token, BM_User, BM_Param_UserName,BM_Param_Password,BM_Param_UserEmail
from utilit import create_access_token, hash_password, verify_password
from pydantic import AfterValidator
# from fastapi.openapi.utils import get_openapi
import logging
import uuid

api_router = APIRouter()
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)





@api_router.post("/signup", status_code=200, response_model=BM_Token)
def signup( fetcheduser:BM_User, session: Session = Depends(get_session)):
    """
    Route to Signup for registration. 
    Function Params:
    1) fetcheduser: A data interpreted as BM_User as json inside API Request Body.(MUST)
        BM_User fields must match with Json keys.
    2) session: A session of database from sqlmodel.   
    """
    if isinstance(fetcheduser.phone,ValueError):
        return HTTPException(100,fetcheduser.phone.args)
    stmt =select(User).where((User.username==fetcheduser.username)|(User.email == fetcheduser.email)|(User.phone == fetcheduser.phone))
    existing_user =session.exec( stmt).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or phone or email already registered")
    fetcheduser.password = hash_password(fetcheduser.password)
    newuser=User(id = uuid.uuid4(),
        username=fetcheduser.username,
        password=fetcheduser.password,
        name= fetcheduser.name,
        phone=fetcheduser.phone,
        email= fetcheduser.email
    )
    session.add(newuser)
    session.commit()
    session.refresh(newuser)
    access_token = create_access_token(data={"sub": newuser.username})
    return Token(access_token=access_token, token_type="bearer")
    


@api_router.post("/login",status_code=200, response_model=BM_Token)
def login(response: Response, fetchedpassword:BM_Param_Password,fetchedusername:BM_Param_UserName = Query() ,
          session: Session = Depends(get_session)):
    """
    Route to login the user.
    Params:
    1) fetchedusername: Api Url Params is interpreted as BM_Param_UserName using the fastapi Query().
    2) fetchedpassword: Api Url body is interpreted as BM_Param_Password.
    3) session: A session of database from sqlmodel.
    
    Can also contain code for authorization after authenticating the user.
    """
    #form_data: OAuth2PasswordRequestForm = Depends()
    user =    session.exec(select(User).where(User.username == fetchedusername.username)).first() #replace fetchedusername with form_data
    if not user or not verify_password(fetchedpassword.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}",httponly=True, max_age=3600, secure=True, samesite="Lax")
    # Optional for now : Save login history
    login_entry = LoginHistory(username=user.username, sessionid="session123", token=access_token)
    session.add(login_entry)
    session.commit()
    return Token(access_token=access_token, token_type="bearer")




@api_router.get("/logout", status_code=200)
def logout(response: Response, session: Session = Depends(get_session)):
    """
    Route to logout the user.
    """
    
    response.delete_cookie(key="access_token", httponly=True, secure= True,samesite='lax')
    # NOTE: database session closes here
    if session:
        session.close()
    return {"message":"User Logged Out. You may close this window.", "status_code":200}



@api_router.post("/forgot_username", status_code=200)
def forgot_username(fetcheduseremail: BM_Param_UserEmail,session:Session = Depends(get_session)):
    """
    Route to send username back to the user .
    Params:
    1) fetcheduseremail: Api Url Params is interpreted as BM_Param_UserEmail using the fastapi Query().
    2) session: A session of database from sqlmodel.
    """
    stmt =select(User).where(User.email == fetcheduseremail.email)
    founduser = session.exec(stmt).first()
    if founduser:
        return {"message": founduser, "status_code": 200}
    return {"message": "No such User", "status_code":100}



@api_router.post("/forgot_password", status_code=200)
def forgot_password(fetcheduseremail: BM_Param_UserEmail,session:Session = Depends(get_session)):
    stmt =select(User).where(User.email == fetcheduseremail.email)
    founduser = session.exec(stmt).first()
    if founduser:
        session.close()
        new_user=modify_password('new_password', founduser=founduser ) # 'Hardcoded password being sent currently'
        session.delete(founduser)
        session.add(new_user)
        session.commit()
        session.close()
        return {"message": "Password Change was successful", "status_code": 200}
    session.close()
    return {"message": "No such User", "status_code":100}



def modify_password(new_password:str,founduser):
    new_user = User(username= founduser.username, password=hash_password(new_password), name=founduser.name,
                phone=founduser.phone, email= founduser.email)
    return new_user



