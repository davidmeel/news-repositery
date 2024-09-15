from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from dependencies.JWT.handlers import JWTHandler


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/signin")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            # Use JWTHandler to decode and verify the token
            handler = JWTHandler()
            if not handler.decode_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")