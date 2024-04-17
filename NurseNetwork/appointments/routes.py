#!/usr/bin/python3
"""
Appointment routes
"""
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import current_user, login_required
from NurseNetwork import db
from NurseNetwork.models import Service, Appointment, Patient, User, Nurse
from NurseNetwork.appointments.forms import AppointmentForm


appointments = Blueprint('appointments', __name__)


@appointments.route("/service/<id>/book_appointment", methods=['GET', 'POST'],
                    strict_slashes=False)
@login_required
def book_appointment(id):
    """Books a new appointment"""
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
        else:
            flash('A nurse cannot book appointments', 'danger')
            return redirect(url_for('main.home'))
    return render_template('new_appointment.html',
                           title='New Appointment',
                           form=form)


@appointments.route('/account/<id>/appointments', methods=['GET'],
                    strict_slashes=False)
@login_required
def retrieve_appointments(id):
    """Retrieves an appointment"""
    if current_user.user_type == 'nurse':
        nurse = Nurse.query.filter_by(user_id=id).first()
        if nurse:
            appointments = nurse.appointments
            return render_template(
                'nurse_appointments.html', appointments=appointments,
                User=User, Nurse=Nurse, Patient=Patient, Service=Service
            )
        flash('Not found!')
        return render_template(url_for('main.home'))
    patient = Patient.query.filter_by(user_id=id).first()
    if patient:
        appointments = patient.appointments
        return render_template(
            'patient_appointments.html', appointments=appointments,
            User=User, Nurse=Nurse, Patient=Patient, Service=Service
        )
    flash('Not found!')
    return redirect(url_for('main.home'))
