from flask import Flask, url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from pymongo import MongoClient
import os
# Initialize application
template_dir = os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__))))
static_dir = os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__))))

template_dir = os.path.join(template_dir, 'Frontend')
template_dir = os.path.join(template_dir, 'templates')

static_dir = os.path.join(static_dir, 'Frontend')
static_dir = os.path.join(static_dir, 'static')
print("template directory :", template_dir)
print("static directory :", static_dir)


app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

app.config['SECRET_KEY'] = 'super secret key'

# Initialized Database Connection

try:
    db = MongoClient(host="localhost", port=27017)
    # create new database
    DB = db["Blog"]
    print("**********************************")
    print("Database Connected Successfully !!")
    print("**********************************")

except Exception as e:
    print("[Error while connecting with Database] :", e)
# Enabling cors
CORS(app)

# Initialize application views
from app import views

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# initialized all routes
from app.routes import *
