import sys, os, time, datetime, smtplib, urlparse, random
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

sandbox = Blueprint('sandbox', __name__, template_folder='templates',url_prefix='/_sandbox')

@sandbox.route("/s1", methods=["GET", "POST"])
def s1():


    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/sandbox/uno.html", data=data)



@sandbox.route("/s2", methods=["GET", "POST"])
@login_required
def s2():


    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/sandbox/uno.html", data=data)



    


