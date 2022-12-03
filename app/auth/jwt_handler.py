# This file is responsible for signing, encoding, decoding and returning JWTs.
import time
import jwt
from decouple import config

JWT_SECRET = config('SECRET')
JWT_ALGORITHM = config('ALGORITHM')


# Function returns the generated Tokens (JWTs)
def token_response(token: str):
    return {
        'access token': token
    }


def sighJWT(userID: str):
    payload = {
        'userID': userID,
        'expiry': time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}
