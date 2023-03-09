from flask import make_response, jsonify, request
from app.services.JwtService import JWTService
from app.config.config import ACCESS_TOKEN_TIMEOUT, REFRESH_TOKEN_TIMEOUT
from datetime import datetime, timedelta
from bson import ObjectId
from functools import wraps
import jwt

print("************ Timeout")
print(ACCESS_TOKEN_TIMEOUT)
print(REFRESH_TOKEN_TIMEOUT)


def token_required(func):
    @wraps(func)
    def decorated(self, *args, **kwargs):
        token = request.headers.get('Authorization')
        if (token):
            token = token.split(" ")[1]
        print("Token:", token)
        if not token:
            return jsonify({
                "statusCode": 401,
                "message": "Token is Missing"
            })
        try:
            payload = JWTService.verify(token=token)
            print("Payload :", payload)
            return func(self)
        except jwt.ExpiredSignatureError:
            return jsonify({
                "statusCode": 401,
                "message": "Token is Expired !!"
            })
        except jwt.InvalidTokenError:
            return jsonify({
                "statusCode": 401,
                "message": "Token is Invalid !!"
            })
    return decorated


def response(status, message, status_code):
    """
    Helper method to make an Http response
    :param status: Status
    :param message: Message
    :param status_code: Http status code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code


def generate_token(userId, database, status, statusCode, role="user"):
    """
    Generate Access-Token && Refresh-Token
    :param userId
    :param accessTokenExp
    :param refreshTokenExp
    :param database
    :retun
    """
    isTokenExist = database.refreshToken.find_one({"userId": userId})
    print("isTokenExist :", isTokenExist)
    if (isTokenExist):
        database.refreshToken.delete_one({"userId": ObjectId(userId)})
    accessTokenExpireTime = int(
        (datetime.now() + timedelta(minutes=int(ACCESS_TOKEN_TIMEOUT))).timestamp())
    refreshTokenExpireTime = int(
        (datetime.now() + timedelta(minutes=int(REFRESH_TOKEN_TIMEOUT))).timestamp())
    accessToken = JWTService.sign(payload={"_id": str(
        userId), "exp": accessTokenExpireTime}, token_name='acces_token')
    refreshToken = JWTService.sign(payload={"_id": str(
        userId), "exp": refreshTokenExpireTime}, token_name='refresh_token')
    database.refreshToken.insert_one(
        {'token': refreshToken.decode('utf-8'), 'userId': userId})
    if (role == "admin"):
        users = list(database.users.find({}, {"password": 0, "_id": 0}))
        return make_response(jsonify({
            'status': status,
            'accessToken': accessToken.decode('utf-8'),
            'refreshToken': refreshToken.decode('utf-8'),
            "data": users
        })), statusCode

    return make_response(jsonify({
        'status': status,
        'accessToken': accessToken.decode('utf-8'),
        'refreshToken': refreshToken.decode('utf-8')
    })), statusCode


def BlackListToken(token, database):
    try:
        database.refreshToken.delete_one({'token': token})
    except Exception as e:
        return response('failed', 'server error', 500)


def verify_link(url, payload):
    try:
        link = "{}/verify/{}".format(url, jwt.encode(payload=payload,
                                                     key="secret", algorithm="HS256").decode())
        return link
    except:
        return response('failed', 'server error', 500)
