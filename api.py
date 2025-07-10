from fastapi import  Body, Depends, HTTPException, Query, status,Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import  Session, select
from db import get_session
from database import LoginHistory, Token, User
from pmodels import BM_LoginHistory, BM_Token, BM_User, BM_Login
from utilit import create_access_token, hash_password, verify_password
from fastapi.openapi.utils import get_openapi
import logging
from fastapi import APIRouter
import uuid
api_router = APIRouter()
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)



@api_router.post("/signup", status_code=200, response_model=BM_Token)
def signup(fetcheduser:BM_User, session: Session = Depends(get_session)):
    logger.info(fetcheduser)
    print("True")
    stmt =select(User).where(User.username==fetcheduser.username)
    existing_user =session.exec( stmt).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
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
def login(fetchedinfo:BM_Login = Query() , session: Session = Depends(get_session)): #form_data: OAuth2PasswordRequestForm = Depends()
  
    user = session.exec(select(User).where(User.username == fetchedinfo.username)).first() #replace fetchedinfo wiht form_data
    if not user or not verify_password(fetchedinfo.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    
    # Optional: Save login history
    login_entry = LoginHistory(username=user.username, sessionid="session123", token=access_token)
    session.add(login_entry)
    session.commit()

    return Token(access_token=access_token, token_type="bearer")
















