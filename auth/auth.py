import sys, os, time, datetime, smtplib, urlparse
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from env_config import FROMEMAIL, FROMPASS, TOEMAIL

from User import User

auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates',url_prefix='')

@auth_flask_login.route("/_login", methods=["GET", "POST"])
def login():

    
    if request.method == "POST" and "email" in request.form:
        email = request.form.get('email')
        userObj = User()
        user = userObj.get_by_email(email)
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

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/auth/login.html", data=data)

#
# Route disabled - enable route to allow user registration.
#
@auth_flask_login.route("/_register", methods=["GET","POST"])
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
            print "Notice: Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
            flash("unable to register with that email address")
            current_app.logger.error("Error on registration - possible duplicate emails")
        
    return render_template("/auth/register.html")

@auth_flask_login.route("/_forgot", methods=["GET", "POST"])
def forgot():


    if request.method == 'POST' and request.form.get('email'):

        email = request.form.get('email')
        userObj = User()
        user = userObj.get_by_email(email)
        print(user)

        if user and user.is_active():

            try:

                o = urlparse.urlparse(request.url)
                host_url=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()

                #Next, log in to the server
                server.login(FROMEMAIL, FROMPASS)

                #Send the mail
                msg = "\r\n".join([
                  "From:"+FROMEMAIL,
                  "To: "+TOEMAIL,
                  "Subject: Password Recovery Email for"+user.email,
                  "",
                  "Click here <a href='"+host_url+"/_recoverpass?token=qwerty12345'>qwerty12345</a>"
                  ])
                #msg = "\nHello!" # The /n separates the message from the headers
                server.sendmail(FROMEMAIL, TOEMAIL, msg)
                server.quit()


                print("Sending password recovery email to: "+user.email)
                flash("Please check your mail's inbox for the password recovery instructions.")
                

            except:
                print("Error sending password revovery email")
                flash("There was an error sending the password recovery instructions")
                pass

        else:
            flash("Could not find this email")
            
        
    data = {}

    
    return render_template("/auth/forgot.html", data=data)


@auth_flask_login.route("/_reauth", methods=["GET", "POST"])
@login_required
def reauth():

    return render_template("/auth/reauth.html")


@auth_flask_login.route("/_logout")
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/_login')



@login_manager.unauthorized_handler
def unauthorized_callback():

    return redirect('/_login')

@login_manager.user_loader
def load_user(id):

    print('load_user id is:')
    print(id)

    if id is None:
        redirect('/_login')
    user = User()
    user.get_by_id(id)
    if user.is_active():
        return user
    else:
        return None
    


