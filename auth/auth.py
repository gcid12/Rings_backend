import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

from User import User

auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates',url_prefix='')

@auth_flask_login.route("/login", methods=["GET", "POST"])
def login():

    
    if request.method == "POST" and "email" in request.form:
        email = request.form.get('email')
        userObj = User()
        user = userObj.get_by_email_w_password(email)
        print(user)
        if user and flask_bcrypt.check_password_hash(user.password,request.form.get('password')) and user.is_active():
            remember = request.form.get("remember", "no") == "yes"
            if login_user(userObj, remember=remember):
                flash("Logged in!")
                #flash("Redirecting to : /"+user.id)
                return redirect('/'+user.id)
            else:
                flash("unable to log you in")
        else:
            flash("User/Password is not correct")
    

    return render_template("/auth/login.html")

#
# Route disabled - enable route to allow user registration.
#
@auth_flask_login.route("/register", methods=["GET","POST"])
def register():

    #registerForm = forms.SignupForm(request.form)
    #current_app.logger.info(request.form)

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')

        # generate password hash
        password_hash = flask_bcrypt.generate_password_hash(request.form.get('password'))

        # prepare User
        user = User(username,email,password_hash)
        print user

        try:
            user.save()
            if login_user(user, remember="no"):
                flash("Logged in!")
                return redirect('/tools')
            else:
                flash("unable to log you in")

        except:
            flash("unable to register with that email address")
            current_app.logger.error("Error on registration - possible duplicate emails")
        
    return render_template("/auth/register.html")


@auth_flask_login.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():

    return render_template("/auth/reauth.html")


@auth_flask_login.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/login')

@login_manager.unauthorized_handler
def unauthorized_callback():

    return redirect('/login')

@login_manager.user_loader
def load_user(id):

    print('load_user id is:')
    print(id)

    if id is None:
        redirect('/login')
    user = User()
    user.get_by_id(id)
    if user.is_active():
        return user
    else:
        return None
    


