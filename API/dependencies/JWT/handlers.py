from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from config import JWT_SECRET_KEY, JWT_ALGORITHM

class JWTHandler:
    def __init__(self, data: dict = None):
        self.data = data

    def create_token(self, username: str, user_id: int):
        encode = {"sub": username, "id": user_id}
        expires = datetime.utcnow() + timedelta(hours=5)
        encode["exp"] = expires
        return jwt.encode(claims=encode, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def decode_jwt(self, token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token.")
        except Exception:
            raise HTTPException(status_code=500, detail="Token decoding error.")

    def __call__(self, token: str):
        return self.decode_jwt(token)