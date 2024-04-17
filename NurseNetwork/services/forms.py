#!/usr/bin/python3
"""
Service forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



class ServiceForm(FlaskForm):
    """Service form"""
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Create service')
