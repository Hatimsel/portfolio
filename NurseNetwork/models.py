#!/usr/bin/python3
""""""
from datetime import datetime
from hashlib import md5
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from NurseNetwork import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


time = "%Y-%m-%d"


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        """
        Returns the instance representation
        """
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__
        of the instance
        """
        dic = self.__dict__.copy()
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        if "password" in dic:
            del dic["password"]
        if "created_at" in dic:
            dic["created_at"] = dic["created_at"].strftime(time)
        dic['__class__'] = type(self).__name__
        return dic


class User(BaseModel, db.Model, UserMixin):
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.Enum('nurse', 'patient'), nullable=False)

    infos = db.relationship('Infos', backref='user', lazy=True)
    nurses = db.relationship('Nurse', backref='user', lazy=True)
    patients = db.relationship('Patient', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Infos(BaseModel, db.Model):
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Nurse(BaseModel, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    services = db.relationship('Service', backref='nurse', lazy=True)
    appointments = db.relationship('Appointment', backref='nurse', lazy=True)
    reviews = db.relationship('Review', backref='nurse', lazy=True)


class Patient(BaseModel, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)


class Service(BaseModel, db.Model):
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(1500), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey('nurse.id'),
                         nullable=False)


class Appointment(BaseModel, db.Model):
    nurse_id =  db.Column(db.Integer, db.ForeignKey('nurse.id'),
                          nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'),
                           nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'),
                           nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    reviews = db.relationship('Review', backref='appointment', lazy=True)


class Review(BaseModel, db.Model):
    description = db.Column(db.String(1500), nullable=True)
    stars = db.Column(db.Integer, nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'),
                               nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey('nurse.id'),
                         nullable=False)
