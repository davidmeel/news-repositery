from models.users import UserTable
from fastapi import HTTPException, Request, Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import pytz
from fastapi.security import OAuth2PasswordBearer



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
tashkent_tz = pytz.timezone("Asia/Tashkent")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")



def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(username: str, password: str, session: Session):
    user = session.query(UserTable).filter(UserTable.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify (password, user.password):
        return False
    return user