#!/usr/bin/python3
"""
Review forms
"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    """Review class"""
    feedback = TextAreaField('Feedback')
    stars = IntegerField('Stars', validators=[
                        validators.NumberRange(
                        min=0, max=5, message="Value must be between 0 and 5"
                        ),
                        DataRequired()])
    submit = SubmitField('Submit Review')
