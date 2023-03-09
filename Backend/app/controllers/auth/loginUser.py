import json
from app import bcrypt
from flask import request, make_response, render_template
from flask.views import MethodView
from flask import Blueprint
from app.services.customErrorHandler import customErrorHandler
from app.controllers.auth.helper import response, generate_token
from app.validator import userValidate
from app import DB

login_auth = Blueprint('login_auth', __name__)


class LoginUser(MethodView):
    """
    Login a user, generate their token and add them to the database
    :return: Json Response with the user`s token
    """

    def get(self):
        return render_template('login.html')

    def post(self):
        try:
            if request.content_type == "application/json":
                # [+] get data
                req = request.json
                userDetails = {
                    "email": req["email"] if "email" in req else "",
                    "password": req["password"] if "password" in req else "",
                }
                print("userDetails")
                print(userDetails)
                # [+] Validate Request
                res = userValidate.loginValidate(payload=req)
                if (res["statusCode"] != 200):
                    return response('failed', "Request Payload is not Valid !!", 403)
                # [+] Check Whether User Already Exist or Not
                isExist = DB.users.find_one({'email': userDetails['email']})
                if (not isExist):
                    return response('failed', "Email Address not found", 400)
                # [+] Validate the password
                isPass = bcrypt.check_password_hash(
                    isExist["password"], userDetails["password"])
                if (not isPass):
                    return response('failed', "UnAuthorized Access !!", 401)
                print(isExist)
                if (not isExist['is_active']):
                    return response('failed', 'Email is not verfied', 401)
                # [+] Generate Tokens
                userId = isExist["_id"]
                role = isExist["role"]
                resp = generate_token(
                    userId=userId, role=role, database=DB, status='success', statusCode=201)
                accessToken = json.loads(resp[0].data.decode())['accessToken']
                # print(json.loads(resp[0].data.decode())['accessToken'])
                res = make_response(render_template('login.html'))
                res.set_cookie('access_token', accessToken)
                return res
            else:
                return response('failed', 'Content-type must be json', 403)
        except Exception as e:
            return response('failed', customErrorHandler.serverError, 500)


login_view = LoginUser.as_view('login')
login_auth.add_url_rule(
    '/auth/login', view_func=login_view, methods=['POST', 'GET'])
