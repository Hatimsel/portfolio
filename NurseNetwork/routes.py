#!/usr/bin/python3
""""""
import secrets
import os
from flask import jsonify, abort, request
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from NurseNetwork import app, db, bcrypt, Mail
from NurseNetwork.forms import RegistrationForm, LoginForm, UpdateAccountForm, ServiceForm, RequestResetForm, ResetPasswordForm
from NurseNetwork.models import User, Nurse, Patient, Service, Appointment, Review, Infos


@app.route('/users', methods=['GET'], strict_slashes=False)
@app.route('/users/<id>', methods=['GET'], strict_slashes=False)
def retrieve_users(id=None):
    if id:
        user = User.query.filter_by(id=id).first()
        if user:
            return jsonify(user.to_dict())
        abort(404)
    else:
        users = User.query.all()
        users_tojson = []
        for i in range(0, len(users)):
            users_tojson.append(users[i].to_dict())
        return jsonify(users_tojson)


@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    if not request.get_json():
        abort(400)
    required_params = ['username', 'email', 'password', 'user_type']
    for param in required_params:
        if param not in request.get_json():
            return jsonify({"error":f"Missing {param}!"})
    new_user = User(**request.get_json())
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User created successfully!"})



@app.route('/users/<id>/infos', methods=['GET'], strict_slashes=False)
def retrieve_infos(id):
    infos = Infos.query.filter_by(user_id=id).first()
    if infos:
        return jsonify(infos.to_dict())
    return jsonify({"error":"No Infos found for this user!"})


@app.route('/users/<id>/infos', methods=['POST'], strict_slashes=False)
def add_infos(id):
    if not request.get_json():
        abort(400)
    required_params = ['age', 'gender', 'address', 'city']
    for param in required_params:
        if param not in request.get_json():
            return jsonify({"error":f"Missing {param}!"})
    dic = request.get_json()
    dic['user_id'] = id
    infos = Infos(**dic)
    db.session.add(infos)
    db.session.commit()
    return jsonify({"message":"Infos added successfully!"})


@app.route('/users/<id>/infos/<infos_id>', methods=['PUT'], strict_slashes=False)
def update_infos(id, infos_id):
    if not request.get_json():
        abort(400)
    infos = Infos.query.filter_by(id=infos_id).first()
    if infos:
        unchanged = ['id', 'user_id']
        for k, v in request.get_json():
            if k in unchanged:
                continue
            setattr(infos, k, v)
        return jsonify({"message":"Infos updated successfully!"})
    return jsonify({"error":"Infos not found!"})



@app.route('/nurses', methods=['GET'], strict_slashes=False)
@app.route('/nurses/<id>', methods=['GET'], strict_slashes=False)
def retrieve_nurses(id=None):
    if id:
        nurse = Nurse.query.filter_by(id=id).first()
        if nurse:
            return jsonify(nurse.to_dict())
        abort(404)
    else:
        nurses = Nurse.query.all()
        nurses_tojson = []
        for i in range(0, len(nurses)):
            nurses_tojson.append(nurses[i].to_dict())
        return jsonify(nurses_tojson)


@app.route('/nurses/<id>/services/', methods=['GET'], strict_slashes=False)
@app.route('/nurses/<id>/services/<service_id>', methods=['GET'],
           strict_slashes=False)
def retrieve_nurse_services(id, service_id=None):
    if service_id:
        service = Service.query.filter_by(id=service_id).first()
        if service:
            return jsonify(service.to_dict())
        abort(404)
    nurse = Nurse.query.filter_by(id=id).first()
    if nurse:
        services = nurse.services
        if len(services) > 0:
            services_tojson = []
            for i in range(0, len(services)):
                services_tojson.append(services[i].to_dict())
            return jsonify(services_tojson)
        return jsonify({"Error": "No services found!"})
    return jsonify({"Error": "Nurse not found!"})


@app.route('/nurses/<id>/services/', methods=['POST'], strict_slashes=False)
def create_service(id):
    if not request.get_json():
        abort(400)
    if "title" not in request.get_json():
        return jsonify({"error": "Missing title!"})
    if "price" not in request.get_json():
        return jsonify({"error": "Missing price!"})
    nurse = Nurse.query.filter_by(id=id).first()
    if not nurse:
        return jsonify({"error":"Nurse not found!"})
    new_service = Service(title=request.get_json()["title"],
                          price=request.get_json()["price"],
                          nurse_id=id)
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message":"Your service has been created successfully!"})


@app.route('/nurses/<id>/appointments', methods=['GET'], strict_slashes=False)
@app.route('/nurses/<id>/appointments/<appointment_id>', methods=['GET'],
           strict_slashes=False)
def retrieve_nurse_appointments(id, appointment_id=None):
    if appointment_id:
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        if appointment:
            return jsonify(appointment.to_dict())
        return jsonify({"error":"Appointment not found!"})
    nurse = Nurse.query.filter_by(id=id).first()
    if nurse:
        appointments = nurse.appointments
        if len(appointments) > 0:
            appointments_tojson = []
            for i in range(0, len(appointments)):
                appointments_tojson.append(appointments[i].to_dict())
            return jsonify(appointments_tojson)
        return jsonify({"message":"0 appointments!"})
    return jsonify({"error":"Nurse not found!"})


@app.route('/nurses/<id>/appointments', methods=['POST'], strict_slashes=False)
def create_appointment(id):
    if not request.get_json():
        abort(404)
    if "patient_id" not in request.get_json():
        return jsonify({"error":"Missing patient_id"})
    if "service_id" not in request.get_json():
        return jsonify({"error":"Missing service_id"})

    nurse = Nurse.query.filter_by(id=id).first()
    if not nurse:
        return jsonify({"error":"Nurse not found!"})
    new_appointment = Appointment(nurse_id=id,
                      patient_id=request.get_json()["patient_id"],
                      service_id=request.get_json()["service_id"])
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message":"Your Appointment has been created successfully!"})


@app.route('/nurses/<id>/appointments/<appointment_id>', methods=['DELETE'],
           strict_slashes=False)
def delete_appointment(id, appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message":"Appointment deleted successfully!"})
    return jsonify({"error":"Appointment not found!"})


@app.route('/nurses/<id>/appointments/<appointment_id>', methods=['PUT'],
           strict_slashes=False)
def update_appointment(id, appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if appointment:
        for k, v in request.get_json().items():
            setattr(appointment, k, v)
        db.session.commit()
        return jsonify({"message":"Appointment updated successfully!"})
    return jsonify({"error":"Appointment not found!"})


@app.route('/nurses/<id>/reviews', methods=['GET'], strict_slashes=False)
@app.route('/nurses/<id>/reviews/<review_id>', methods=['GET'],
           strict_slashes=False)
def retrieve_nurse_reviews(id, review_id=None):
    if review_id:
        review = Review.query.filter_by(id=review_id).first()
        if review:
            return jsonify(review.to_dict())
        return jsonify({"error":"Review not found!"})
    nurse = Nurse.query.filter_by(id=id).first()
    if nurse:
        reviews = nurse.reviews
        if len(reviews) > 0:
            reviews_tojson = []
            for i in range(0, len(reviews)):
                reviews_tojson.append(reviews[i].to_dict())
            return jsonify(reviews_tojson)
        return jsonify({"message":"No reviews found!"})
    return jsonify({"message":"Nurse not found!"})


@app.route('/nurses/<id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(id):
    if not request.get_json():
        abort(404)
    if "appointment_id" not in request.get_json():
        return jsonify({"error":"Missing appointment_id"})
    if "stars" not in request.get_json():
        return jsonify({"error":"Missing stars"})

    if not Nurse.query.filter_by(id=id).first():
        return jsonify({"error":"Nurse not found!"})
    new_review = Review(nurse_id=id,
                      appointment_id=request.get_json()["appointment_id"],
                      stars=request.get_json()["stars"])
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message":"Your review has been created successfully!"})


@app.route('/nurses/<id>/reviews/<review_id>', methods=['DELETE'],
           strict_slashes=False)
def delete_review(id, review_id):
    review = Review.query.filter_by(id=review_id).first()
    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message":"Review deleted successfully!"})
    return jsonify({"error":"Review not found!"})


@app.route('/nurses/<id>/reviews/<review_id>', methods=['PUT'],
           strict_slashes=False)
def update_review(id, review_id):
    review = Review.query.filter_by(id=review_id).first()
    if review:
        for k, v in request.get_json().items():
            setattr(review, k, v)
        db.session.commit()
        return jsonify({"message":"Review updated successfully!"})
    return jsonify({"error":"Review not found!"})


@app.route('/services', methods=['GET'], strict_slashes=False)
def retrieve_services():
    services = Service.query.all()
    if len(services) > 0:
        services_tojson = []
        for i in range(0, len(services)):
            services_tojson.append(services[i].to_dict())
        return jsonify(services_tojson)
    return jsonify({"message":"0 Services"})


@app.route('/reviews', methods=['GET'], strict_slashes=False)
@app.route('/reviews/<id>', methods=['GET'], strict_slashes=False)
def retrieve_reviews(id=None):
    if id:
        review = Review.query.filter_by(id=id).first()
        if review:
            return jsonify(review.to_dict())
        return jsonify({"error":"Review not found!"})
    reviews = Review.query.all()
    if len(reviews) > 0:
        reviews_tojson = []
        for i in range(0, len(reviews)):
            reviews_tojson.append(reviews[i].to_dict())
        return jsonify(reviews_tojson)
    return jsonify({"message":"0 Reviews"})
