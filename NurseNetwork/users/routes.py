#!/usr/bin/python3

from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from NurseNetwork import db, bcrypt
from NurseNetwork.models import User, Service, Nurse, Patient
from NurseNetwork.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                    RequestResetForm, ResetPasswordForm)
from NurseNetwork.users.utils import save_picture, send_reset_email



users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_pwd, user_type=form.user_type.data)
        db.session.add(new_user)
        db.session.commit()

        if new_user.user_type == 'nurse':
            new_nurse = Nurse(user_id=new_user.id)
            db.session.add(new_nurse)
        else:
            new_patient = Patient(user_id=new_user.id)
            db.session.add(new_patient)
        db.session.commit()

        flash('Your account has been created! Please log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(url_for(next_page.strip('/') if next_page else 'main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/reset_password", strict_slashes=False,
           methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password',
                           form=form)


@users.route("/reset_password/<token>", strict_slashes=False,
           methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()

        flash('Your password has been updated! Please log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password',
                           form=form)

    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account(id=None):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/profile/<user_id>", strict_slashes=False, methods=['GET'])
def profile(user_id):
    user = User.query.get_or_404(user_id)
    nurse = Nurse.query.filter_by(user_id=user_id).first()
    image_file = url_for('static', filename=user.image_file)
    return render_template('profile.html', title='Profile',
                           user=user, nurse=nurse,
                           image_file=image_file)


@users.route('/users', methods=['GET'], strict_slashes=False)
@users.route('/users/<id>', methods=['GET'], strict_slashes=False)
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
