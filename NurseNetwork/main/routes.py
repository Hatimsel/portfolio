#!/usr/bin/python3

from flask import render_template, request, Blueprint
from NurseNetwork.models import Service, User, Nurse

main = Blueprint('main', __name__)


# with app.app_context():
#     db.drop_all()
#     db.create_all()

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.created_at.desc())\
            .paginate(per_page=10, page=page)
    return render_template('home.html', services=services,
                           User=User, Nurse=Nurse)


@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/privacy")
def privacy():
    return render_template('privacy.html')

