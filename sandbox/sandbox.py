import sys, os, time, datetime, smtplib, urlparse, random, requests, json
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from auth.User import User

sandbox = Blueprint('sandbox', __name__, template_folder='templates',url_prefix='/_widget')

def login_user_by_email(email,username):

    
    userObj = User(email=email)
    userview = userObj.get_user()
    print(userObj)

    mpp = {'status':'OK'}
    flash({'f':'track','v':'_register','p':mpp},'MP')
    flash({'f':'alias','v':username},'MP')

    if login_user(userObj, remember="no"):
        flash("Logged in. Welcome to MyRing!",'UI')

        mpp = {'status':'OK','msg':'Automatic'}
        flash({'f':'track','v':'_login','p':mpp},'MP')
        #flash({'track':'_login OK, Automatic'},'MP')
        #return redirect('/'+userview.id+'/_home') 
        return True 

    else:
        flash("Please enter your credentials ",'UI')

        mpp = {'status':'KO','msg':'Automatic'}
        flash({'f':'track','v':'_login','p':mpp},'MP') 
        #flash({'track':'_login KO, Automatic'},'MP')

        #return redirect('/_login')
        return False




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
    data['mask']= "mbf"
    
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


@sandbox.route("/mbf_signup", methods=["GET"])
#@login_required
def mbf_signup():

    data = {}
    #data['mask']= "mbf"

    return render_template("/sandbox/mbf_signup.html", data=data) 



@sandbox.route("/mbf_signup", methods=["POST"])
#@login_required
def mbf_signup_post():

    #Coming via POST: username,email,password,confirm,orgusername    

    complete = 0

    if 'username' in request.form:
        username = request.form.get('username')
        complete += 1

    if 'email' in request.form:
        email = request.form.get('email')
        complete += 1

    if 'password' in request.form:
        password = request.form.get('password')
        complete += 1

    if 'confirm' in request.form:
        confirm = request.form.get('confirm')
        complete += 1

    if 'orgusername' in request.form:
        orgusername = request.form.get('orgusername')
        complete += 1

    if complete == 5:

        try:
            # _api/_register . Create the user
            print('r1')
            api_url = 'http://0.0.0.0:8080/_api/_register?token=qwerty1234'
            payload = {'username':username, 'email':email, 'password':password, 'confirm':confirm}
            r1 = requests.post(api_url,data=payload)
            print(r1.text)
            q1 = json.loads(r1.text)
            print(q1)

            login_result = login_user_by_email(email,username)


            if q1['Success']:
                print('r2')
                flash(q1['Message'],'UI')
                # _api/_orgregister . Create the organization
                api_url = 'http://0.0.0.0:8080/_api/_orgregister?token=qwerty1234'
                payload = {'username':orgusername, 'email':email, 'owner':username}
                r2 = requests.post(api_url,data=payload)
                print(r2.text)
                q2 = json.loads(r2.text)

                if q2['Success']:
                    print('r3')
                    flash(q2['Message'],'UI')
                    # _api/USER/_collections . Create the collection
                    api_url = 'http://0.0.0.0:8080/_api/'+orgusername+'/_collections?token=qwerty1234'
                    colname = 'business_facts'
                    payload = {'CollectionName':colname}
                    r3 = requests.post(api_url,data=payload)
                    print(r3.text)
                    q3 = json.loads(r3.text)

                    if q3['Success']:
                        print('r4')
                        flash(q3['Message'],'UI')
                        # Create the ring in the collection
                        api_url = 'http://0.0.0.0:8080/_api/'+orgusername+'/_collections/'+colname+'?token=qwerty1234'
                        ringurl = 'http://0.0.0.0:8080/_api/blalab/arboles'
                        payload = {'ringurl':ringurl}
                        r4 = requests.post(api_url,data=payload)
                        print(r4.text)
                        q4 = json.loads(r4.text)

                        if q4['Success']:
                            print('r5')
                            flash(q4['Message'],'UI')
                        else: 
                            # The rings could not be added
                            flash(q4['Message'],'ER')

                            #THIS SHOULD LOGIN THE USER, GO TO THE ORG ANYWAY. THE NEXT STEP WILL CHECK AND REPAIR IF NEEDED
                            return redirect('/_sandbox/mbf_signup')
                    else:
                        # The collection could not be created
                        flash(q3['Message'],'ER')

                        #THIS SHOULD LOGIN THE USER, GO TO THE ORG ANYWAY. THE NEXT STEP WILL CHECK AND REPAIR IF NEEDED
                        return redirect('/_sandbox/mbf_signup')
                else:
                    # The org could not be created
                    flash(q2['Message'],'ER')

                    #THIS SHOULD LOGIN THE USER AND SHOW PARTIAL mbf_signup => ORGUSERNAME PART ONLY
                    return redirect('/_sandbox/mbf_signup?orgusername='+orgusername)
            else:
                # The user could not be created
                flash(q1['Message'],'ER')

                return redirect('/_sandbox/mbf_signup?username='+username+'&email='+email+'&orgusername='+orgusername)

        except:
            print "Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
            print('There was an API exception. 500')
            flash('There was an API exception. 500','ER')
            data = {}
            return render_template("/sandbox/mbf_signup.html", data=data) 
        #r = requests.get('http://localhost:8080/_api/blalab2/reactivoexamen_0-1-2')             
        
        #print('Raw JSON schema:')
        #print(r.text)
        #schema = json.loads(r.text)
    
    else:

        flash('You need to send all the parameters =)')
        return render_template("/sandbox/mbf_signup.html", data=data) 

    data = {}
    #data['mask']= "mbf"

    if login_result and q2['Success']:
        return redirect('/'+orgusername)
    elif q2['Success']: 
        return redirect('/_login?org='+orgusername)
    else:
        return redirect('/_login')



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
def mbf_pricing():
    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/mbf_pricing.html", data=data) 







@sandbox.route("/wiz_org", methods=["GET", "POST"])
#@login_required
def wiz_org():

    data = {}
    data['mask']= "mbf"

    return render_template("/sandbox/wiz_org.html", data=data) 











    


