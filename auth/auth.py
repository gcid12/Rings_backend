import sys, os, time, smtplib, urlparse, random, json
from datetime import datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, g
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required,login_url)
from env_config import FROMEMAIL, FROMPASS, IMAGE_CDN_ROOT
from MainModel import MainModel
from EmailModel import EmailModel
from AvispaLogging import AvispaLoggerAdapter

from User import User

auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates',url_prefix='')

@auth_flask_login.route("/_login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated():    
        return redirect('/'+current_user.id+'/_home')
    
   
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

                    #next = request.args.get('next')
                    #if not next_is_valid(next):
                    #    return flask.abort(400)

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

                    if 'r' in request.form:
                        return redirect('/'+request.form.get('r'))

                    if user.onlogin != '':
                        return redirect(user.onlogin)

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



# API
@auth_flask_login.route("/_api/_register", methods=["POST"])
def api_register_post():

    if request.args.get('token') != 'qwerty1234':

        out = {} 
        out['Success'] = False
        out['Message'] = 'Wrong Token'
        data = {}
        data['api_out'] = json.dumps(out)
        return render_template("/base_json.html", data=data)


    username = request.form.get('username')
    email = request.form.get('email')
    token = request.form.get('token')

    # generate password hash
    password_hash = flask_bcrypt.generate_password_hash(request.form.get('password'))

    # prepare User
    user = User(username,email,password_hash)
    current_app.logger.debug(user)

    try:
    #if True:
        if user.set_user():
            current_app.logger.debug('Now log in the user')

            #Go through regular login process
            userObj = User(email=email)
            userview = userObj.get_user()
            current_app.logger.debug(userObj)
    

            out = {} 
            out['Success'] = True
            out['Message'] = 'The user has been created'
            data = {}
            data['api_out'] = json.dumps(out)
            return render_template("/base_json.html", data=data)

        else:

            out = {} 
            out['Success'] = False
            out['Message'] = 'Unable to register user with that email address'
            data = {}
            data['api_out'] = json.dumps(out)

            return render_template("/base_json.html", data=data)

    #except(KeyError):
    except:

        current_app.logger.debug("Notice: Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1])           
        out = {} 
        out['Success'] = False
        out['Message'] = 'The user could not be created'
        data = {}
        data['api_out'] = json.dumps(out)
        return render_template("/base_json.html", data=data)

#WEB
@auth_flask_login.route("/_teaminvite", methods=["GET"])
def register_teaminvite():

    MAM = MainModel()   
    logout_user()

    if current_user.is_authenticated():  
        return redirect('/_teaminvite2?h='+request.args.get('h')+
                            '&t='+request.args.get('t')+
                            '&k='+request.args.get('k')+
                            '&e='+request.args.get('e'))

    else:       
        result = MAM.select_user_doc_view('auth/userbyemail',request.args.get('e'))
        if result:
            flash(request.args.get('e')+" already exists. Please log in.",'UI') 
            return redirect(login_url('/_login','/_teaminvite2?h='+request.args.get('h')+
                            '&t='+request.args.get('t')+
                            '&k='+request.args.get('k')+
                            '&e='+request.args.get('e')))
        else:
            return redirect('/_register?h='+request.args.get('h')+
                            '&t='+request.args.get('t')+
                            '&k='+request.args.get('k')+
                            '&e='+request.args.get('e'))

#WEB
@auth_flask_login.route("/_register", methods=["GET"])
def register_get():

    data = {}
    data['image_cdn_root'] = IMAGE_CDN_ROOT
    data['method'] = '_register'

    return render_template("/auth/register.html", data=data)

#WEB
@auth_flask_login.route("/_register", methods=["POST"])
def register_post():

    MAM = MainModel()

    invite_organization = request.form.get('h') 
    invite_team = request.form.get('t') 
    invite_token = request.form.get('k')
    #invite_email = request.form.get('e')  
    
    #if e and email are not the same that is ok.

    username = request.form.get('username')
    email = request.form.get('email')

    # generate password hash
    password_hash = flask_bcrypt.generate_password_hash(request.form.get('password'))

    # prepare User
    user = User(username,email,password_hash)
    current_app.logger.debug(user)

    try:
        if user.set_user():
            user_created = True
        else:
            user_created = False

        

    except:
        current_app.logger.debug("Notice: Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1])          

        flash("unable to register with that email address",'UI')
        mpp = {'status':'KO','msg':'Unable to register with that email address'}
        flash({'f':'track','v':'_register','p':mpp},'MP')
        current_app.logger.error("Error on registration ")
        return redirect('/_register') 

    if True:
    #try:
    
        if user_created:

            

            if invite_organization and invite_team and invite_token and email:

                

                # Aquire org.invitations document
                result = MAM.select_user_doc_view('orgs/invitations',invite_organization)
                
                # Verify if this is a valid invitation
                for i in result['invitations']:
                    
                    if i['token'] == invite_token and i['email'] == email :
                        
                        valid_invite = True
                        break
                    else:
                        valid_invite = False
                
                
                if valid_invite:
                    
                    people = {}
                    people['added'] = str(datetime.now())
                    people['handle'] = username
                    people['addedby'] = i['author']
                    # Add the user to the organization people
                    MAM.append_to_user_field(invite_organization,'people',people)
                   
                    # Add the user to the team
                    MAM.append_to_user_field(invite_organization,'teams',people,
                                             sublist = 'members',
                                             wherefield = 'teamname',
                                             wherefieldvalue = invite_team
                                             )

                    
 
                # Set its onLogin hook to <invite_organization>/<invite_team>
                u = {}
                u['id'] = username
                u['onlogin'] = '/'+invite_organization+'/_home'
                MAM.update_user(u)

                



            current_app.logger.debug('User created, now log in the user')
            #Go through regular login process
            userObj = User(email=email)
            userview = userObj.get_user()
            current_app.logger.debug(userObj)

            mpp = {'status':'OK'}
            flash({'f':'track','v':'_register','p':mpp},'MP')
            flash({'f':'alias','v':username},'MP')

            if login_user(userObj, remember="no"):
                    flash("Logged in. Welcome to MyRing!",'UI')

                    mpp = {'status':'OK','msg':'Automatic'}
                    flash({'f':'track','v':'_login','p':mpp},'MP')
                    #flash({'track':'_login OK, Automatic'},'MP')
                    if invite_organization:
                        return redirect('/'+invite_organization+'/_home')
                    else:
                        return redirect('/'+userview.id+'/_home')      
            else:
                flash("Please enter your credentials ",'UI')

                mpp = {'status':'KO','msg':'Automatic'}
                flash({'f':'track','v':'_login','p':mpp},'MP') 
                #flash({'track':'_login KO, Automatic'},'MP')

                return redirect('/_login')



        else:

            mpp = {'status':'KO','msg':'User could not be created'}
            flash({'f':'track','v':'_register','p':mpp},'MP')
            flash({'f':'alias','v':username},'MP')          
            return redirect('/_register')


    else:
    #except:

        flash("Please enter your credentials. [E12] ",'UI')
        mpp = {'status':'KO','msg':'Automatic'}
        flash({'f':'track','v':'_login','p':mpp},'MP') 

        return redirect('/_login')

        


#WEB
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

#API
@auth_flask_login.route("/_api/_orgregister", methods=["POST"])
def api_orgregister_post():

    if request.args.get('token') != 'qwerty1234':
        out = {} 
        out['Success'] = False
        out['Message'] = 'Wrong Token'
        data = {}
        data['api_out'] = json.dumps(out)
        return render_template("/base_json.html", data=data)


    owner = request.form.get('owner')
    username = request.form.get('username')
    email = request.form.get('email')

    # prepare User
    user = User(username,email,'',owner,isOrg=True)
    current_app.logger.debug(user)

    try:
    
        if user.set_user():

            out = {} 
            out['Success'] = True
            out['Message'] = 'The organization has been created'
            data = {}
            data['api_out'] = json.dumps(out)
            return render_template("/base_json.html", data=data)

        else:

            out = {} 
            out['Success'] = False
            out['Message'] = 'The organization could not be created'
            data = {}
            data['api_out'] = json.dumps(out)
            return render_template("/base_json.html", data=data)

    except:
    
        current_app.logger.debug("Notice: Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1])

        out = {} 
        out['Success'] = False
        out['Message'] = 'The organization could not be created'
        data = {}
        data['api_out'] = json.dumps(out)
        return render_template("/base_json.html", data=data)
        
#WEB
@auth_flask_login.route("/_orgregister", methods=["POST"])
@login_required
def orgregister_post():

    MAM = MainModel()
    g.ip = request.remote_addr
    g.tid = MAM.random_hash_generator(36)

    logger = logging.getLogger('Avispa')
    self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})

    username = request.form.get('username')
    email = request.form.get('email')

    # Organizations use no passwords
    password_hash = ''

    # prepare User
    user = User(username,email,password_hash,current_user.id,True)
    current_app.logger.debug(user)

    try:
    #if True:
        user.set_user()

        mpp = {'status':'OK'}
        flash({'f':'track','v':'_orgregister','p':mpp},'MP')
        

        return redirect('/'+username+'/_home')

    except:
    #else:

        self.lggr.error("Notice: Unexpected error:"+str(sys.exc_info()[0])+' '+str(sys.exc_info()[1]))
        flash("unable to register the organization",'UI')

        mpp = {'status':'KO','msg':"Notice: Unexpected error:"+str(sys.exc_info()[0])+' '+str(sys.exc_info()[1])}
        flash({'f':'track','v':'_orgregister','p':mpp},'MP')
               
        return redirect('/_orgregister')



@auth_flask_login.route("/_forgot", methods=["GET", "POST"])
def forgot():


    if request.method == 'POST' and request.form.get('email'):

        email = request.form.get('email')
        userObj = User(email=email)
        user = userObj.get_user()
        current_app.logger.debug(user)


        if user and user.is_active():

            try:

                o = urlparse.urlparse(request.url)
                host_url=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

                #save the token in the database
                key = flask_bcrypt.generate_password_hash(request.form.get('email')+str(random.randint(0,9999)))
                #key = 'qwerty1234'
                current_app.logger.debug("key:"+key)
                userObj.set_password_key(key)


                to = user.email
                subject = "Password Recovery Email for: "+user.email
                content = "Click here "+host_url+"/_forgot?k="+key+"&e="+email


                EMO = EmailModel()
                if EMO.send_one_email(to,subject,content):
                    current_app.logger.debug("Sending password recovery email to: "+user.email)
                    flash("Please check your mail's inbox for the password recovery instructions.",'UI')


                    mpp = {'status':'OK','msg':'Sent recovery email'}
                    flash({'f':'track','v':'_forgot','p':mpp},'MP')
                    #flash({'track':'_forgot OK, sent recovery email'},'MP')
                else:
                    current_app.logger.debug("Something went wrong with sending the email but no error was raised")

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
                current_app.logger.debug("Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1])
                current_app.logger.debug("Error sending password revovery email")
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
            current_app.logger.debug('Token authorized')
            mpp = {'status':'OK','msg':'Token authorized'}
            flash({'f':'track','v':'_forgot','p':mpp},'MP')
            #flash({'track':'_forgot OK, Token authorized'},'MP')
            return render_template("/auth/new_password.html", data=data)
        else:
            current_app.logger.debug('Token Rejected')
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
                current_app.logger.debug('Token authorized')
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
        data['menu'] = 's1'

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
        data['menu'] = ''

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

    #current_app.logger.debug('xload_user id is:',str(id))
    

    if id is None:
        redirect('/_login')
    user = User(username=id)
    user.get_user()
    if user.is_active():
        return user
    else:
        return None
    



@auth_flask_login.route("/<handle>/_access", methods=["GET"])
@login_required
def access_get(handle):

    if handle == current_user.id:
        user = load_user(handle)

        data = {}
        data['user'] = user
        data['handle'] = handle
        data['menu'] = 's2'

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

        return render_template("/auth/access.html", data=data)

    else:
        flash('Redirected to your own profile','UI')
        mpp = {'status':'KO','msg':'Redirecting users profile'}
        flash({'f':'track','v':'_profile','p':mpp},'MP')
        #flash({'track':'_profile KO, redirecting to your own profile'},'MP')
        return redirect('/'+current_user.id+'/_profile')



@auth_flask_login.route("/<handle>/_email", methods=["GET"])
@login_required
def email_get(handle):

    if handle == current_user.id:
        user = load_user(handle)

        data = {}
        data['user'] = user
        data['handle'] = handle
        data['menu'] = 's3'

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

        return render_template("/auth/email.html", data=data)

    else:
        flash('Redirected to your own profile','UI')
        mpp = {'status':'KO','msg':'Redirecting users profile'}
        flash({'f':'track','v':'_profile','p':mpp},'MP')
        #flash({'track':'_profile KO, redirecting to your own profile'},'MP')
        return redirect('/'+current_user.id+'/_profile')




@auth_flask_login.route("/<handle>/_billing", methods=["GET"])
@login_required
def billing_get(handle):

    if handle == current_user.id:
        user = load_user(handle)

        data = {}
        data['user'] = user
        data['handle'] = handle
        data['menu'] = 's4'

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

        return render_template("/auth/billing.html", data=data)

    else:
        flash('Redirected to your own profile','UI')
        mpp = {'status':'KO','msg':'Redirecting users profile'}
        flash({'f':'track','v':'_profile','p':mpp},'MP')
        #flash({'track':'_profile KO, redirecting to your own profile'},'MP')
        return redirect('/'+current_user.id+'/_profile')



@auth_flask_login.route("/<handle>/_licenses", methods=["GET"])
@login_required
def licenses_get(handle):

    if handle == current_user.id:
        user = load_user(handle)

        data = {}
        data['user'] = user
        data['handle'] = handle
        data['menu'] = 's5'

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

        return render_template("/auth/licenses.html", data=data)

    else:
        flash('Redirected to your own profile','UI')
        mpp = {'status':'KO','msg':'Redirecting users profile'}
        flash({'f':'track','v':'_profile','p':mpp},'MP')
        #flash({'track':'_profile KO, redirecting to your own profile'},'MP')
        return redirect('/'+current_user.id+'/_profile')













