#!/usr/bin/python3

import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from NurseNetwork import app, mail
from NurseNetwork.models import User


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@gmail.com',
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request, please ignore this email
    """
    mail.send(msg)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/', picture_fn)
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn
