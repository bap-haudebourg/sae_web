from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os.path

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname( __file__ ),p))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../BD/DB_Fest.db'))

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '94da14e7-22ba-424c-b262-f5eeb505e5e9'
app.config['UPLOAD_FOLDER'] = 'static/document'

login_manager = LoginManager(app)
login_manager.login_view = "login"