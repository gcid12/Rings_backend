import sys, os, time, datetime, smtplib, urlparse, random
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from env_config import FROMEMAIL, FROMPASS
from MainModel import MainModel

from User import User

auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates',url_prefix='')

@auth_flask_login.route("/_login", methods=["GET", "POST"])
def login():

    
    if request.method == "POST" and "email" in request.form:
        email = request.form.get('email')
        userObj = User(email=email)
        user = userObj.get_user()
        #print("user:")
        #print(user.password)
        #print(request.form.get('password'))
        #print(flask_bcrypt.check_password_hash(user.password,request.form.get('password')))
        #print(user)
        #print(userObj.is_active())
        if userObj.is_active():
            if user and flask_bcrypt.check_password_hash(user.password,request.form.get('password')):
                remember = request.form.get("remember", "no") == "yes"
                if login_user(userObj, remember=remember):
                    flash("Logged in!")
                    #flash("Redirecting to : /"+user.id)
                    return redirect('/'+user.id+'/_home')
                else:
                    flash("unable to log you in")
            else:
                flash("User/Password is not correct")
        else:
            flash("User not active")

    data = {}
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/auth/login.html", data=data)


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
        #if True:
            if user.set_user():

                #return redirect('/_login')
                print('Now log in the user')

                #Go through regular login process
                userObj = User(email=email)
                userview = userObj.get_user()
                print(userObj)
                if login_user(userObj, remember="no"):
                        flash("Logged in. Welcome to MyRing!")
                        #flash("Redirecting to : /"+user.id)
                        return redirect('/'+userview.id+'/_home')
      
                else:
                    flash("Please enter your credentials ")
                    return redirect('/_login')
            else:
                
                return redirect('/_register')


        except(KeyError):
        #else:
            print "Notice: Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
            flash("unable to register with that email address")
            current_app.logger.error("Error on registration ")
        
    data = {}

    return render_template("/auth/register.html", data=data)

@auth_flask_login.route("/_orgregister", methods=["GET","POST"])
@login_required
def orgregister():

    #registerForm = forms.SignupForm(request.form)
    #current_app.logger.info(request.form)

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')

        # Organizations use no passwords
        password_hash = ''

        # prepare User
        user = User(username,email,password_hash,current_user.id,True)
        print user

        #try:
        if True:
            user.set_user()
            return redirect('/'+username+'/_home')

        #except:
        else:
            print "Notice: Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
            flash("unable to register with that email address")
            current_app.logger.error("Error on registration ")
        
    data = {}

    MAM = MainModel()
    user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    if user_doc:
        data['handle'] = current_user.id
        data['actualname'] = user_doc['name']
        data['profilepic'] = user_doc['profilepic']
        data['location'] = user_doc['location']

    return render_template("/auth/orgregister.html", data=data)

@auth_flask_login.route("/_forgot", methods=["GET", "POST"])
def forgot():


    if request.method == 'POST' and request.form.get('email'):

        email = request.form.get('email')
        userObj = User(email=email)
        user = userObj.get_user()
        print(user)


        if user and user.is_active():

            try:

                o = urlparse.urlparse(request.url)
                host_url=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

                #save the token in the database
                key = flask_bcrypt.generate_password_hash(request.form.get('email')+str(random.randint(0,9999)))
                #key = 'qwerty1234'
                print("key:"+key)
                userObj.set_password_key(key)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()

                #Next, log in to the server
                server.login(FROMEMAIL, FROMPASS)

                #Send the mail
                msg = "\r\n".join([
                  "From:"+FROMEMAIL,
                  "To: "+user.email,
                  "Subject: Password Recovery Email for: "+user.email,
                  "",
                  "Click here "+host_url+"/_forgot?k="+key+"&e="+email
                  ])
                #msg = "\nHello!" # The /n separates the message from the headers
                server.sendmail(FROMEMAIL, user.email, msg)
                server.quit()


                print("Sending password recovery email to: "+user.email)
                flash("Please check your mail's inbox for the password recovery instructions.")
                

            except:
                print "Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
                print("Error sending password revovery email")
                flash("There was an error sending the password recovery instructions")
                pass

        else:
            flash("Could not find this email")

    elif request.method == 'GET' and request.args.get('k') and request.args.get('e'):
        data = {}
        data['key'] = request.args.get('k')
        data['email'] = request.args.get('e')
        userObj = User()
        if userObj.is_valid_password_key(data['email'],data['key']):
            print('Token authorized')
            return render_template("/auth/new_password.html", data=data)
        else:
            print('Token Rejected')
            

    elif (request.method == 'POST' and 
         request.form.get('e') and 
         request.form.get('k') and 
         request.form.get('password') and 
         request.form.get('confirm')):

        userObj = User(email=request.form.get('e'))
        user = userObj.get_user()

        if request.form.get('password') == request.form.get('confirm'):
            if userObj.is_valid_password_key(request.form.get('e'),request.form.get('k')):
                print('Token authorized')
                # generate password hash
                passhash = flask_bcrypt.generate_password_hash(request.form.get('password'))
                userObj.set_password(passhash)
                flash('Password changed')
                return redirect('_login')
            else:
                flash('Token Rejected')
                return redirect('_login')
        else:
            flash('Both passwords need to match')
            return redirect('/_forgot?k='+request.form.get('k')+'&e='+request.form.get('e'))
            
              
    data = {}

    
    return render_template("/auth/forgot.html", data=data)


@auth_flask_login.route("/_profile", methods=["GET"])
@login_required
def profile_get():

    print('profile_get():')
    rawuser = load_user(current_user.id)
    
    user = {}
    user['profilepic'] = rawuser.profilepic
    user['name'] = rawuser.name
    user['url'] = rawuser.url
    user['location'] = rawuser.location

    data = {}
    data['user'] = user
    data['handle'] = current_user.id


    
    MAM = MainModel()
    user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    if user_doc:   
        data['profilepic'] = user_doc['profilepic']
        
    


    o = urlparse.urlparse(request.url)
    data['host_url']=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

    return render_template("/auth/profile.html", data=data)




@auth_flask_login.route("/_profile", methods=["POST"])
@login_required
def profile_post():
    
    user = User(username=current_user.id)
    if user.update_user_profile(request):
        flash('Profile updated')
    else:
        flash('Profile not updated. There was a problem')

    return redirect('/'+current_user.id+'/_home')


@auth_flask_login.route("/_profile/<handle>", methods=["POST"])
@login_required
def profile_wrong(handle):
    
    return redirect('/'+handle+'/_home')

  

@auth_flask_login.route("/_orgprofile/<handle>", methods=["GET"])
@login_required
def orgprofile_get(handle):

    

    MAM = MainModel()

    needs_reload = False

    print('orgprofile_get():')
    rawuser = load_user(handle)

    '''
    print(rawuser)
    print(rawuser.added)
    profile_prerequisites = ['profilepic','name','url','location']
    for prq in profile_prerequisites:
        if rawuser[prq]:
            needs_reload = True
            # Repair elements that are missing in the profile
            elements = [prq]           
            if not MAM.repair_user_doc(elements,handle):
                flash("The organization profile can't be updated right now. Error in: "+prq)
                redirect('/'+handle+'/_home')

    if needs_reload:
        rawuser = load_user(handle)
    '''


    user = {}

    prerequisites = ['profilepic','name','url','location']
    for pr in prerequisites:
        
        '''
        try:
            user[pr] = rawuser[pr]
            user[pr] = getattr(rawuser, pr, default_value)
        except(AttributeError):
            if MAM.repair_user_doc(pr,handle):
                print('Repaired '+pr)
                user[pr] = ''
            else:
                print('Could not repair '+pr)
        '''

        if hasattr(rawuser,pr):
            print('Value is there for:'+pr)
            user[pr] = getattr(rawuser, pr,'')
        else:
            if MAM.repair_user_doc(pr,handle):
                print('Repaired '+pr)
                user[pr] = ''
            else:
                print('Could not repair '+pr)


    '''
    user['profilepic'] = rawuser.profilepic
    user['name'] = rawuser.name
    user['url'] = rawuser.url
    user['location'] = rawuser.location
    '''

    data = {}
    data['user'] = user
    data['handle'] = handle


    return render_template("/auth/orgprofile.html", data=data)


@auth_flask_login.route("/_orgprofile/<handle>", methods=["POST"])
@login_required
def orgprofile_post(handle):


    user = User(username=handle)
    if user.update_user_profile(request):
        flash('Organization information updated')
    else:
        flash('Organization information not updated. There was a problem')

    return redirect('/'+handle+'/_home')



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
    # This is called every single time when you are logged in.

    print('xload_user id is:',id)
    

    if id is None:
        redirect('/_login')
    user = User(username=id)
    user.get_user()
    if user.is_active():
        return user
    else:
        return None
    


