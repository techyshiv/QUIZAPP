from flask import request
from flask.views import MethodView
from flask import Blueprint
from app import DB
from app.controllers.auth.helper import response, BlackListToken, generate_token
refresh_auth = Blueprint('refresh_auth', __name__)


class RefreshToken(MethodView):
    """
    :Refresh Token ,get Access-Token and delete it from database and generate new Access-Token & RefreshToken
    """

    def post(self):
        try:
            if request.content_type == "application/json":
                # [+] Get data
                req = request.json
                refreshToken = req['refreshToken']
                # Check whether it present in database or not
                isExist = DB.refreshToken.find_one({'token': refreshToken})
                if (not isExist):
                    pass
                BlackListToken(refreshToken, database=DB)
                # [+] Generate new Acces-Token and RefreshToken
                return generate_token(userId=isExist['userId'], database=DB, status='success', statusCode=201)
            return response('failed', 'Content-type must be json', 403)
        except Exception as e:
            print("Error ", e)
            return response('failed', "server error", 500)
        # [+] Get Data
        req = request.json()


# Register classes as views
refresh_view = RefreshToken.as_view('refresh')
refresh_auth.add_url_rule(
    '/auth/refresh', view_func=refresh_view, methods=['POST'])
