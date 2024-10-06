import os
import jwt
import datetime

from datetime import timedelta
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
from typing import List, Annotated, Dict, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from sqlalchemy import text

from ..database import Session, get_session
from ..models import TokenData, User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = os.environ["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["JWT_EXPIRATION"])

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise PyJWTError
    user = await AuthService(Session()).get_user(token_data.username)
    if not user:
        raise credentials_exception
    return User.from_orm(user)


class AuthService:
    """ Service for simple authorization """

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user(self, email: str) -> Dict:
        result = await self.session.execute(
            text(f'''
                 SELECT * FROM admin.users
                 WHERE email = :email 
                 '''),
            [{"email": email}]
        )
        result = result.first()
        if result:
            return result

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    @classmethod
    def create_access_token(cls, data: Dict,
                            expires_delta: Union[timedelta, None]):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + timedelta(minutes=216000)  # 150 days
        to_encode.update({"expr": str(expire)})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY,
                                 algorithm=ALGORITHM)
        return encoded_jwt

    async def users_list(self) -> List[Dict]:
        """
        This method allows to get all users for test

        :rtype: List[Dict]
        """

        result = await self.session.execute(
            text(f'''
                  SELECT * FROM admin.users
                  '''),
            )
        result = [user for user in result.all()]
        if result:
            return result