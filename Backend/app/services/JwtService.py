import sys
import os
import jwt
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from config import JWT_SECRET, REFRESH_SECRET


class JWTService:
    @staticmethod
    def sign(payload, token_name='access_token'):
        secret = JWT_SECRET if token_name != 'refresh_token' else REFRESH_SECRET
        return jwt.encode(
            payload=payload,
            key=secret
        )

    @staticmethod
    def verify(token, token_name='access_token'):
        secret = JWT_SECRET if token_name != 'refresh_token' else REFRESH_SECRET
        try:
            payload = jwt.decode(token, secret)
            return {
                "statusCode": 200,
                "data": payload
            }

        except jwt.ExpiredSignatureError:
            return {
                "statusCode": 401,
                "message": "Token is Expired !!"
            }
        except jwt.InvalidTokenError:
            return {
                "statusCode": 401,
                "message": "Token is Invalid !!"
            }
