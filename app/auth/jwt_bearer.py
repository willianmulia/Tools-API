# The function of this file is to check whether the request is authorized or not [ Verification of the protected route ]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail='Invalid or Expired Token!')
            return credentials.credentials

    def verify_jwt(self, jwtoken: str):
        is_token_valid: bool = False
        payload = decodeJWT(jwtoken)
        if payload:
            is_token_valid = True
        return is_token_valid
