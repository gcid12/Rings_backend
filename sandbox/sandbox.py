import sys, os, time, datetime, smtplib, urlparse, random
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

sandbox = Blueprint('sandbox', __name__, template_folder='templates',url_prefix='/_sandbox')

@sandbox.route("/s1", methods=["GET", "POST"])
def s1():

    flash("User not active")

    data = {}
    #t = time.time()
    data['section_name']= "unoname"
    
    return render_template("/sandbox/uno.html", data=data)



@sandbox.route("/landing", methods=["GET", "POST"])
#@login_required
def landing():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= ""
    
    return render_template("/sandbox/landing.html", data=data)



@sandbox.route("/landing_tech", methods=["GET", "POST"])
#@login_required
def landing_tech():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Tech Landing"
    
    return render_template("/sandbox/landing_tech.html", data=data)



@sandbox.route("/landing_orgs", methods=["GET", "POST"])
#@login_required
def landing_orgs():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Organizations Landing"
    
    return render_template("/sandbox/landing_orgs.html", data=data)



@sandbox.route("/landing_travel", methods=["GET", "POST"])
#@login_required
def landing_travel():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Travel Landing"
    
    return render_template("/sandbox/landing_travel.html", data=data)


@sandbox.route("/landing_freelance", methods=["GET", "POST"])
#@login_required
def landing_freelance():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Freelance Landing"
    
    return render_template("/sandbox/landing_freelance.html", data=data)


# A. INVITE FROM MYRING

@sandbox.route("/landing_a", methods=["GET", "POST"])
#@login_required
def landing_a():

    flash("User not active")

    data = {}
    data['section_name']= "Signing up first time"
    data['t00']= "a"
    data['t01']= "Hey welcome to MyRing"
    data['t02']= "Please complete your registration"
    
    return render_template("/sandbox/landing_invite.html", data=data)



# B. INVITE FROM INDIVIDUAL
@sandbox.route("/landing_b", methods=["GET", "POST"])
def landing_b():  

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Invitation"
    data['t00']= "b"
    data['t01']= "Hey Jon, Thanks for accepting my invite/ RZ invite"
    data['t02']= "Please complete your registration"
    
    return render_template("/sandbox/landing_invite.html", data=data)





@sandbox.route("/terms", methods=["GET", "POST"])
#@login_required
def terms():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Terms & Conditions"
    
    return render_template("/sandbox/terms.html", data=data)




##########      MAILS    




@sandbox.route("/mail_welcome", methods=["GET", "POST"])
#@login_required
def mail_welcome():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Welcome mail"
    
    return render_template("/sandbox/mail_welcome.html", data=data)  




@sandbox.route("/mail_welcome2", methods=["GET", "POST"])
#@login_required
def mail_welcome2():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Welcome"
    
    return render_template("/sandbox/mail_welcome2.html", data=data)  



@sandbox.route("/mail_recover", methods=["GET", "POST"])
#@login_required
def mail_recover():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/sandbox/mail_recover.html", data=data)  




@sandbox.route("/mail_invite", methods=["GET", "POST"])
#@login_required
def mail_invite():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Invite"
    
    return render_template("/sandbox/mail_invite.html", data=data) 


@sandbox.route("/mail_invite_r1", methods=["GET", "POST"])
#@login_required
def mail_invite_r1():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Invite reminder 1"
    
    return render_template("/sandbox/mail_invite_r1.html", data=data) 




@sandbox.route("/mail_invite_r2", methods=["GET", "POST"])
#@login_required
def mail_invite_r2():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Invite reminder 2"
    
    return render_template("/sandbox/mail_invite_r2.html", data=data) 





@sandbox.route("/mail_achievement", methods=["GET", "POST"])
#@login_required
def mail_achievement():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "Achievement"
    
    return render_template("/sandbox/mail_achievement.html", data=data)  



@sandbox.route("/mail_firsttime", methods=["GET", "POST"])
#@login_required
def mail_firsttime():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    data['section_name']= "First Time"
    
    return render_template("/sandbox/mail_firsttime.html", data=data) 



@sandbox.route("/mail_retention", methods=["GET", "POST"])
#@login_required
def mail_retention():

    flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/sandbox/mail_retention.html", data=data) 


@sandbox.route("/examples", methods=["GET", "POST"])
#@login_required
def examples():

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/sandbox/examples.html", data=data) 





@sandbox.route("/launchpad", methods=["GET", "POST"])
#@login_required
def launchpad():

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/sandbox/launchpad.html", data=data) 



# MBF


@sandbox.route("/mbf_login", methods=["GET", "POST"])
#@login_required
def mbf_login():

    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_login.html", data=data) 


@sandbox.route("/mbf_signup", methods=["GET", "POST"])
#@login_required
def mbf_signup():

    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_signup.html", data=data) 



@sandbox.route("/mbf_home", methods=["GET", "POST"])
#@login_required
def mbf_home():
    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_home.html", data=data) 


@sandbox.route("/mbf_categories", methods=["GET", "POST"])
#@login_required
def mbf_categories():
    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_categories.html", data=data) 


@sandbox.route("/mbf_developers", methods=["GET", "POST"])
#@login_required
def mbf_developers():
    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_developers.html", data=data) 

@sandbox.route("/mbf_experts", methods=["GET", "POST"])
#@login_required
def mbf_experts():
    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_experts.html", data=data) 



@sandbox.route("/mbf_how", methods=["GET", "POST"])
#@login_required
def mbf_how():
    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_how.html", data=data) 



@sandbox.route("/mbf_pricing", methods=["GET", "POST"])
#@login_required
def mbf_how():
    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_pricing.html", data=data) 







@sandbox.route("/wiz_org", methods=["GET", "POST"])
#@login_required
def wiz_org():

    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/wiz_org.html", data=data) 









    


