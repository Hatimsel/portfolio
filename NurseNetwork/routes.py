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
# from flask_login import login_user, current_user, logout_user, login_required
# from flask_mail import Message
#
#
# with app.app_context():
#     db.create_all()
# @app.route("/")
# @app.route("/home")
# def home():
#     page = request.args.get('page', 1, type=int)
#     services = Service.query.order_by(Service.created_at.desc())\
#             .paginate(per_page=10, page=page)
#     return render_template('home.html', services=services,
#                            User=User, Nurse=Nurse)
#
#
# @app.route("/about")
# def about():
#     return render_template('about.html')
#
#
# @app.route("/privacy")
# def privacy():
#     return render_template('privacy.html')
#
#
# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         new_user = User(username=form.username.data, email=form.email.data,
#                         password=hashed_pwd, user_type=form.user_type.data)
#         db.session.add(new_user)
#         db.session.commit()
#
#         if new_user.user_type == 'nurse':
#             new_nurse = Nurse(user_id=new_user.id)
#             db.session.add(new_nurse)
#         else:
#             new_patient = Patient(user_id=new_user.id)
#             db.session.add(new_patient)
#         db.session.commit()
#
#         flash('Your account has been created! Please log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)
#
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             flash('You have been logged in!', 'success')
#             next_page = request.args.get('next')
#             return redirect(url_for(next_page.strip('/') if next_page else 'home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)
#
#
# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))
#
#
# @app.route("/service/new", strict_slashes=False, methods=['GET', 'POST'])
# @login_required
# def new_service():
#     if current_user.user_type != 'nurse':
#         abort(403)
#     form = ServiceForm()
#     if form.validate_on_submit():
#         nurse = Nurse.query.filter_by(user_id=current_user.id).first()
#         new_service = Service(title=form.title.data,
#                               description=form.description.data,
#                               price=form.price.data,
#                               nurse_id=nurse.id)
#         db.session.add(new_service)
#         db.session.commit()
#         flash('Your service has been created!', 'success')
#         return redirect(url_for('home'))
#     return render_template('create_service.html', title='New Service', form=form)
#
#
# @app.route("/service/<id>", strict_slashes=False,
#            methods=['GET'])
# def service(id):
#     service = Service.query.get_or_404(id)
#     return render_template('service.html', title=service.title,
#                            service=service, Nurse=Nurse, User=User)
#
#
# @app.route("/service/<id>/update", strict_slashes=False,
#            methods=['Get', 'POST'])
# @login_required
# def update_service(id):
#     service = Service.query.get_or_404(id)
#     nurse = Nurse.query.get_or_404(service.nurse_id)
#     user = User.query.get_or_404(nurse.user_id)
#     if user != current_user:
#         abort(403)
#     form = ServiceForm()
#     if form.validate_on_submit():
#         service.title = form.title.data
#         service.description = form.description.data
#         service.price = form.price.data
#         db.session.commit()
#         flash('Service updated successfully!', 'success')
#         return redirect(url_for('service', id=service.id))
#     return render_template('update_service.html', title='Update service',
#                            service=service, nurse=nurse, user=user,
#                            form=form)
#
#
# @app.route("/service/<id>/delete", strict_slashes=False,
#            methods=['POST'])
# @login_required
# def delete_service(id):
#     service = Service.query.get_or_404(id)
#     nurse = Nurse.query.get_or_404(service.nurse_id)
#     user = User.query.get_or_404(nurse.user_id)
#     if user != current_user:
#         abort(403)
#     db.session.delete(service)
#     db.session.commit()
#     flash('Service deleted successfully', 'success')
#     return redirect(url_for('home'))
#
# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request', sender='noreply@gmail.com',
#                   recipients=[user.email])
#     msg.body = f"""To reset your password, visit the following link:
#     {url_for('reset_token', token=token, _external=True)}
#     If you did not make this request, please ignore this email
#     """
#     mail.send(msg)
#
#
# @app.route("/reset_password", strict_slashes=False,
#            methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent to reset your password', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password',
#                            form=form)
#
#
# @app.route("/reset_password/<token>", strict_slashes=False,
#            methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid token', 'warning')
#         return redirect(url_for('reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_pwd
#         db.session.commit()
#
#         flash('Your password has been updated! Please log in', 'success')
#         return redirect(url_for('login'))
#
#     return render_template('reset_token.html', title='Reset Password',
#                            form=form)
#
#
# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/', picture_fn)
#     output_size = (125, 125)
#     image = Image.open(form_picture)
#     image.thumbnail(output_size)
#     image.save(picture_path)
#
#     return picture_fn
#
#
# @app.route("/account", methods=['GET', 'POST'])
# @login_required
# def account(id=None):
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.profile_pic.data:
#             picture_file = save_picture(form.profile_pic.data)
#             current_user.image_file = picture_file
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Account has been updated!', 'success')
#         return redirect(url_for('account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     image_file = url_for('static', filename=current_user.image_file)
#     return render_template('account.html', title='Account',
#                            image_file=image_file, form=form)
#
#
# @app.route("/profile/<user_id>", strict_slashes=False, methods=['GET'])
# def profile(user_id):
#     user = User.query.get_or_404(user_id)
#     nurse = Nurse.query.filter_by(user_id=user_id).first()
#     image_file = url_for('static', filename=user.image_file)
#     return render_template('profile.html', title='Profile',
#                            user=user, nurse=nurse,
#                            image_file=image_file)
# @app.route()


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
    # new_user = User(username=request.get_json()['username'],
    #               email=request.get_json()['email'],
    #               password=request.get_json()['password'],
    #               user_type=request.get_json()['user_type'])
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
    # infos = Infos(age=request.get_json()['age'],
    #               gender=request.get_json()['gender'],
    #               city=request.get_json()['city'],
    #               address=request.get_json()['address'],
    #               user_id=id)
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
    # if "nurse_id" not in request.get_json():
    #     return jsonify({"error": "Missing nurse_id!"})
    nurse = Nurse.query.filter_by(id=id).first()
    if not nurse:
        return jsonify({"error":"Nurse not found!"})
    new_service = Service(title=request.get_json()["title"],
                          price=request.get_json()["price"],
                          nurse_id=id)
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message":"Your service has been created successfully!"})


# @app.route('/nurses/<id>/services/<service_id>', methods=['DELETE'],
#            strict_slashes=False)
# def delete_service(id, service_id):
#     service = Service.query.filter_by(id=service_id).first()
#     if service:
#         db.session.delete(service)
#         db.session.commit()
#         return jsonify({"message": "Service deleted successfully!"})
#     return jsonify({"error":"Service not found!"})


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
