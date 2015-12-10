import sys, os, time, smtplib, urlparse, random, json,logging,traceback
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

def lggr_setup():

    MAM = MainModel()
    g.ip = request.remote_addr
    g.tid = MAM.random_hash_generator(36)
    logger = logging.getLogger('Avispa')
    lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})

    return lggr


@auth_flask_login.route("/_login", methods=["GET", "POST"])
def login():

    MAM = MainModel()

    lggr = lggr_setup()

    if current_user.is_authenticated(): 

        return redirect('/'+current_user.id+'/_home')
     
    if request.method == "POST" and "email" in request.form:

        lggr.info('Login attempt for:'+request.form.get('email')) 
        email = request.form.get('email')

        
        if email.strip() != '':
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

                        lggr.info('Login attempt successful for:'+request.form.get('email')) 

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
                            #lggr.info('Redirecting to :'+'/'+request.form.get('r')) 
                            #return redirect('/'+request.form.get('r'))
                            rr = '/'+request.form.get('r')

                        elif user.onlogin != '':
                            #lggr.info('Redirecting to :'+user.onlogin) 
                            #return redirect(user.onlogin)
                            rr = user.onlogin

                        else:
                            rr = '/'+user.id+'/_home'

                        lggr.info('Redirecting to :'+rr) 

                        return redirect(rr)
                    else:

                        lggr.info('Something went wrong in the user object:'+request.form.get('email')) 
                        flash("unable to log you in",'UI')

                        mpp = {'status':'KO','msg':'Unable to log in'}
                        flash({'f':'track','v':'_login','p':mpp},'MP')
                        #flash({'track':'_login KO, Try again'},'MP')
                else:
                    lggr.info('User/Password is not correct for:'+request.form.get('email')) 
                    flash("User/Password is not correct",'UI')

                    mpp = {'status':'KO','msg':'User/Password incorrect'}
                    flash({'f':'track','v':'_login','p':mpp},'MP')
                    #flash({'track':'_login KO, User/Password incorrect'},'MP')
            else:
                lggr.info('User is not active:'+request.form.get('email')) 
                flash("User not active",'UI')

                mpp = {'status':'KO','msg':'User not active'}
                flash({'f':'track','v':'_login','p':mpp},'MP')
                #flash("_login KO, User not active",'MP')
        else:
            lggr.info('Enter a valid email:') 
            flash("Enter a valid email",'UI')



    data = {}
    data['method'] = '_login'
    #t = time.time()
    #data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))
    
    return render_template("/auth/login.html", data=data)



# API
@auth_flask_login.route("/_api/_register", methods=["POST"])
def api_register_post():

    MAM = MainModel() 
    lggr = lggr_setup()
    lggr = lggr_info('_api/_register attempt')

    if request.args.get('token') != 'qwerty1234':

        out = {} 
        out['Success'] = False
        out['Message'] = 'Wrong Token'
        data = {}
        data['api_out'] = json.dumps(out)
        lggr = lggr_info('_api/_register attempt')
        return render_template("/base_json.html", data=data)


    username = request.form.get('username')
    email = request.form.get('email')
    token = request.form.get('token')

    # generate password hash
    password_hash = flask_bcrypt.generate_password_hash(request.form.get('password'))

    # prepare User
    user = User(username,email,password_hash)
    lggr.debug(user)


    try:
    #if True:
        if user.set_user():
            lggr.info('Now log in the user')

            #Go through regular login process
            userObj = User(email=email)
            userview = userObj.get_user()
            lggr.info(userObj)
    

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

        lggr.error(traceback.format_exception(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))         
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
    lggr = lggr_setup()
   
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

    MAM = MainModel()
    lggr = lggr_setup()

    data = {}
    data['image_cdn_root'] = IMAGE_CDN_ROOT
    data['method'] = '_register'

    return render_template("/auth/register.html", data=data)

#WEB
@auth_flask_login.route("/_register", methods=["POST"])
def register_post():

    MAM = MainModel()
    lggr = lggr_setup()

    invite_organization = request.form.get('h') 
    invite_team = request.form.get('t') 
    invite_token = request.form.get('k')
    #invite_email = request.form.get('e')  
    
    #if e and email are not the same that is ok.

    username = request.form.get('username').lower().replace(' ','')
    email = request.form.get('email').lower().replace(' ','')

    # generate password hash
    password_hash = flask_bcrypt.generate_password_hash(request.form.get('password'))

    # prepare User
    user = User(username,email,password_hash)
    lggr.info(user)

    try:
        if user.set_user():
            lggr.info('User created')
            user_created = True
        else:
            lggr.info('User NOT created')
            user_created = False

        

    except:
        lggr.error(traceback.format_exception(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))         

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
                        lggr.info('Invitation valid')
                        
                        valid_invite = True
                        break
                    else:
                        lggr.info('Invitation invalid')
                        valid_invite = False
                
                
                if valid_invite:
                    
                    people = {}
                    people['added'] = str(datetime.now())
                    people['handle'] = username
                    people['addedby'] = i['author']
                    # Add the user to the organization people
                    MAM.append_to_user_field(invite_organization,'people',people)
                    lggr.info('User appended to org: %s'%(invite_organization))
                   
                    # Add the user to the team
                    MAM.append_to_user_field(invite_organization,'teams',people,
                                             sublist = 'members',
                                             wherefield = 'teamname',
                                             wherefieldvalue = invite_team
                                             )

                    lggr.info('User added to team: %s'%(invite_team))



                    
 
                # Set its onLogin hook to <invite_organization>/<invite_team>
                u = {}
                u['id'] = username
                u['onlogin'] = '/'+invite_organization+'/_home'
                MAM.update_user(u)

                



            lggr.info('User created, now log in the user')
            #Go through regular login process
            userObj = User(email=email)
            userview = userObj.get_user()
            lggr.info(userObj)

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

            lggr.info('User could not be created')
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

    MAM = MainModel()
    lggr = lggr_setup()

    #registerForm = forms.SignupForm(request.form)
    #current_app.logger.info(request.form)
        
    data = {}
    data['image_cdn_root'] = IMAGE_CDN_ROOT
    data['method'] = '_orgregister'

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

    MAM = MainModel()
    lggr = lggr_setup()

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
    lggr.info(user)

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
    
        lggr.error(traceback.format_exception(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))

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
    lggr = lggr_setup()

    username = request.form.get('username')
    email = request.form.get('email')

    # Organizations use no passwords
    password_hash = ''

    # prepare User
    user = User(username,email,password_hash,current_user.id,True)
    lggr.info(user)

    try:
    #if True:
        user.set_user()

        mpp = {'status':'OK'}
        flash({'f':'track','v':'_orgregister','p':mpp},'MP')
        

        return redirect('/'+username+'/_home')

    except(TypeError):

    #else:
 
        
        lggr.error(traceback.format_exception(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
        flash("unable to register the organization",'UI')

        mpp = {'status':'KO','msg':"Notice: Unexpected error:"+str(sys.exc_info()[0])+' '+str(sys.exc_info()[1])}
        flash({'f':'track','v':'_orgregister','p':mpp},'MP')
               
        return redirect('/_orgregister')



@auth_flask_login.route("/_forgot", methods=["GET", "POST"])
def forgot():

    MAM = MainModel()
    lggr = lggr_setup()


    if request.method == 'POST' and request.form.get('email'):

        email = request.form.get('email')
        userObj = User(email=email)
        user = userObj.get_user()
        lggr.info(user)


        if user and user.is_active():

            try:

                o = urlparse.urlparse(request.url)
                host_url=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

                #save the token in the database
                key = flask_bcrypt.generate_password_hash(request.form.get('email')+str(random.randint(0,9999)))
                #key = 'qwerty1234'
                lggr.info("key:"+key)
                userObj.set_password_key(key)


                to = user.email
                subject = "Password Recovery Email for: "+user.email
                content = "Click here "+host_url+"/_forgot?k="+key+"&e="+email


                EMO = EmailModel()
                if EMO.send_one_email(to,subject,content):
                    lggr.info("Sending password recovery email to: "+user.email)
                    flash("Please check your mail's inbox for the password recovery instructions.",'UI')


                    mpp = {'status':'OK','msg':'Sent recovery email'}
                    flash({'f':'track','v':'_forgot','p':mpp},'MP')
                    #flash({'track':'_forgot OK, sent recovery email'},'MP')
                else:
                    lggr.info("Something went wrong with sending the email but no error was raised")

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
                lggr.error(traceback.format_exception(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2]))
                lggr.error("Error sending password revovery email")
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
            lggr.info('Token authorized')
            mpp = {'status':'OK','msg':'Token authorized'}
            flash({'f':'track','v':'_forgot','p':mpp},'MP')
            #flash({'track':'_forgot OK, Token authorized'},'MP')
            return render_template("/auth/new_password.html", data=data)
        else:
            lggr.info('Token Rejected')
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
                lggr.info('Token authorized')
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

    MAM = MainModel()
    lggr = lggr_setup()

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

    MAM = MainModel()
    lggr = lggr_setup()
    
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
    lggr = lggr_setup()

    
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
    user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    if user_doc:   
        data['cu_profilepic'] = user_doc['profilepic']


    return render_template("/auth/orgprofile.html", data=data)



@auth_flask_login.route("/<handle>/_orgprofile", methods=["POST"])
@login_required
def orgprofile_post(handle):

    MAM = MainModel()
    lggr = lggr_setup()
    
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

    MAM = MainModel()
    lggr = lggr_setup()

    return render_template("/auth/reauth.html")


@auth_flask_login.route("/_logout")
def logout():

    MAM = MainModel()
    lggr = lggr_setup()


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

    #lggr.info('xload_user id is:',str(id))
    

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

    MAM = MainModel()
    lggr = lggr_setup()

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

    MAM = MainModel()
    lggr = lggr_setup()

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

    MAM = MainModel()
    lggr = lggr_setup()

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

    MAM = MainModel()
    lggr = lggr_setup()

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













