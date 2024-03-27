#!/usr/bin/python3

from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import current_user, login_required
from NurseNetwork import db
from NurseNetwork.models import Service, Appointment, Patient
from NurseNetwork.appointments.forms import AppointmentForm


appointments = Blueprint('appointments', __name__)


@appointments.route("/service/<id>/book_appointment", methods=['GET', 'POST'])
def book_appointment(id):
    form = AppointmentForm()
    if form.validate_on_submit():
        service = Service.query.filter_by(id=id).first()
        if current_user.user_type == 'patient':
            patient = Patient.query.filter_by(user_id=current_user.id).first()
        appointment_date = form.appointment_date.data
        new_appointment = Appointment(nurse_id=service.nurse_id,
                                      patient_id=patient.id,
                                      service_id=service.id,
                                      appointment_date=appointment_date)
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment booked successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('appointment.html',
                           title='Appointment',
                           form=form)
