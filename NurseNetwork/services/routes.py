#!/usr/bin/python3
"""
Service routes
"""
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from flask_login import current_user, login_required
from NurseNetwork import db
from NurseNetwork.models import Service, User, Nurse
from NurseNetwork.services.forms import ServiceForm


services = Blueprint('services', __name__)


@services.route("/service/new", strict_slashes=False, methods=['GET', 'POST'])
@login_required
def new_service():
    """Creates a new service"""
    if current_user.user_type != 'nurse':
        abort(403)
    form = ServiceForm()
    if form.validate_on_submit():
        nurse = Nurse.query.filter_by(user_id=current_user.id).first()
        new_service = Service(title=form.title.data,
                              description=form.description.data,
                              price=form.price.data,
                              nurse_id=nurse.id)
        db.session.add(new_service)
        db.session.commit()
        flash('Your service has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_service.html', title='New Service', form=form)


@services.route("/service/<id>", strict_slashes=False,
           methods=['GET'])
def service(id):
    """Retrieves a service"""
    service = Service.query.get_or_404(id)
    return render_template('service.html', title=service.title,
                           service=service, Nurse=Nurse, User=User)


@services.route("/service/<id>/update", strict_slashes=False,
           methods=['Get', 'POST'])
@login_required
def update_service(id):
    """Updates a service"""
    service = Service.query.get_or_404(id)
    nurse = Nurse.query.get_or_404(service.nurse_id)
    user = User.query.get_or_404(nurse.user_id)
    if user != current_user:
        abort(403)
    form = ServiceForm()
    if form.validate_on_submit():
        service.title = form.title.data
        service.description = form.description.data
        service.price = form.price.data
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('services.service', id=service.id))
    return render_template('update_service.html', title='Update service',
                           service=service, nurse=nurse, user=user,
                           form=form)


@services.route("/service/<id>/delete", strict_slashes=False,
           methods=['POST'])
@login_required
def delete_service(id):
    """Deletes a service"""
    service = Service.query.get_or_404(id)
    nurse = Nurse.query.get_or_404(service.nurse_id)
    user = User.query.get_or_404(nurse.user_id)
    if user != current_user:
        abort(403)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully', 'success')
    return redirect(url_for('main.home'))


@services.route('/nurses/<id>/services/', methods=['GET'], strict_slashes=False)
@services.route('/nurses/<id>/services/<service_id>', methods=['GET'],
           strict_slashes=False)
def retrieve_nurse_services(id, service_id=None):
    """Retrieves services assigned to a particular nurse"""
    if service_id:
        service = Service.query.filter_by(id=service_id).first()
        if service:
            return render_template('nurse_service.html', services=service,
                                   Nurse=Nurse, User=User)
        abort(404)
    nurse = Nurse.query.filter_by(user_id=id).first()
    services = nurse.services
    if len(services) > 0:
        services_tojson = []
        for i in range(0, len(services)):
            services_tojson.append(services[i].to_dict())
        return render_template('nurse_service.html', services=services_tojson,
                               Nurse=Nurse, User=User)
    flash('No services found!')
    return redirect(url_for('main.home'))
