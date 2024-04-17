#!/usr/bin/python3
"""
Appointment forms
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, validators
from wtforms.validators import DataRequired
from wtforms.fields import DateField


class AppointmentForm(FlaskForm):
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d',
                                 validators=[DataRequired()])
    submit = SubmitField('Book Appointment')
