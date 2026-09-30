from datetime import UTC, timedelta, datetime
import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt import  InvalidTokenError
from fastapi import HTTPException, status, Depends
from app.config.config import  settings as s


SECRET_KEY = s.secret_key
ALGORITHM = s.algorithm
EXPIRATION_MINUTE= 30
oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(tokendata:dict):
    expiration_minute = datetime.now(UTC) + timedelta(minutes=EXPIRATION_MINUTE)
    tokeninfo = tokendata.copy()
    tokeninfo.update({"exp": expiration_minute})
    new_access_token = jwt.encode(tokeninfo, SECRET_KEY, ALGORITHM)
    return {"token": new_access_token, "token_type":"bearer"}



def verify_access_token(token:str, credentials_exception):
    try:
        tokendata = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = tokendata.get("user_id")
        if id is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        data = id
    except InvalidTokenError:
        raise credentials_exception

    return data


def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate":"Bearer"}, detail="Could not verify Credentials")
    return verify_access_token(token, credentials_exception)

