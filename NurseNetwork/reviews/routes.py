#!/usr/bin/python3

from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user, login_required
from NurseNetwork import db
from NurseNetwork.models import Appointment, Review, User, Nurse, Patient
from NurseNetwork.reviews.forms import ReviewForm


reviews = Blueprint('reviews', __name__)


@reviews.route("/appointments/<id>/new_review", methods=['GET', 'POST'],
               strict_slashes=False)
@login_required
def new_review(id):
    form = ReviewForm()
    if form.validate_on_submit():
        appointment = Appointment.query.filter_by(id=id).first()
        description = form.feedback.data
        stars = int(form.stars.data)
        new_review = Review(appointment_id=appointment.id,
                            nurse_id=appointment.nurse_id,
                            description=description,
                            stars=stars)
        db.session.add(new_review)
        db.session.commit()
        flash('Review added successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_review.html',
                           title='New review',
                           form=form)


@reviews.route('/account/<id>/reviews', methods=['GET'],
               strict_slashes=False)
@reviews.route('/account/<id>/reviews/<review_id>', methods=['GET'],
           strict_slashes=False)
def retrieve_reviews(id, review_id=None):
    if review_id:
        review = Review.query.filter_by(id=review_id).first()
        if review:
            return render_template(
                'reviews.html', reviews=reviews, User=User,
                Nurse=Nurse, Patient=Patient, Appointment=Appointment
            )
            # return jsonify(review.to_dict())
        flash('Review not found!')
        return redirect(url_for('main.home'))
    if current_user.user_type == 'nurse':
        nurse = Nurse.query.filter_by(user_id=id).first()
        if nurse:
            reviews = nurse.reviews
            return render_template(
                'reviews.html', reviews=reviews, User=User,
                Nurse=Nurse, Patient=Patient, Appointment=Appointment
            )
        flash('Nurse not found!')
    return redirect(url_for('main.home'))
