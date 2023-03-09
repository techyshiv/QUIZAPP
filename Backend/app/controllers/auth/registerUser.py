from app import bcrypt
from flask import request, render_template
from flask.views import MethodView
from flask import Blueprint
from app.services.customErrorHandler import customErrorHandler
from app.controllers.auth.helper import response, generate_token, verify_link
from app.validator import userValidate
from app.controllers.auth.emailSender import Email
from app import DB
from app.config.config import EMAIL_VERIFICATION_APPLY
from app.config.config import APP_URL, APP_PORT
from threading import Thread
register_auth = Blueprint('register_auth', __name__)
email = Email()


class RegisterUser(MethodView):

    def get(self):
        return render_template("signup.html")

    def post(self):
        """
        Register a user, generate their token and add them to the database
        :return: Json Response with the user`s token
        """
        try:
            if request.content_type == "application/json":
                # [+] get data
                req = request.json
                userDetails = {
                    "firstname": req["firstname"] if "firstname" in req else "",
                    "lastname": req["lastname"] if "lastname" in req else "",
                    "email": req["email"] if "email" in req else "",
                    "password": req["password"] if "password" in req else "",
                    "role": req["role"] if "role" in req else "user",
                }

                print("userDetails")
                print(userDetails)

                # [+] Validate Request
                res = userValidate.Validate(payload=req)
                if (res["statusCode"] != 200):
                    return response('failed', "Request Payload is Not Valid", 403)
                # [+] Check Whether User Already Exist or Not
                isExist = DB.users.find_one({'email': userDetails['email']})
                print("is email exist :", isExist)
                if (isExist):
                    return response('failed', "Email already taken", 409)
                # [+] : Hash Password
                hashPassword = bcrypt.generate_password_hash(
                    userDetails["password"])
                # print("HashPassword :", hashPassword)
                # [+] : Prepare the model
                userDetails["password"] = hashPassword
                if (EMAIL_VERIFICATION_APPLY == "YES"):
                    userDetails["is_active"] = False
                    # [+] Send Email Verification
                    email_verify_link = verify_link(
                        url=f"{APP_URL}:{APP_PORT}/v1/auth", payload={"email": userDetails["email"]})
                    print("email verify link :", email_verify_link)
                    if isinstance(email_verify_link, str):
                        task = Thread(target=email.send, kwargs=({
                            "receiver_email": [userDetails['email']],
                            "email": "support@myblog.com",
                            "number": "+91 1111111111",
                            "verify_link": email_verify_link,
                            "image_url": "index.webp"
                        }))
                        task.start()
                else:
                    userDetails["is_active"] = True

                # [+] Save User in database
                result = DB.users.insert_one(userDetails)
                print("Result :", result.inserted_id)
                userId = result.inserted_id
                # [+] Generate Tokens
                return generate_token(userId=userId, database=DB, status='success', statusCode=201)
            return response('failed', 'Content-type must be json', 403)
        except Exception as e:
            return response('failed', customErrorHandler.serverError, 500)


class VerifyUser(MethodView):
    """
    Class to verify user
    """

    def get(self, token):
        print("token :", token)
        res = email.validateEmail(token)
        print(res)
        if (res["statusCode"] == 200):
            # [+] Update User Status in database
            email_address = res['data']['email']
            DB.users.update_one({"email": email_address}, {
                "$set": {"is_active": True}})
            return response('success', 'Email Verification is Successfully Completed', 200)
        else:
            return response('failed', 'Unauthorized', 409)


class ResendEmail(MethodView):
    def post(self):
        try:
            if request.content_type == "application/json":
                # [+] get data
                req = request.json
                user_email = req['email']
                # [+] Send Email Verification
                email_verify_link = verify_link(
                    url=f"http://{APP_URL}:{APP_PORT}/v1/auth", payload={"email": user_email})
                print("email verify link :", email_verify_link)
                if isinstance(email_verify_link, str):
                    task = Thread(target=email.send, kwargs=({
                        "receiver_email": [user_email],
                        "email": "support@myblog.com",
                        "number": "9621299170",
                        "verify_link": email_verify_link,
                        "image_url": "index.webp"
                    }))
                    task.start()
                    return response('success', 'Email send successfully', 200)
                return response('failed', 'server error', 500)

            return response('failed', 'Content-type must be json', 403)
        except Exception as e:
            return response('failed', customErrorHandler.serverError, 500)


# Register classes as views
registration_view = RegisterUser.as_view('register')
verify_view = VerifyUser.as_view('verify')
resend_view = ResendEmail.as_view('resend')

register_auth.add_url_rule(
    '/auth/register', view_func=registration_view, methods=['POST', 'GET'])

register_auth.add_url_rule(
    '/auth/verify/<string:token>', view_func=verify_view, methods=["GET"])

register_auth.add_url_rule(
    '/auth/resend', view_func=resend_view, methods=["POST"])
