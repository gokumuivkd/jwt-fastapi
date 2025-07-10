# Simple Backend for JWT Authenticating User and Logging in System

## Modifications Required.
Foldername: RENAME /FOLDER everywhere to your custom /Folder then install your libraries.
databasename: RENAME all dbname to your given database name for this app.
Note: run python onceinalifetime.py only when you understand when to run sqlmodel.metadata.createall()

configurea.py like below
=======================================
from passlib.context import CryptContext
SECRET_KEY = "<your_own_secret_key>"
ALGORITHM = "HS256" # or any other
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # or your value
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #
 
