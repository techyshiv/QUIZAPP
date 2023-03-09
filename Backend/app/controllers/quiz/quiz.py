from flask import request, render_template
from flask.views import MethodView
from flask import Blueprint
from app.services.customErrorHandler import customErrorHandler
from app.controllers.auth.helper import response
from app.services.JwtService import JWTService
from app import DB
from bson import ObjectId


quiz_auth = Blueprint('quiz_auth', __name__)


class Home(MethodView):
    """
    Home Page routes
    """

    def get(self):
        # check whether user is authenticated or not
        token = request.cookies.get('access_token')
        print("token :", token)
        if token is not None:
            decoded_token_response = JWTService.verify(
                token=token, token_name='access_token')
            print("Decoded token response")
            print(decoded_token_response)
            if (decoded_token_response['statusCode'] == 401):
                return render_template("login.html")
            user_id = decoded_token_response['data']['_id']
            result = DB.users.find_one({"_id": ObjectId(user_id)})
            username = result['firstname']
            return render_template("index.html", username=username)
        return render_template("signup.html")


class Quiz(MethodView):
    """
    Quiz Page routes
    """

    def get(self):
        # get data from database
        print("Query strings")
        print(request.query_string)
        print(request.args.get('points'))
        if request.args.get('points') is None:
            questionData = list(DB.questions.find({}, {'_id': False}))
            return render_template("quiz.html", data=questionData)
        points = request.args.get('points')
        username = request.args.get('username')
        time_taken = request.args.get('time_taken')
        return render_template("end.html", points=points, username=username, time_taken=time_taken)

    def post(self):
        try:
            if request.content_type == "application/json":
                # get all questions data
                req = request.get_json()
                print("received req")
                print(req)
                points = 0
                for ans in req:
                    ques = DB.questions.find_one({'id': ans['question_id']})
                    if (ques['answer'] == ans['answer']):
                        points += 10
                    else:
                        points -= 1
                return response('success', points, 200)
            return response('failed', 'Content-type must be json', 403)
        except Exception as e:
            return response('failed', customErrorHandler.serverError, 500)


class Question(MethodView):
    """
    Admin can create Questions
    """

    def post(self):
        try:
            if request.content_type == "application/json":
                # get all questions data
                req = request.get_json()
                req = [ques for ques in req if DB.questions.find_one(
                    {'question': ques['question']}) is None]
                print("After Filter Request Data are:")
                if (len(req) > 0):
                    DB.questions.insert_many(req)
                else:
                    print("ALl Questions present")
                return response('success', 'Questions Added Successfully !!', 201)
            return response('failed', 'Content-type must be json', 403)
        except Exception as e:
            return response('failed', customErrorHandler.serverError, 500)


index_view = Home.as_view('home')
quiz_auth.add_url_rule('/', view_func=index_view, methods=['GET'])

quiz_view = Quiz.as_view('quiz')
quiz_auth.add_url_rule('/quiz', view_func=quiz_view, methods=['GET', 'POST'])

question_view = Question.as_view('question')
quiz_auth.add_url_rule('/question', view_func=question_view, methods=['POST'])
