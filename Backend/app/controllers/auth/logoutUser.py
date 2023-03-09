from flask import request
from flask.views import MethodView
from flask import Blueprint
from app.services.JwtService import JWTService
from app import DB
from app.controllers.auth.helper import response, BlackListToken, token_required
logout_auth = Blueprint('logout_auth', __name__)


class LogoutUser(MethodView):
    @token_required
    def post(self):
        """
        Logout a user using a token and remove token from the database
        :return: Json Response
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                return response('failed', 'Provide a valid auth token', 403)
            else:
                decoded_token_response = JWTService.verify(
                    token=auth_token, token_name='refresh_token')
                print("decoded response :", decoded_token_response)
                if not isinstance(decoded_token_response, dict):
                    BlackListToken(auth_token, database=DB)
                    return response('success', 'Successfully logged out', 200)
                return response('failed', decoded_token_response, 401)
        return response('failed', 'Provide an authorization header', 403)


# Register classes as views
logout_view = LogoutUser.as_view('logout')
logout_auth.add_url_rule(
    '/auth/logout', view_func=logout_view, methods=['POST'])
