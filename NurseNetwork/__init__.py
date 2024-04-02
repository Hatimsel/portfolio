#!/usr/bin/python3
""""""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from NurseNetwork.config import Config
import os


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail(app)

from NurseNetwork.users.routes import users
from NurseNetwork.services.routes import services
from NurseNetwork.appointments.routes import appointments
from NurseNetwork.reviews.routes import reviews
from NurseNetwork.main.routes import main


app.register_blueprint(users)
app.register_blueprint(services)
app.register_blueprint(appointments)
app.register_blueprint(reviews)
app.register_blueprint(main)


# with app.app_context():
#     db.drop_all()
#     db.create_all()
