import sys, os, time, datetime, smtplib, urlparse, random, json
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from env_config import FROMEMAIL, FROMPASS, IMAGE_CDN_ROOT
from MainModel import MainModel
from EmailModel import EmailModel

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

                    mpp = {'status':'OK'}
                    flash({'f':'track','v':'_login','p':mpp},'MP')
                    #flash({'track':'_login OK'},'MP')

                    
                    flash({'f':'identify','v':current_user.id},'MP')
                    #flash({'identify':current_user.id},'MP')

                    mpp = {'$name':current_user.id}
                    flash({'f':'people.set','p':mpp},'MP')
                    #msg = {"$name":current_user.id}
                    #flash({'people.set': msg },'MP') 

                    flash("Logged in!",'UI')

                    if 'redirect' in request.form:
                        return redirect('/'+request.form.get('redirect')+'/_home')

                    return redirect('/'+user.id+'/_home')
                else:
                    flash("unable to log you in",'UI')

                    mpp = {'status':'KO','msg':'Unable to log in'}
                    flash({'f':'track','v':'_login','p':mpp},'MP')
                    #flash({'track':'_login KO, Try again'},'MP')
            else:
                flash("User/Password is not correct",'UI')

                mpp = {'status':'KO','msg':'User/Password incorrect'}
                flash({'f':'track','v':'_login','p':mpp},'MP')
                #flash({'track':'_login KO, User/Password incorrect'},'MP')
        else:
            flash("User not active",'UI')

            mpp = {'status':'KO','msg':'User not active'}
            flash({'f':'track','v':'_login','p':mpp},'MP')
            #flash("_login KO, User not active",'MP')


    data = {}
    data['method'] = '_login'
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/auth/login.html", data=data)


@auth_flask_login.route("/_register", methods=["GET"])
def register_get():
    
    data = {}
    data['image_cdn_root'] = IMAGE_CDN_ROOT
    data['method'] = '_register'

    return render_template("/auth/register.html", data=data)


@auth_flask_login.route("/_register", methods=["POST"])
def register_post():

    api = 'web'
    if 'api' in request.args:
        if request.args.get('api').lower() == 'json':
            api = 'json'

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
            print('Now log in the user')

            #Go through regular login process
            userObj = User(email=email)
            userview = userObj.get_user()
            print(userObj)

            if api == 'web':

                mpp = {'status':'OK'}
                flash({'f':'track','v':'_register','p':mpp},'MP')
                flash({'f':'alias','v':username},'MP')

                if login_user(userObj, remember="no"):
                        flash("Logged in. Welcome to MyRing!",'UI')

                        mpp = {'status':'OK','msg':'Automatic'}
                        flash({'f':'track','v':'_login','p':mpp},'MP')
                        #flash({'track':'_login OK, Automatic'},'MP')
                        return redirect('/'+userview.id+'/_home')      
                else:
                    flash("Please enter your credentials ",'UI')

                    mpp = {'status':'KO','msg':'Automatic'}
                    flash({'f':'track','v':'_login','p':mpp},'MP') 
                    #flash({'track':'_login KO, Automatic'},'MP')

                    return redirect('/_login')

            elif api == 'json':     

                out = {} 
                out['Success'] = True
                out['Message'] = 'The user has been created'
                data = {}
                data['api_out'] = json.dumps(out)
                return render_template("/auth/register_rs_json.html", data=data)


        else:

            if api == 'web': 

                mpp = {'status':'KO','msg':'User could not be created'}
                flash({'f':'track','v':'_register','p':mpp},'MP')
                flash({'f':'alias','v':username},'MP')          
                return redirect('/_register')

            elif api == 'json':

                out = {} 
                out['Sucess'] = False
                out['Message'] = 'The user could not be created'
                data = {}
                data['api_out'] = json.dumps(out)

                return render_template("/auth/register_rs_json.html", data=data)

            


    #except(KeyError):
    except:

        print "Notice: Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]            
        if api == 'web': 

            flash("unable to register with that email address",'UI')
            mpp = {'status':'KO','msg':'Unable to register with that email address'}
            flash({'f':'track','v':'_register','p':mpp},'MP')
            current_app.logger.error("Error on registration ")
            return redirect('/_register')

        elif api == 'json':

            print('flag9')
            out = {} 
            out['Sucess'] = False
            out['Message'] = 'Unable to register with that email address'
            data = {}
            data['api_out'] = json.dumps(out)
            return render_template("/auth/register_rs_json.html", data=data)
    


@auth_flask_login.route("/_orgregister", methods=["GET"])
@login_required
def orgregister_get():

    #registerForm = forms.SignupForm(request.form)
    #current_app.logger.info(request.form)
        
    data = {}
    data['image_cdn_root'] = IMAGE_CDN_ROOT
    data['method'] = '_orgregister'

    MAM = MainModel()

    #This is to be used by the user bar
    cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    if cu_user_doc:

        #data['cu_actualname'] = cu_user_doc['name']
        data['cu_profilepic'] = cu_user_doc['profilepic']
        #data['cu_location'] = cu_user_doc['location']
        #data['cu_handle'] = current_user.id

        data['handle_actualname'] = cu_user_doc['name']
        data['handle_profilepic'] = cu_user_doc['profilepic']
        data['handle_location'] = cu_user_doc['location']



    return render_template("/auth/orgregister.html", data=data)


@auth_flask_login.route("/_orgregister", methods=["POST"])
@login_required
def orgregister_post():

    username = request.form.get('username')
    email = request.form.get('email')

    # Organizations use no passwords
    password_hash = ''

    # prepare User
    user = User(username,email,password_hash,current_user.id,True)
    print user

    try:
    #if True:
        user.set_user()

        mpp = {'status':'OK'}
        flash({'f':'track','v':'_orgregister','p':mpp},'MP')
        

        return redirect('/'+username+'/_home')

    except:
    #else:
        print "Notice: Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
        flash("unable to register with that email address",'UI')

        mpp = {'status':'KO','msg':'Unable to register with that email address'}
        flash({'f':'track','v':'_orgregister','p':mpp},'MP')
        
        
        current_app.logger.error("Error on registration ")

    
        data = {}
        data['image_cdn_root'] = IMAGE_CDN_ROOT
        data['method'] = '_orgregister'

        MAM = MainModel()

        #This is to be used by the user bar
        cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
        if cu_user_doc:

            #data['cu_actualname'] = cu_user_doc['name']
            data['cu_profilepic'] = cu_user_doc['profilepic']
            #data['cu_location'] = cu_user_doc['location']
            #data['cu_handle'] = current_user.id

            data['handle_actualname'] = cu_user_doc['name']
            data['handle_profilepic'] = cu_user_doc['profilepic']
            data['handle_location'] = cu_user_doc['location']



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


                to = user.email
                subject = "Password Recovery Email for: "+user.email
                content = "Click here "+host_url+"/_forgot?k="+key+"&e="+email


                EMO = EmailModel()
                if EMO.send_one_email(to,subject,content):
                    print("Sending password recovery email to: "+user.email)
                    flash("Please check your mail's inbox for the password recovery instructions.",'UI')


                    mpp = {'status':'OK','msg':'Sent recovery email'}
                    flash({'f':'track','v':'_forgot','p':mpp},'MP')
                    #flash({'track':'_forgot OK, sent recovery email'},'MP')
                else:
                    print("Something went wrong with sending the email but no error was raised")

                '''

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

                '''



                
                

            except:
                print "Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
                print("Error sending password revovery email")
                flash("There was an error sending the password recovery instructions")
                flash({'track':'_forgot KO, error sending recovery email'},'MP')
                pass

        else:
            flash("Could not find this email",'UI')

            mpp = {'status':'KO','msg':'Could not find email'}
            flash({'f':'track','v':'_forgot','p':mpp},'MP')
            #flash({'track':'_forgot KO, could not find email'},'MP')

    elif request.method == 'GET' and request.args.get('k') and request.args.get('e'):
        data = {}
        data['key'] = request.args.get('k')
        data['email'] = request.args.get('e')
        userObj = User()
        if userObj.is_valid_password_key(data['email'],data['key']):
            print('Token authorized')
            mpp = {'status':'OK','msg':'Token authorized'}
            flash({'f':'track','v':'_forgot','p':mpp},'MP')
            #flash({'track':'_forgot OK, Token authorized'},'MP')
            return render_template("/auth/new_password.html", data=data)
        else:
            print('Token Rejected')
            mpp = {'status':'KO','msg':'Token not authorized'}
            flash({'f':'track','v':'_forgot','p':mpp},'MP')
            #flash({'track':'_forgot KO, Token not authorized'},'MP')
            

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
                flash('Password changed','UI')
                mpp = {'status':'OK','msg':'Password changed'}
                flash({'f':'track','v':'_forgot','p':mpp},'MP')
                #flash({'track':'_forgot OK, Password changed'},'MP')
                return redirect('_login')
            else:
                flash('Token Rejected','UI')
                mpp = {'status':'KO','msg':'Token rejected'}
                flash({'f':'track','v':'_forgot','p':mpp},'MP')
                #flash({'track':'_forgot KO, Token rejected'},'MP')
                return redirect('_login')
        else:
            flash('Both passwords need to match','UI')
            mpp = {'status':'KO','msg':'Password do not match'}
            flash({'f':'track','v':'_forgot','p':mpp},'MP')
            #flash({'track':'_forgot KO, passwords do not match'},'MP')

            return redirect('/_forgot?k='+request.form.get('k')+'&e='+request.form.get('e'))
            
              
    data = {}
    data['method'] = '_forgot'

    
    return render_template("/auth/forgot.html", data=data)


@auth_flask_login.route("/<handle>/_profile", methods=["GET"])
@login_required
def profile_get(handle):

    if handle == current_user.id:
        user = load_user(handle)

        data = {}
        data['user'] = user
        data['handle'] = handle

        o = urlparse.urlparse(request.url)
        data['host_url']=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
        data['image_cdn_root'] = IMAGE_CDN_ROOT
        data['method'] = '_profile'

        
        #This is for the upperbar only
        MAM = MainModel()
        user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
        if user_doc:   
            data['cu_profilepic'] = user_doc['profilepic']
            flash({'track':'_profile'},'MP')

        return render_template("/auth/profile.html", data=data)

    else:
        flash('Redirected to your own profile','UI')
        mpp = {'status':'KO','msg':'Redirecting users profile'}
        flash({'f':'track','v':'_profile','p':mpp},'MP')
        #flash({'track':'_profile KO, redirecting to your own profile'},'MP')
        return redirect('/'+current_user.id+'/_profile')



@auth_flask_login.route("/<handle>/_profile", methods=["POST"])
@login_required
def profile_post(handle):
    
    user = User(username=current_user.id)
    if user.update_user_profile(request):
        flash('Profile updated','UI')
        mpp = {'status':'OK','msg':'Profile updated'}
        flash({'f':'track','v':'_profile','p':mpp},'MP')
        #flash({'track':'_profile OK, Profile updated'},'MP')

    else:
        flash('Profile not updated. There was a problem','UI')
        mpp = {'status':'KO','msg':'Profile not updated'}
        flash({'f':'track','v':'_profile','p':mpp},'MP')
        #flash({'track':'_profile KO, Profile not updated'},'MP')

    return redirect('/'+current_user.id+'/_home')


@auth_flask_login.route("/<handle>/_orgprofile", methods=["GET"])
@login_required
def orgprofile_get(handle):

    MAM = MainModel()
    if MAM.user_belongs_org_team(current_user.id,handle,'owner'):

        user = load_user(handle)
        data = {}
        data['user'] = user
        data['handle'] = handle
        data['method'] = '_orgprofile'
        data['image_cdn_root'] = IMAGE_CDN_ROOT
        flash({'track':'_orgprofile'},'MP')

    else:
        mpp = {'status':'KO','msg':'Not owner'}
        flash({'f':'track','v':'_orgprofile','p':mpp},'MP')
        #flash({'track':'_orgprofile KO, User does not belong to owner team'},'MP')
        return redirect('/'+current_user.id+'/_profile')

    #This is for the current user thumbnail in the upperbar only
    MAM = MainModel()
    user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    if user_doc:   
        data['cu_profilepic'] = user_doc['profilepic']


    return render_template("/auth/orgprofile.html", data=data)



@auth_flask_login.route("/<handle>/_orgprofile", methods=["POST"])
@login_required
def orgprofile_post(handle):

    
    user = User(username=handle)
    if user.update_user_profile(request):
        flash('Organization information updated','UI')

        mpp = {'status':'OK','msg':'Updated'}
        flash({'f':'track','v':'_orgprofile','p':mpp},'MP')
        #flash({'track':'_orgprofile OK, Updated'},'MP')
    else:
        flash('Organization information not updated. There was a problem','UI')

        mpp = {'status':'OK','msg':'Not Updated'}
        flash({'f':'track','v':'_orgprofile','p':mpp},'MP')
        #flash({'track':'_orgprofile KO, Not Updated'},'MP')

    return redirect('/'+handle+'/_home')



@auth_flask_login.route("/_reauth", methods=["GET", "POST"])
@login_required
def reauth():

    return render_template("/auth/reauth.html")


@auth_flask_login.route("/_logout")
def logout():
    logout_user()
    flash("Logged out.",'UI') 

    mpp = {'status':'OK'}
    flash({'f':'track','v':'_logout','p':mpp},'MP')
    #flash({'track':'_logout OK'},'MP')

    flash({'f':'cookie.clear'},'MP')
    #flash({'cookie.clear':None},'MP')
    
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
    


