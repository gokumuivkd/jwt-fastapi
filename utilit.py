from datetime import datetime, timedelta
from jose import jwt
from configurea import pwd_context,SECRET_KEY,ALGORITHM
def hash_password(password: str) -> str:
    """
    computes and returns cryptographic hash for given password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    recomputes and compares the cryptographic hash of given plain_password
    with hashed_password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates Access token from the data dictionary. 
    Also adds time of token expirations.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)