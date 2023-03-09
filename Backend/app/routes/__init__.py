from app import app
from app.controllers.auth.registerUser import register_auth
from app.controllers.auth.loginUser import login_auth
from app.controllers.auth.logoutUser import logout_auth
from app.controllers.auth.refreshToken import refresh_auth
from app.controllers.quiz.quiz import quiz_auth

# auth routes
app.register_blueprint(register_auth, url_prefix='/v1')
app.register_blueprint(login_auth, url_prefix='/v1')
app.register_blueprint(logout_auth, url_prefix='/v1')
app.register_blueprint(refresh_auth, url_prefix='/v1')

# home routes
app.register_blueprint(quiz_auth)
