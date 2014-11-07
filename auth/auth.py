import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)



auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates',url_prefix='')

@auth_flask_login.route("/login", methods=["GET", "POST"])
def login():

    return render_template("/auth/login.html")

#
# Route disabled - enable route to allow user registration.
#
@auth_flask_login.route("/register", methods=["GET","POST"])
def register():
	


	return render_template("/auth/register.html")

@auth_flask_login.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():

    return render_template("/auth/reauth.html")


@auth_flask_login.route("/logout")
@login_required
def logout():
    
    return redirect('/login')

@login_manager.unauthorized_handler
def unauthorized_callback():

	return redirect('/login')

@login_manager.user_loader
def load_user(id):
	return None

