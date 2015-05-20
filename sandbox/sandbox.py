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

@sandbox.route("/rq_test", methods=["GET"])
def requests_test_get():

    data = {}

    return render_template("/sandbox/rq_test_form.html", data=data) 


@sandbox.route("/rq_test", methods=["POST"])
def requests_test_post():

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
    
    
    #api_url = 'https://avispa.myring.io/_register'
    api_url = 'https://avispa.myring.io/_api/_register?token=qwerty1234'
    payload = {'username':username, 'email':email, 'password':password, 'confirm':confirm}

    #api_url = 'http://0.0.0.0:8080/_api/_orgregister?token=qwerty1234'
    #payload = {'username':orgusername, 'email':email, 'owner':username}
    #r2 = requests.get(api_url)
    r1 = requests.post(api_url,data=payload,verify=False)
    print(r1.text)
    #q2 = json.loads(r2.text)

    data = {}
    data['ok'] = True
    #data['q2'] = q2

    return render_template("/sandbox/rq_test.html", data=data) 



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

        #cafile = 'cacert.pem' # http://curl.haxx.se/ca/cacert.pem
        
        cert=('/etc/ssl/public.crt', '/etc/ssl/avispa.myring.io.key')

        #try:
        if(True):
            # _api/_register . Create the user
            print('r1')
            api_url = 'https://avispa.myring.io/_api/_register?token=qwerty1234'
            payload = {'username':username, 'email':email, 'password':password, 'confirm':confirm}
            #r1 = requests.post(api_url,data=payload,cert=cert)
            r1 = requests.post(api_url,data=payload,verify=False)
            print(r1.text)
            q1 = json.loads(r1.text)
            print(q1)

            login_result = login_user_by_email(email,username)


            if q1['Success']:
                print('r2')
                flash(q1['Message'],'UI')
                # _api/_orgregister . Create the organization
                api_url = 'https://avispa.myring.io/_api/_orgregister?token=qwerty1234'
                #api_url = 'http://0.0.0.0:8080/_api/_orgregister?token=qwerty1234'
                payload = {'username':orgusername, 'email':email, 'owner':username}
                #r2 = requests.post(api_url,data=payload,cert=cert)
                r2 = requests.post(api_url,data=payload,verify=False)
                
                print(r2.text)
                q2 = json.loads(r2.text)

                if q2['Success']:
                    print('r3')
                    flash(q2['Message'],'UI')
                    # _api/USER/_collections . Create the collection
                    api_url = 'https://avispa.myring.io/_api/'+orgusername+'/_collections?token=qwerty1234'
                    colname = 'business_facts'
                    payload = {'CollectionName':colname}
                    #r3 = requests.post(api_url,data=payload,cert=cert)
                    r3 = requests.post(api_url,data=payload,verify=False)
                    print(r3.text)
                    q3 = json.loads(r3.text)

                    if q3['Success']:
                        print('r4')
                        flash(q3['Message'],'UI')
                        # Create the ring in the collection
                        api_url = 'https://avispa.myring.io/_api/'+orgusername+'/_collections/'+colname+'?token=qwerty1234'

                        #https://avispa.myring.io/_api/facts/company
                        #https://avispa.myring.io/_api/facts/product
                        ringlist = [
                            'https://avispa.myring.io/_api/facts/company',
                            'https://avispa.myring.io/_api/facts/product'
                        ]

                        success = True
                        for r in ringlist: 
                            payload = {'ringurl':r}
                            #r4 = requests.post(api_url,data=payload,cert=cert)
                            r4 = requests.post(api_url,data=payload,verify=False)
                            print(r4.text)
                            q4 = json.loads(r4.text)
                            if 'Success' not in q4:
                                success = False


                        if success:
                            print('r5')
                            flash(q4['Message'],'UI')
                        else: 
                            # The rings could not be added
                            flash(q4['Message'],'ER')

                            #THIS SHOULD LOGIN THE USER, GO TO THE ORG ANYWAY. THE NEXT STEP WILL CHECK AND REPAIR IF NEEDED
                            return redirect('/_widget/mbf_signup')
                    else:
                        # The collection could not be created
                        flash(q3['Message'],'ER')

                        #THIS SHOULD LOGIN THE USER, GO TO THE ORG ANYWAY. THE NEXT STEP WILL CHECK AND REPAIR IF NEEDED
                        return redirect('/_widget/mbf_signup')
                else:
                    # The org could not be created
                    flash(q2['Message'],'ER')

                    #THIS SHOULD LOGIN THE USER AND SHOW PARTIAL mbf_signup => ORGUSERNAME PART ONLY
                    return redirect('/_widget/mbf_signup?orgusername='+orgusername)
            else:
                # The user could not be created
                flash(q1['Message'],'ER')

                return redirect('/_widget/mbf_signup?username='+username+'&email='+email+'&orgusername='+orgusername)

        #except:
        else:
            print "Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
            print('There was an API exception. 500')
            flash('There was an API exception. 500','ER')
            data = {}
            return render_template("/widget/mbf_signup.html", data=data) 
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





# REPORTS   

@sandbox.route("/facts/travelservice", methods=["GET", "POST"])
#@login_required
def travelservice():

    data = {}
    data['mask']= "mbf"

    # HOTEL INFO
    
    data['Name']= "Park Central NY" 
    data['Address']= "870 Seventh Avenue at 56th Street"
    data['City']= "NewYork"
    data['State']= "NY"
    data['Zip']= "10018"
    data['Industry']= "10018"


    data['OneLine'] = [{
                #This USES THE FACTCARD MACRO
                #Title of the card
                'fc_SubTitle':'One Line Description',
                'fc_Descriptions': {
                    'en': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 
                    'sp': 'espanol del product 1', 
                    'fr': 'frances del product 1'
                    }
                }]# CLOSE

    data['Description'] = [{
            #This USES THE FACTCARD MACRO
            #Title of the card
            'fc_SubTitle':'One Line Description',
            'fc_Descriptions': {
                'en': 'ingles del product 1', 
                'sp': 'espanol del product 1', 
                'fr': 'frances del product 1'
                }
            }]# CLOSE

    #CONTACT
    data['Website']= "x14"
    data['Mail']= "x12"
    data['Phone']= "x13"
    data['Fax']= "x15"
    data['Newsletter']= "x18"

    #DETAILS
    data['Founded']= "x18"
    data['Closed']= "x18"
    data['ResAge']= "x09"
    data['Founded']= "x10"
    data['payments']="x12"


    #SOCIALMEDIA
        # twitter
    data['SM1']= "x19"
        # facebook
    data['SM2']= "x20"
        # youtube
    data['SM3']= "x21"
        # instagram
    data['SM4']= "x22"
        #Other Links
    data['LINK1']= "x23"
    data['LINK2']= "x23"
    data['LINK3']= "x23"
    data['LINK4']= "x23"


    #HISTORY
    data['Facts']= "x14"
    data['Awards']= "x14"
    data['FAQ']= "x14"
    data['FactualID']= "x14"
    data['history'] = [{
                    #This USES THE FACTCARD MACRO
                    #Title of the card
                    'fc_SubTitle':'History',
                    # Fields used:  History, History2, History3
                    'fc_Descriptions': {
                        'en': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra tortor sit amet justo volutpat, et varius libero lobortis. Nullam mattis turpis quis nunc efficitur suscipit. Sed eu vestibulum nisl, quis finibus leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus. Nam nibh quam, convallis a neque at, commodo cursus tortor. Morbi mollis purus sem, vel dapibus augue ornare malesuada. Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    # HISTORY PHOTOS
                    'fc_Owner':'teamamerica',
                    # PHOTOS
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    

                    }]# CLOSE
    data['OurStaff'] = [{
                    'fc_Title':'Our Staff',
                    'fc_Descriptions': {
                        'en': 'ingles del product 1', 
                        'sp': 'espanol del product 1', 
                        'fr': 'frances del product 1'
                        }
                    }]# CLOSE

    data['curious'] = [{
                    'fc_SubTitle':'Curious Facts',
                    'fc_Specs': {
                            'd1': ['fact 1','Carpintero'], 
                            'd2': ['fact 2','Soldado'],  
                            'd3': ['fact 3','Musico'], 
                        },
                    }]# CLOSE

    data['contact'] = [{
                    'fc_SubTitle':'Contact',
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        }

                    }]# CLOSE

    data['Services'] = [{
                    'fc_Title':'Bateaux New York',
                    'fc_SubTitle':'The best way to see the city , unique Brunch',
                    'fc_Category':'Cruise Waterfront',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Casual'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra tortor sit amet justo volutpat, et varius libero lobortis. Nullam mattis turpis quis nunc efficitur suscipit. Sed eu vestibulum nisl, quis finibus leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus. Nam nibh quam, convallis a neque at, commodo cursus tortor. Morbi mollis purus sem, vel dapibus augue ornare malesuada. Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439'],
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.'], 
                            'd2': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas']
                        },

                    },
                    # SECOND ITEM
                    {
                    'fc_Title':'La Pecorina',
                    'fc_SubTitle':'The best Brger in Town and unique familiar mood',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Casual'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra tortor sit amet justo volutpat, et varius libero lobortis. Nullam mattis turpis quis nunc efficitur suscipit. Sed eu vestibulum nisl, quis finibus leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus. Nam nibh quam, convallis a neque at, commodo cursus tortor. Morbi mollis purus sem, vel dapibus augue ornare malesuada. Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas'], 
                            'd2': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.']
                        },

                    }] # CLOSE

    data['photos'] = [{
                    
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439'],

                    }]# CLOSE
                    
    data['staff'] = [{
                    'fc_SubTitle':'Our Staff',
                    'fc_Descriptions': {
                        'en': 'ingles del product 1', 
                        'sp': 'espanol del product 1', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],

                    }]# CLOSE

    # HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////
    # HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////

    # DETAILS ONLY HOTEL
    data['Checkin']= "x06" 
    data['Checkout']= "x07"
    data['NumberRooms']= "x08"
    data['Parking']= "x08"
    data['Accesibility']="x12"
    data['Rank']= "x06"
    data['LastRenovation']= "x06"

    data['Rooms'] = [{
                    'fc_Title':'Single Room Presidential',
                    'fc_Category':'Room',
                    'fc_Specs': {
                            'd1': ['Category','SGL Room'], 
                            'd2': ['Avg Size','300 sq ft.'],  
                            'd3': ['Smoking','No'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra tortor sit amet justo volutpat, et varius libero lobortis. Nullam mattis turpis quis nunc efficitur suscipit. Sed eu vestibulum nisl, quis finibus leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus. Nam nibh quam, convallis a neque at, commodo cursus tortor. Morbi mollis purus sem, vel dapibus augue ornare malesuada. Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439'],
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],
                        'fc_SmallNotes': {
                            'd1': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.'], 
                            'd2': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas']
                        },
                        'fc_Tags':[{'name': 'Room Ammenities', 
                                'list': ['a_001','a_002','a_003']
                                }
                            ],
                    },

                    ]# CLOSE

    # HOTEL AMMENITIES
    data['Includes'] = [{   
                    'fc_SubTitle':'Ammenities',

                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                },
                                {'name': 'Concierge', 
                                'list': ['c_001','c_002','c_003','c_004','c_005','c_006']
                                },
                                {'name': 'Food', 
                                'list': ['d_001','d_002','d_003','d_004','d_005','d_006','d_007','d_008']
                                },
                                {'name': 'Events', 
                                'list': ['e_001','e_002','e_003']
                                },
                                {'name': 'Fitness', 
                                'list': ['f_001','f_002','f_003','f_004','f_005']
                                },
                                {'name': 'Kids', 
                                'list': ['g_001','g_002','g_003','g_004']
                                },
                                {'name': 'Leisure', 
                                'list': ['h_001','h_002','h_003','h_004']
                                },
                                {'name': 'Medical', 
                                'list': ['i_001','i_002','i_003','i_004','i_005']
                                },
                                {'name': 'pets', 
                                'list': ['j_001','j_002','j_003','j_004']
                                },
                                {'name': 'Pool', 
                                'list': ['k_001','k_002','k_003','k_004','k_005']
                                },
                                {'name': 'Shopping', 
                                'list': ['l_001','l_002','l_003','l_004','l_005']
                                },
                                {'name': 'Smoking', 
                                'list': ['m_001','m_002','m_003']
                                },
                                {'name': 'Transportation', 
                                'list': ['n_001','n_002','n_003','n_004','n_005']
                                },
                            ],
                            }]


    return render_template("/sandbox/factcard.html", data=data)   

@sandbox.route("/facts/parkcentral", methods=["GET", "POST"])
#@login_required
def facts_001():

    data = {}
    data['mask']= "mbf"

    # HOTEL INFO
    
    data['Name']= "Park Central NY" 
    data['Address']= "870 Seventh Avenue at 56th Street"
    data['City']= "NewYork"
    data['State']= "NY"
    data['Zip']= "10018"
    data['Industry']= "10018"


    data['OneLine'] = [{
                #This USES THE FACTCARD MACRO
                #Title of the card
                'fc_SubTitle':'Full Description',
                'fc_DescriptionsSize':'1',
                'fc_Descriptions': {
                      'd1': ['en',1 ,'Midtown convenience. Classic hospitality. Complete comfort. A celebrated past. It all comes together at the Park Central New York Hotel. located squarely amidst New York`s most popular sights and hotels in Midtown Manhattan. Our mix of exciting amenities pay homage to our glamorous past, while presenting a modern spin on the hotel`s electrifying environment. Guests will delight in escaping the hectic city life to bask in the stylish Park Central New York.'], 
                      'd2': ['sp',1,'Conveniencia Midtown . Hospitalidad Classic. Total comodidad . Un pasado celebre . Todo confluye en el Hotel Parque Central de Nueva York. situado de lleno en medio de nuevas Yorks atracciones turisticas mas populares y hoteles en el centro de Manhattan . Nuestra mezcla de comodidades sorprendentes rendir homenaje a nuestro pasado glamoroso , al tiempo que presenta un giro moderno en el medio ambiente electrizante del hotel. Los huespedes se deleitaran con escapar del bullicio de la ciudad para tomar el sol en el elegante Parque Central de Nueva York.'],  
                      'd3': ['fr',4,'(not defined)'], 
                  }
                }]# CLOSE

    data['Description'] = [{
            #This USES THE FACTCARD MACRO
            #Title of the card
            'fc_SubTitle':'One Line Description',
            'fc_DescriptionsSize':'2',
            'fc_Descriptions': {
                    'd1': ['en',1 ,'The midtown new york city hotel Central to new york`s best'], 
                    'd2': ['sp',1,'El hotel mejor situado en Midtown Manhattan, cerca de lo mejor de NewYork'],  
                    'd3': ['fr',4,'(not defined)'], 
                }

            }]# CLOSE

    #CONTACT
    data['Website']= "x14"
    data['Mail']= "x12"
    data['Phone']= "x13"
    data['Fax']= "x15"
    data['Newsletter']= "x18"

    #DETAILS
    data['Founded']= "x18"
    data['Closed']= "x18"
    data['ResAge']= "x09"
    data['Founded']= "x10"
    data['payments']="x12"


    #SOCIALMEDIA
        # twitter
    data['SM1']= "x19"
        # facebook
    data['SM2']= "x20"
        # youtube
    data['SM3']= "x21"
        # instagram
    data['SM4']= "x22"
        #Other Links
    data['LINK1']= "x23"
    data['LINK2']= "x23"
    data['LINK3']= "x23"
    data['LINK4']= "x23"


    #HISTORY
    data['Facts']= "x14"
    data['Awards']= "x14"
    data['FAQ']= "x14"
    data['FactualID']= "x14"
    data['history'] = [{
                    #This USES THE FACTCARD MACRO
                    #Title of the card
                    'fc_SubTitle':'History',
                    # Fields used:  History, History2, History3
                    'fc_Descriptions': {
                      'd1': ['en',1 ,'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra tortor sit amet justo volutpat, et varius libero lobortis. Nullam mattis turpis quis nunc efficitur suscipit. Sed eu vestibulum nisl, quis finibus leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus. Nam nibh quam, convallis a neque at, commodo cursus tortor. Morbi mollis purus sem, vel dapibus augue ornare malesuada. Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas'], 
                      'd2': ['sp',4,'(not defined)'],  
                      'd3': ['fr',4,'(not defined)'], 
                    },
                    # HISTORY PHOTOS
                    'fc_Owner':'teamamerica',
                    # PHOTOS
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    

                    }]# CLOSE
    data['OurStaff'] = [{
                    'fc_Title':'Our Staff',
                    'fc_Descriptions': {
                      'd1': ['en',4 ,'(not defined)'], 
                      'd2': ['sp',4,'(not defined)'],  
                      'd3': ['fr',4,'(not defined)'], 
                      }
                    }]# CLOSE

    data['curious'] = [{
                    'fc_SubTitle':'Curious Facts',
                    'fc_Specs': {
                            'd1': ['fact 1','Carpintero'], 
                            'd2': ['fact 2','Soldado'],  
                            'd3': ['fact 3','Musico'], 
                        },
                    }]# CLOSE

    data['contact'] = [{
                    'fc_SubTitle':'Contact',
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        }

                    }]# CLOSE

    data['photos'] = [{
                    
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        }

                    }]# CLOSE
                    
    data['staff'] = [{
                    'fc_SubTitle':'Our Staff',
                    'fc_Descriptions': {
                      'd1': ['en',4 ,'(not defined)'], 
                      'd2': ['sp',4,'(not defined)'],  
                      'd3': ['fr',4,'(not defined)'], 
                      },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        }


                    }]# CLOSE

    # HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////
    # HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////HOTEL////

    # DETAILS ONLY HOTEL
    data['Checkin']= "x06" 
    data['Checkout']= "x07"
    data['NumberRooms']= "x08"
    data['Parking']= "x08"
    data['Accesibility']="x12"
    data['Rank']= "x06"
    data['LastRenovation']= "x06"

    data['Rooms'] = [{
                    'fc_Title':'Single Room Presidential',
                    'fc_Category':'Room',
                    'fc_Specs': {
                            'd1': ['Category','SGL Room'], 
                            'd2': ['Avg Size','300 sq ft.'],  
                            'd3': ['Smoking','No'], 
                        },
                    'fc_Descriptions': {
                      'd1': ['en',4 ,'(not defined)'], 
                      'd2': ['sp',4,'(not defined)'],  
                      'd3': ['fr',4,'(not defined)'], 
                      },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],
                        'fc_SmallNotes': {
                            'd1': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.'], 
                            'd2': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas']
                        },
                        'fc_Tags':[{'name': 'Room Ammenities', 
                                'list': ['a_001','a_002','a_003']
                                }
                            ],
                    },

                    ]# CLOSE

    # HOTEL AMMENITIES
    data['Includes'] = [{   
                    'fc_SubTitle':'Ammenities',

                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                },
                                {'name': 'Concierge', 
                                'list': ['c_001','c_002','c_003','c_004','c_005','c_006']
                                },
                                {'name': 'Food', 
                                'list': ['d_001','d_002','d_003','d_004','d_005','d_006','d_007','d_008']
                                },
                                {'name': 'Events', 
                                'list': ['e_001','e_002','e_003']
                                },
                                {'name': 'Fitness', 
                                'list': ['f_001','f_002','f_003','f_004','f_005']
                                },
                                {'name': 'Kids', 
                                'list': ['g_001','g_002','g_003','g_004']
                                },
                                {'name': 'Leisure', 
                                'list': ['h_001','h_002','h_003','h_004']
                                },
                                {'name': 'Medical', 
                                'list': ['i_001','i_002','i_003','i_004','i_005']
                                },
                                {'name': 'pets', 
                                'list': ['j_001','j_002','j_003','j_004']
                                },
                                {'name': 'Pool', 
                                'list': ['k_001','k_002','k_003','k_004','k_005']
                                },
                                {'name': 'Shopping', 
                                'list': ['l_001','l_002','l_003','l_004','l_005']
                                },
                                {'name': 'Smoking', 
                                'list': ['m_001','m_002','m_003']
                                },
                                {'name': 'Transportation', 
                                'list': ['n_001','n_002','n_003','n_004','n_005']
                                },
                            ],
                            }]


    return render_template("/sandbox/factcard.html", data=data)  



@sandbox.route("/facts/ecruises", methods=["GET", "POST"])
#@login_required
def facts_002():

    data = {}
    data['mask']= "mbf"

    # HOTEL INFO
    
    data['Name']= "Entertainment Cruises NY" 
    data['Address']= "Pier 62, Chelsea Piers Suite 200"
    data['City']= "NewYork"
    data['State']= "NY"
    data['Zip']= "10011"
    data['Industry']= ""
    data['Description'] = [{
            #This USES THE FACTCARD MACRO
            #Title of the card
            'fc_SubTitle':'Full Description',
            'fc_DescriptionsSize':'1',
            'fc_Descriptions': {
                'en': 'Get up close to the Statue of Liberty and travel under the iconic Brooklyn Bridge. Come out for a cruise on beautiful New York Harbor from your choice of our dock at Chelsea Piers or Lincoln Harbor Marina in Weehawken, New Jersey.', 
                'sp': 'espanol del product 1', 
                'fr': 'frances del product 1'
                }
            }]# CLOSE

    data['OneLine'] = [{
                #This USES THE FACTCARD MACRO
                #Title of the card
                'fc_SubTitle':'One Line Description',
                'fc_DescriptionsSize':'2',
                'fc_Descriptions': {
                    'en': 'Entertainment Cruises, dining cruises, yacht charters and sightseeing tours.', 
                    'sp': 'espanol del product 1', 
                    'fr': 'frances del product 1'
                    }
                }]# CLOSE
    #CONTACT
    data['Website']= "http://www.bateauxnewyork.com/new-york-metro"
    data['Mail']= "x12"
    data['Phone']= "866-817-3463"
    data['Fax']= ""
    data['Newsletter']= ""
    data['Blog']= "http://www.entertainmentcruises.com/blog/"

    #DETAILS
    data['Founded']= "x18"
    data['Closed']= "x18"
    data['ResAge']= "x09"
    data['Founded']= "x10"
    data['payments']="x12"
    #SOCIALMEDIA  
        # twitter
    data['SM1']= "entertaincruise"
        # facebook
    data['SM2']= "https://www.facebook.com/BateauxNewYork"
        # instagram
    data['SM3']= "ecnewyork"
        # youtube
    data['SM4']= "ecnewyork"
        #Other Links
    data['LINK1']= "x23"
    data['LINK2']= "x23"
    data['LINK3']= "x23"
    data['LINK4']= "x23"
    #HISTORY
    data['Facts']= "x14"
    data['Awards']= "x14"
    data['FAQ']= "x14"
    data['FactualID']= "x14"
    data['history'] = [{
                    #This USES THE FACTCARD MACRO
                    #Title of the card
                    'fc_SubTitle':'History',
                    # Fields used:  History, History2, History3
                    'fc_Descriptions': {
                        'en': 'Entertainment Cruises roots date back to 1978 when the Spirit of Norfolk was christened and began cruising the historic Elizabeth River. Today, we have 30 boats across nine locations and host more than 1.5 million guests each year. Our shipmates feel privileged to share in our guests special celebrations - and help make their experiences with us memorable. ', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    # HISTORY PHOTOS
                    'fc_Owner':'teamamerica',
                    # PHOTOS
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        }
                    

                    }]# CLOSE
    data['OurStaff'] = [{
                    'fc_Title':'Our Staff',
                    'fc_Descriptions': {
                        'en': 'ingles del product 1', 
                        'sp': 'espanol del product 1', 
                        'fr': 'frances del product 1'
                        }
                    }]# CLOSE

    data['curious'] = [{
                    'fc_SubTitle':'Curious Facts',
                    'fc_Specs': {
                            'd1': ['1978','Spirit Cruises is founded in Norfolk, Virginia'], 
                            'd2': ['1978-1988','Spirit launches in Boston, Chicago, New York, Philadelphia and Washington DC'],  
                            'd3': ['1991','Odyssey launches at Navy Pier in Chicago'], 
                            'd4': ['1993-1995','Odyssey expands to Boston and Washington DC'], 
                            'd5': ['1996','Seadog, a speedboat excursion and architectural tour, is introduced at Chicago`s Navy Pier'], 
                            'd6': ['1998','Mystic Blue begins cruising in Chicago'], 
                            'd7': ['2006','Entertainment Cruises purchases Baltimore`s Harbor Cruises'], 
                            'd8': ['2006','ICV purchases Odyssey, Seadog and Spirit Cruises forming Entertainment Cruises'], 
                            'd9': ['2006','ICV purchases Odyssey, Seadog and Spirit Cruises forming Entertainment Cruises'], 
                            'd10': ['2006','ICV purchases Odyssey, Seadog and Spirit Cruises forming Entertainment Cruises'], 
                        },
                    }]# CLOSE

    data['contact'] = [{
                    'fc_SubTitle':'Contact',
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        }

                    }]# CLOSE

    data['Services'] = [{
                    'fc_Title':'Bateaux New York',
                    'fc_SubTitle':'Upscale. Exceptional.',
                    'fc_Category':'Cruise Waterfront',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Casual'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Get ready for the ultimate dining experience. Cruising year-round from Chelsea Piers, European-inspired Bateaux New York offers champagne brunch, lunch, dinner and full moon cruises, plus dozens of holiday cruises.', 
                        'sp': 'Preparate para la mas emocionante experiencia mientras comes una cena de lujo. Operamos todo el ano desde el puerto de Chelsea. Inspirado en el estilo europeo, ofrecemos champagne, brunch, lunch, comidas y cruceros de luna llena, ademas de muchas experiencias en distintas fiestas y aniversarios. ',
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['5678084712','6436108326','5238394461','6435936964','4551328098','2994274171'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Notes','Boarding is 30 minutes prior departure from Chelsea Pier, Pier 61 West 23rd Street and 12th Avenue. Dinner Sailing times: 7:00 to 10:00 pm. Brunch and Lunch Sailing Time: 12:00 to 2:00 pm. Schedule may change and boarding and departure time will be advised at time of confirmation of service.'], 
                            'd2': ['Dress Code','We request no jeans, shorts, tank tops, halter-tops, gym shoes or flip flops are worn on any cruise, Dinner: Jackets are recommended for men and cocktail attire for women.  Lunch: We recommend dressy casual attire, such as nice slacks and collared shirts. ']
                        },

                    },
                    # SECOND ITEM
                    {
                    'fc_Title':'Spirit Cruises',
                    'fc_SubTitle':'Fresh, Fun',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Casual'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Get ready for the time of your life aboard one of our two recently renovated ships departing from both New York and New Jersey. Sample a variety of dishes. Dance. And head topside to feel the wind in your hair. Join us aboard Spirit of New York and Spirit of New Jersey for a fun mix of dining, dancing, entertainment and skyline views. Cruising the Hudson River year-round, Spirit has a variety of lunch, dinner, moonlight and holiday cruises like Mother`s Day, plus dozens of themed cruises, to choose from.', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['5260765449','4204319897','7568051980','7930459506','6776873592','3067507519','3706970137','1390223211'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas'], 
                            'd2': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.']
                        }



                    },
                    # THIRD ITEM
                    {
                    'fc_Title':'Elite Private Yatch',
                    'fc_SubTitle':'Customizable. Private.',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Formal'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Host an exclusive event on New York Harbor on one of two private yachts. Atlantica or Manhattan Elite. Customize your charter with a variety of menu, decor, entertainment and route options. It`s your very own NYC private yacht. With sensational skyline views and completely customizable options, the Atlantica and Manhattan Elite offer two great ways to host an amazing and unique event aboard your own private yacht.', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['3621946540','4304442038','3964600599','9535813029','6822424476','2787176776','2731636522','1098120043','3419158938','5631973583'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas'], 
                            'd2': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.']
                        }



                    }



                    ] 

                    
    data['staff'] = [{
                    'fc_SubTitle':'Our Staff',
                    'fc_Descriptions': {
                        'en': 'There`s nothing our team loves more than helping people create unforgettable memories. Each year we serve over 1.5 million guests in 8 markets, so we do a whole lot of celebrating.Our passions range from finding the hottest new recipes, to helping guests select the perfect entertainment to enhance their event theme. We love stress-free weddings, corporate events that exceed expectations and events that are unique to the cities where we cruise.', 
                        'sp': 'espanol del product 1', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        }

                    }]





    return render_template("/sandbox/factcard.html", data=data) 



@sandbox.route("/facts/bike", methods=["GET", "POST"])
#@login_required
def facts_004():

    data = {}
    data['mask']= "mbf"
    data['mode']= "edit"

    # HOTEL INFO
    
    data['Name']= "Bike the Big Apple"
    data['S_Name']= 1 
    data['Address']= ""
    data['S_Address']= 1
    data['City']= ""
    data['S_City']= 2
    data['State']= ""
    data['S_State']= 3
    data['Zip']= ""
    data['S_Zip']= 2
    data['Industry']= ""
    data['S_Industry']= 4
    data['Description'] = [{
            #This USES THE FACTCARD MACRO
            #Title of the card
            'fc_SubTitle':'Full Description',
            'fc_DescriptionsSize':'1',
            'fc_Descriptions': {
                            'd1': ['en',1 ,'For over fourteen years, we have been providing the absolute best and safest way of bringing visitors and residents alike far off the beaten path to see, feel, and experience the real New York. You will find that on our tours, you will surely see the sights the typical tourist seldom sees!. Whether you want to maximize the amount of New York that you experience, want to learn a whole lot about what is behind our city, or just want to have an utter blast, come tour with us.'], 
                            'd2': ['sp',4,'(not spanish translation)'],  
                            'd3': ['it',4,'(not italian translation)'],
                        }

            }]# CLOSE


    data['OneLine'] = [{
                #This USES THE FACTCARD MACRO
                #Title of the card
                'fc_SubTitle':'One Line Description',
                'fc_DescriptionsSize':'2',
                'fc_Descriptions': {
                            'd1': ['en',1 ,'Welcome to New York`s premier bicycle touring company'], 
                            'd2': ['sp',4,'(not spanish translation)'],  
                            'd3': ['it',4,'(not italian translation)'], 
                        }
                }]# CLOSE
    #CONTACT
    data['S_Website']= 1
    data['Website']= "www.bikethebigapple.com"
    data['Mail']= "explore@bikethebigapple.com "
    data['S_Mail']= 1
    data['Phone']= "1-347-878-9809"
    data['S_Phone']= 1
    data['Fax']= ""
    data['S_Fax']= 4
    data['Newsletter']= ""
    data['S_Newsletter']= 5
    data['Blog']= ""
    data['S_Blog']= 1

    #DETAILS
    data['Founded']= "x18"
    data['S_Founded']= 1
    data['Closed']= "x18"
    data['SClosed']= 1
    data['ResAge']= "x09"
    data['S_ResAge']= 1
    data['Founded']= "x10"
    data['S_Founded']= 1
    data['payments']="x12"
    data['S_payments']=1
    #SOCIALMEDIA  
        # twitter
    data['SM1']= "http://twitter.com/bikethebigapple"
    data['S_SM1']= 1
        # facebook
    data['SM2']= "http://www.facebook.com/pages/Bike-the-Big-Apple/373495324184"
    data['S_SM2']= 1
        # instagram
    data['SM3']= ""
    data['S_SM3']= 1
        # youtube
    data['SM4']= ""
    data['S_SM4']= 1
        #Other Links
    data['LINK1']= "x23"
    data['S_LINK1']= 1
    data['LINK2']= "x23"
    data['S_LINK2']= 1
    data['LINK3']= "x23"
    data['S_LINK3']= 1
    data['LINK4']= "x23"
    data['S_LINK4']= 1
    #HISTORY
    data['Facts']= "x14"
    data['S_Facts']= 1
    data['Awards']= "x14"
    data['S_Awards']= 1
    data['FAQ']= "x14"
    data['FactualID']= "x14"
    data['history'] = [{
                    #This USES THE FACTCARD MACRO
                    #Title of the card
                    'fc_SubTitle':'History',
                    # Fields used:  History, History2, History3
                    'fc_Descriptions': {
                        'd1': ['en',1 ,'For well over a decade, we have been proud to be the largest, most successful company to offer fully-escorted bicycle tours throughout the five boroughs of the Big Apple. We take you beyond the usual tourist spots that bus and walking tours usually miss. And travelling by bike, you will come to appreciate, is the perfect way to truly experience the diverse neighborhoods of the city. On a bike tour, you will feel as though you are really part of the neighborhood. Walking tours & bus tours are certainly a nice way to see the city but bikes offer the best of both worlds (and more!). When compared to a day as pedestrian in New York, our leisurely paced rides are effortless and cover much more ground. And, you are able to interact with your surroundings much more than when on a bus. We feel certain you will leave with stories and photos that even the `natives` do not know about. '], 
                        'd2': ['sp',4,'(not spanish translation)'],  
                        'd3': ['it',4,'(not italian translation)'], 
                        },
                    # HISTORY PHOTOS
                    'fc_Owner':'teamamerica',
                    # PHOTOS
                    'fc_SmartPhotos': {
                            
                        }
                    
                    }]# CLOSE
    data['staff'] = [{
                    'fc_SubTitle':'Our Staff',
                    'fc_Descriptions': {
                        'd1': ['en',1,'We are not a bike rental shop that also does bike tours or a walking/bus tour company that also does bike tours. Bike tours are all that we do. It is our focus, so we do it right. '],
                        'd2': ['sp',4,'(not spanish translation)'],  
                        'd3': ['it',4,'(not italian translation)'],
                        
                        },
                    'fc_SmartPhotos': {
                            
                        }
                    }]# CLOSE

    data['curious'] = [{
                    'fc_SubTitle':'Facts',
                    'fc_Specs': {
                            'd1': ['Fact1','Each day, more than 250,000 cyclists ride in New York City, more than at any time in the last 25 years'], 
                            'd2': ['Fact2','A 2003 a report by Jacobsen showed that: The more bicyclists there are on the streets, the safer they are.'],  
                            'd3': ['Fact3','Bike riders are subject to the same laws as drivers in New York'], 
                            'd4': ['Fact4','Bike Friendly Business campaign exists to cultivate relationships with local businesses to encourage safe and lawful bicycling behavior'], 
                            'd5': ['Fact5','Eighty percent of the total cost of the 250 miles of bike lanes installed since 2006 was paid for by the federal government'], 
                            'd6': ['Fact6','Bike lanes can boost business. Streets that prioritize walking and biking, incorporated with amenities such as pedestrian plazas, have proven to boost local retail sales by 10-25 percent in cities around the world'], 
                            'd7': ['Fact7','Any person riding a bike can receive a ticket for not observing local transit laws.'], 
                            'd8': ['Fact8','there was a 13 percent increase in daily commuter bicycling between 2009 and 2010 alone']
                        },
                    }]# CLOSE

    data['contact'] = [{
                    'fc_SubTitle':'Contact',
                    'fc_List': {
                            'd1': ['Website','www.bikethebigapple.com'], 
                            'd2': ['Mail','explore@bikethebigapple.com'],  
                            'd3': ['Phone','1-347-878-9809'], 
                        }

                    }]# CLOSE

    data['Services'] = [

                # START ITEM A
                {
                    'fc_Title':'Tour A - The Ethnic Apple Tour.',
                    'S_fc_Title':1,
                    'fc_SubTitle':'Our ethnic mosaic tour',
                    'S_fc_SubTitle':1,
                    'fc_Category':'Bike Tour',
                    'S_fc_Category':1,
                    'fc_Specs': {
                            'd1': ['Category','Bike Tour'], 
                            'd2': ['Duration','7hrs'], 
                            'd3': ['MinAge','10'],  
                            'd4': ['Attire','Casual/ Sport'],
                            'd5': ['MinPax','4'], 
                            'd6': ['Season','All'], 
                        },
                    'S_fc_Specs':1,
                    'fc_Descriptions': {
                        'd1': ['en',1 ,'Great urban vistas that are typically not seen. Ethnic neighborhoods that are part of the unique mosaic of the city. This great bike tour combines them both!. Our tour begins with a ride over the imposing Queensboro Bridge high over the East River. Don`t be confused by this bridge`s identity. Immortalized in popular music under its nickname, the bridge has recently been officially renamed after one of the city`s most charismatic, zaniest mayors ever. Once we`ve entered Queens, we`ll head to Gantry State Park. At this historic location we can see restored `gantries` and learn about their critical role in the city`s commerce in the first part of the 20th century. The view across the East River, directly opposite the United Nations and what was the world`s tallest apartment building, provides an unforgettable photo opportunity.'], 
                        'd2': ['sp',4,'(not spanish translation)'],  
                        'd3': ['it',4,'(not italian translation)'],
                        },
                    'fc_Owner':'teamamerica',
                    'fc_SmartPhotos': {
                            'p1': [1,'4261055295','ok'], 
                            'p2': [2,'7452298333','ok'],  
                            'p3': [3,'7230214040','ok'], 
                            
                        },
                    'fc_Tags':[{'name': 'Includes', 
                                'list': ['bike','helmet','insurance'],
                                'status': 4
                                }, 
                            ],
                    'fc_Schedule': {
                            
                            'd1': ['Friday','10:100','17:00',1], 
                            'd2': ['On request','(min5 pax)','',4],
                            
                            },  
                    'fc_SmallNotes': {
                            'd1': ['Notes','This tour leaves every Friday, year-round, weather permitting, at 10:00 am from the Upper East Side of Manhattan (near the 68th street on the #6 subway) (precise address will be given after booking is made). It is approximately 15 miles and will last about 7 hours. (It is also available, by special request, any weekday)']
                        },
                        'S_fc_SmallNotes':1
                },
                # CLOSE ITEM
                # START ITEM B
                {
                    'fc_Title':'Tour B - The Delights of Brooklyn.',
                    'S_fc_Title':1,
                    'fc_SubTitle':'Brews, Views, Chocolate, and much more!',
                    'S_fc_SubTitle':1,
                    'fc_Category':'Bike Tour',
                    'S_fc_Category':1,
                    'fc_Specs': {
                            'd1': ['Category','Bike Tour'], 
                            'd2': ['Duration','7hrs'], 
                            'd3': ['MinAge','10'],  
                            'd4': ['Attire','Casual/ Sport'],
                            'd5': ['MinPax','4'], 
                            'd6': ['Season','All'], 
                        },
                    'S_fc_Specs':1,
                    'fc_Descriptions': {
                        'd1': ['en',1 ,'This special tour starts with a ride through the historic Lower East Side. Once the most densely populated neighborhood in the world(!), it is now a very `in` section with a thriving nightlife, as well as an authentic Soviet era, larger than life, statue of Lenin. Leaving Manhattan, we dive into the delights offered by the borough of Brooklyn as we pedal over the new Williamsburg Bridge bike path. We enter the `hip,` artistic neighborhood of Williamsburg and head to one of the Big Apple`s truly underground micro-brewery. Here you can sample its artisinal beers and ale, or stout on tap.'], 
                        'd2': ['sp',4,'(not spanish translation)'],  
                        'd3': ['it',4,'(not italian translation)'], 
                        },
                    'fc_Owner':'teamamerica',
                    'fc_SmartPhotos': {
                            'p1': [1,'7893794577','hi res'], 
                            'p2': [2,'3152079455','ok res'],  
                            'p4': [4,'5947166861','low res'], 
                        },
                    'fc_Tags':[{'name': 'Includes', 
                                'list': ['bike','helmet','insurance'],
                                'status': 4
                                }, 
                            ],
                    'fc_Schedule': {
                            
                            'd1': ['Saturday','10:15','17:00',1],
                            'd2': ['On request','(min5 pax)','',4],
                            
                            },  
                    'fc_SmallNotes': {
                            'd1': ['Notes','This tour leaves every Saturday, year-round, weather permitting, at 10:15 am, a few blocks from Union Square, of Manhattan (precise address will be given after booking is made). It is approximately 15 miles and will last about 7 hours. (It is also available, by special request, any weekday)']
                        },
                        'S_fc_SmallNotes':1

                },
                # CLOSE ITEM
                # START ITEM C
                {
                    'fc_Title':'Tour C - The Sensational Park and Soul Tour.',
                    'S_fc_Title':1,
                    'fc_SubTitle':'Bike the green Apple',
                    'S_fc_SubTitle':1,
                    'fc_Category':'Bike Tour',
                    'S_fc_Category':1,
                    'fc_Specs': {
                            'd1': ['Category','Bike Tour'], 
                            'd2': ['Duration','7hrs'], 
                            'd3': ['MinAge','10'],  
                            'd4': ['Attire','Casual/ Sport'],
                            'd5': ['MinPax','4'], 
                            'd6': ['Season','All'], 
                        },
                    'S_fc_Specs':1,
                    'fc_Descriptions': {
                        'd1': ['en',1 ,'On this bike tour of Central Park and Harlem, we start on the East Side of Manhattan, the city`s wealthiest neighborhood with extravagant brownstones and mansions. Next door is Central Park, which never fails to amaze with its sheer natural beauty (all man-made). As we pedal through the park we`ll visit Strawberry Fields, the only `beach` on Manhattan Island, the North Woods loch, an authentic 3500 year old obelisk, an $18 million lawn, as well as one of the largest stands of still surviving magnificent elms in the western world. Highlights in Harlem include a live Sunday gospel service, as well as a dramatic poetry reading by the home of the `Black` Carl Sandberg. We`ll see Clinton`s new office and a former grand synagogue that is now a major Black church! We`ll even hear `Sachmo` playing a composition by `the Duke` beneath an unusual statue to this great composer. Enjoy a `Bike and Bite` soul food lunch in Harlem. '], 
                        'd2': ['sp',4,'(not spanish translation)'],  
                        'd3': ['it',4,'(not italian translation)'], 
                        },
                    'fc_Owner':'teamamerica',
                    'fc_SmartPhotos': {
                            'p1': [1,'7078181063','hi res'], 
                            'p2': [2,'8885682710','ok res'],   
                        },
                    'fc_Tags':[{'name': 'Includes', 
                                'list': ['bike','helmet','insurance'],
                                'status': 4
                                }, 
                            ],
                    'fc_Schedule': {
                            
                            'd1': ['Saturday','10:15','17:00',1],
                            'd2': ['On request','(min5 pax)','',4],
                            
                            },  
                    'fc_SmallNotes': {
                            'd1': ['Notes','This tour leaves every Sunday, year-round, weather permitting, at 10:00 am from the Upper East Side of Manhattan (near the 68th street on the #6 subway) (precise address will be given after booking is made). It is approximately 12 miles and lasts about 5 hours. (It is also available, by special request, any weekday)']
                        },
                        'S_fc_SmallNotes':1

                },
                # CLOSE ITEM
                # START ITEM D
                {
                    'fc_Title':'Tour D - Secret Streets',
                    'S_fc_Title':1,
                    'fc_SubTitle':'From High Finance to Hidden Chinatown',
                    'S_fc_SubTitle':1,
                    'fc_Category':'Bike Tour',
                    'S_fc_Category':1,
                    'fc_Specs': {
                            'd1': ['Category','Bike Tour'], 
                            'd2': ['Duration','7hrs'], 
                            'd3': ['MinAge','10'],  
                            'd4': ['Attire','Casual/ Sport'],
                            'd5': ['MinPax','4'], 
                            'd6': ['Season','All'], 
                        },
                    'S_fc_Specs':1,
                    'fc_Descriptions': {
                        'd1': ['en',1 ,'Get ready for a true New York bike tour that has you smack in the middle of New York City`s action. First, we head past Union Square, the place of every protest, from basic to bizarre. Next, we`re in Greenwich Village at the Stonewall Inn, symbol of the Gay Liberation movement. From `the Village,` we ride along the Hudson River Greenway to Wall Street, where we are caught up in the frantic pace of high finance. Bankers rub shoulders with bike messengers, and brokers down their lunch as fast as the fluctuation of the stock market. Then to Ground Zero, to experience that tragic day and the agonizing months that followed. In typical New York fashion, the city has bounced back. The new Number 7 World Trade Center, with its amazing streaming video, captures this sense of optimism.'], 
                        'd2': ['sp',4,'(not spanish translation)'],  
                        'd3': ['it',4,'(not italian translation)'],
                        },
                    'fc_Owner':'teamamerica',
                    'fc_SmartPhotos': {
                            'p1': [1,'2602344552'], 
                            'p2': [2,'5054080943'],  
                        },
                    'fc_Tags':[{'name': 'Includes',
                                'list': ['bike','helmet','insurance'],
                                'status': 4
                                }, 
                            ],
                    'fc_Schedule': {
                            
                            'd1': ['Tuesday','10:15','17:00',1],
                            'd2': ['On request','(min5 pax)','',4], 
                            
                            },  
                    'fc_SmallNotes': {
                            'd1': ['Notes','This tour leaves every Tuesday, year-round, weather permitting, at 10:15 am, a few blocks from Union Square in Manhattan (precise address will be given after booking is made). It is approximately 14 miles and will last about 7 hours.']
                        },
                        'S_fc_SmallNotes':1

                },
                # CLOSE ITEM

                
            


                    ] 

    return render_template("/sandbox/factcard.html", data=data) 


@sandbox.route("/facts/mezcal", methods=["GET", "POST"])
#@login_required
def facts_005():

    data = {}
    data['mask']= "mbf"

    # HOTEL INFO
    
    data['Name']= "Bike the Big Apple" 
    data['Address']= ""
    data['City']= ""
    data['State']= ""
    data['Zip']= ""
    data['Industry']= ""
    data['Description'] = [{
            #This USES THE FACTCARD MACRO
            #Title of the card
            'fc_SubTitle':'Full Description',
            'fc_DescriptionsSize':'1',
            'fc_Descriptions': {
                'en': 'Mezcals are spirits distilled from the agave plant. Tequila is a mezcal, but tequila producers remove the agave solids before they distill. Tequila distillers put just the fermented juice into their stills, but artisan mezcal distillers include the fermented agave solids, meaning that well-made artisan mezcals from Oaxaca are richer and more complex than tequila. Alipus is distilled from local plantings of the agave espadin, the genetic ancestor of the blue agave Weber of tequila. Distillation takes place at small family distilleries in remote pueblos in Oaxaca state.', 
                'sp': 'espanol del product 1', 
                'fr': 'frances del product 1'
                }
            }]# CLOSE

    data['OneLine'] = [{
                #This USES THE FACTCARD MACRO
                #Title of the card
                'fc_SubTitle':'One Line Description',
                'fc_DescriptionsSize':'2',
                'fc_Descriptions': {
                    'en': 'Welcome to New York`s premier bicycle touring company', 
                    'sp': 'espanol del product 1', 
                    'fr': 'frances del product 1'
                    }
                }]# CLOSE
    #CONTACT
    data['Website']= "www.bikethebigapple.com"
    data['Mail']= "explore@bikethebigapple.com "
    data['Phone']= "1-347-878-9809"
    data['Fax']= ""
    data['Newsletter']= ""
    data['Blog']= ""

    #DETAILS
    data['Founded']= "x18"
    data['Closed']= "x18"
    data['ResAge']= "x09"
    data['Founded']= "x10"
    data['payments']="x12"
    #SOCIALMEDIA  
        # twitter
    data['SM1']= "bikethebigapple"
        # facebook
    data['SM2']= "http://www.facebook.com/pages/Bike-the-Big-Apple/373495324184"
        # instagram
    data['SM3']= ""
        # youtube
    data['SM4']= ""
        #Other Links
    data['LINK1']= "x23"
    data['LINK2']= "x23"
    data['LINK3']= "x23"
    data['LINK4']= "x23"
    #HISTORY
    data['Facts']= "x14"
    data['Awards']= "x14"
    data['FAQ']= "x14"
    data['FactualID']= "x14"
    data['history'] = [{
                    #This USES THE FACTCARD MACRO
                    #Title of the card
                    'fc_SubTitle':'History',
                    # Fields used:  History, History2, History3
                    'fc_Descriptions': {
                        'en': '', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    # HISTORY PHOTOS
                    'fc_Owner':'teamamerica',
                    # PHOTOS
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        }
                    

                    }]# CLOSE
    data['staff'] = [{
                    'fc_SubTitle':'Our Staff',
                    'fc_Descriptions': {
                        'en': 'We are not a bike rental shop that also does bike tours or a walking/bus tour company that also does bike tours. Bike tours are all that we do. It is our focus, so we do it right. ', 
                        'sp': 'espanol del product 1', 
                        'fr': 'frances del product 1'
                        }
                    }]# CLOSE

    data['curious'] = [{
                    'fc_SubTitle':'Facts',
                    'fc_Specs': {
                            'd1': ['Fact1','Each day, more than 250,000 cyclists ride in New York City, more than at any time in the last 25 years'], 
                            'd2': ['Fact2','A 2003 a report by Jacobsen showed that: The more bicyclists there are on the streets, the safer they are.'],  
                            'd3': ['Fact3','Bike riders are subject to the same laws as drivers in New York'], 
                            'd4': ['Fact4','Bike Friendly Business campaign exists to cultivate relationships with local businesses to encourage safe and lawful bicycling behavior'], 
                            'd5': ['Fact5','Eighty percent of the total cost of the 250 miles of bike lanes installed since 2006 was paid for by the federal government'], 
                            'd6': ['Fact6','Bike lanes can boost business. Streets that prioritize walking and biking, incorporated with amenities such as pedestrian plazas, have proven to boost local retail sales by 10-25 percent in cities around the world'], 
                            'd7': ['Fact7','Any person riding a bike can receive a ticket for not observing local transit laws.'], 
                            'd8': ['Fact8','there was a 13 percent increase in daily commuter bicycling between 2009 and 2010 alone']
                        },
                    }]# CLOSE

    data['contact'] = [{
                    'fc_SubTitle':'Contact',
                    'fc_List': {
                            'd1': ['Website','www.bikethebigapple.com'], 
                            'd2': ['Mail','explore@bikethebigapple.com'],  
                            'd3': ['Phone','1-347-878-9809'], 
                        }

                    }]# CLOSE

    data['Services'] = [

                # START ITEM A
                {
                    'fc_Title':'Tour A - The Ethnic Apple Tour.',
                    'fc_SubTitle':'Our ethnic mosaic tour',
                    'fc_Category':'Bike Tour',
                    'fc_Specs': {
                            'd1': ['Category','Bike Tour'], 
                            'd2': ['Duration','7hrs'], 
                            'd3': ['MinAge','10'],  
                            'd4': ['Attire','Casual/ Sport'],
                            'd5': ['MinPax','2'], 
                            'd6': ['Season','All'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Great urban vistas that are typically not seen. Ethnic neighborhoods that are part of the unique mosaic of the city. This great bike tour combines them both!. Our tour begins with a ride over the imposing Queensboro Bridge high over the East River. Don`t be confused by this bridge`s identity. Immortalized in popular music under its nickname, the bridge has recently been officially renamed after one of the city`s most charismatic, zaniest mayors ever. Once we`ve entered Queens, we`ll head to Gantry State Park. At this historic location we can see restored `gantries` and learn about their critical role in the city`s commerce in the first part of the 20th century. The view across the East River, directly opposite the United Nations and what was the world`s tallest apartment building, provides an unforgettable photo opportunity.', 
                        'sp': '',
                        'fr': ''
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['5678084712','6436108326','5238394461','6435936964','4551328098','2994274171'],
                    'fc_SmartPhotos': {
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Tags':[{'name': 'Includes', 
                                'list': ['bike','helmet','insurance']
                                }
                                
                            ],

                    'fc_Schedule': {
                            
                            'd5': ['Friday','10:100','17:00'], 
                            
                            },  
                        'fc_SmallNotes': {
                            'd1': ['Notes','This tour leaves every Friday, year-round, weather permitting, at 10:00 am from the Upper East Side of Manhattan (near the 68th street on the #6 subway) (precise address will be given after booking is made). It is approximately 15 miles and will last about 7 hours. (It is also available, by special request, any weekday)']
                        },

                },
                # CLOSE ITEM
                # START ITEM B
                {
                    'fc_Title':'Tour B - The Delights of Brooklyn.',
                    'fc_SubTitle':'Brews, Views, Chocolate, and much more!',
                    'fc_Category':'Bike Tour',
                    'fc_Specs': {
                            'd1': ['Category','Bike Tour'], 
                            'd2': ['Duration','7hrs'], 
                            'd3': ['MinAge','10'], 
                            'd4': ['Attire','Casual/ Sport'],
                            'd5': ['MinPax','2'], 
                            'd6': ['Season','All'], 
                        },
                    'fc_Descriptions': {
                        'en': 'This special tour starts with a ride through the historic Lower East Side. Once the most densely populated neighborhood in the world(!), it is now a very `in` section with a thriving nightlife, as well as an authentic Soviet era, larger than life, statue of Lenin. Leaving Manhattan, we dive into the delights offered by the borough of Brooklyn as we pedal over the new Williamsburg Bridge bike path. We enter the `hip,` artistic neighborhood of Williamsburg and head to one of the Big Apple`s truly underground micro-brewery. Here you can sample its artisinal beers and ale, or stout on tap. ', 
                        'sp': '',
                        'fr': ''
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['5678084712','6436108326','5238394461','6435936964','4551328098','2994274171'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Tags':[{'name': 'Includes', 
                                'list': ['bike','helmet','insurance']
                                }
                                
                            ],

                    'fc_Schedule': {
                            
                            'd5': ['Saturday','10:15','17:00'], 
                            
                            },  
                        'fc_SmallNotes': {
                            'd1': ['Notes','This tour leaves every Saturday, year-round, weather permitting, at 10:15 am, a few blocks from Union Square, of Manhattan (precise address will be given after booking is made). It is approximately 15 miles and will last about 7 hours. (It is also available, by special request, any weekday)']
                        },
                },
                # CLOSE ITEM
                # START ITEM C
                {
                    'fc_Title':'Tour C - The Sensational Park and Soul Tour.',
                    'fc_SubTitle':'Bike the green Apple',
                    'fc_Category':'Bike Tour',
                    'fc_Specs': {
                            'd1': ['Category','Bike Tour'], 
                            'd2': ['Duration','7hrs'], 
                            'd3': ['MinAge','10'], 
                            'd4': ['Attire','Casual/ Sport'],
                            'd5': ['MinPax','2'], 
                            'd6': ['Season','All'], 
                        },
                    'fc_Descriptions': {
                        'en': 'On this bike tour of Central Park and Harlem, we start on the East Side of Manhattan, the city`s wealthiest neighborhood with extravagant brownstones and mansions. Next door is Central Park, which never fails to amaze with its sheer natural beauty (all man-made). As we pedal through the park we`ll visit Strawberry Fields, the only `beach` on Manhattan Island, the North Woods loch, an authentic 3500 year old obelisk, an $18 million lawn, as well as one of the largest stands of still surviving magnificent elms in the western world. Highlights in Harlem include a live Sunday gospel service, as well as a dramatic poetry reading by the home of the `Black` Carl Sandberg. We`ll see Clinton`s new office and a former grand synagogue that is now a major Black church! We`ll even hear `Sachmo` playing a composition by `the Duke` beneath an unusual statue to this great composer. Enjoy a `Bike and Bite` soul food lunch in Harlem. ', 
                        'sp': '',
                        'fr': ''
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['5678084712','6436108326','5238394461','6435936964','4551328098','2994274171'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Tags':[{'name': 'Includes', 
                                'list': ['Tour guide','bike','helmet','insurance']
                                }
                                
                            ],

                    'fc_Schedule': {
                            
                            'd5': ['Saturday','10:15','17:00'], 
                            
                            },  
                        'fc_SmallNotes': {
                            'd1': ['Notes','This tour leaves every Sunday, year-round, weather permitting, at 10:00 am from the Upper East Side of Manhattan (near the 68th street on the #6 subway) (precise address will be given after booking is made). It is approximately 12 miles and lasts about 5 hours. (It is also available, by special request, any weekday)']
                        },
                },
                # CLOSE ITEM
                # START ITEM D
                {
                    'fc_Title':'Tour D - Secret Streets',
                    'fc_SubTitle':'From High Finance to Hidden Chinatown',
                    'fc_Category':'Bike Tour',
                    'fc_Specs': {
                            'd1': ['Category','Bike Tour'], 
                            'd2': ['Duration','7hrs'], 
                            'd3': ['MinAge','10'], 
                            'd4': ['Attire','Casual/ Sport'],
                            'd5': ['MinPax','2'], 
                            'd6': ['Season','All'], 
                            'd7': ['Price','$95'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Get ready for a true New York bike tour that has you smack in the middle of New York City`s action. First, we head past Union Square, the place of every protest, from basic to bizarre. Next, we`re in Greenwich Village at the Stonewall Inn, symbol of the Gay Liberation movement. From `the Village,` we ride along the Hudson River Greenway to Wall Street, where we are caught up in the frantic pace of high finance. Bankers rub shoulders with bike messengers, and brokers down their lunch as fast as the fluctuation of the stock market. Then to Ground Zero, to experience that tragic day and the agonizing months that followed. In typical New York fashion, the city has bounced back. The new Number 7 World Trade Center, with its amazing streaming video, captures this sense of optimism. ', 
                        'sp': '',
                        'fr': ''
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['5678084712','6436108326','5238394461','6435936964','4551328098','2994274171'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Tags':[{'name': 'Includes', 
                                'list': ['Tour guide','bike','helmet','insurance']
                                }
                                
                            ],

                    'fc_Schedule': {
                            
                            'd1': ['Tuesday','10:15','17:00'],
                            'd2': ['On request','(min5 pax)',''], 
                            
                            },  
                        'fc_SmallNotes': {
                            'd1': ['Notes','This tour leaves every Tuesday, year-round, weather permitting, at 10:15 am, a few blocks from Union Square in Manhattan (precise address will be given after booking is made). It is approximately 14 miles and will last about 7 hours.']
                        },
                },
                # CLOSE ITEM

                
            


                    ] 

    return render_template("/sandbox/factcard.html", data=data)     





@sandbox.route("/facts/123", methods=["GET", "POST"])
#@login_required
def facts_003():

    data = {}
    data['mask']= "mbf"

    # HOTEL INFO
    
    data['Name']= "" 
    data['Address']= "Pier 62, Chelsea Piers Suite 200"
    data['City']= "NewYork"
    data['State']= "NY"
    data['Zip']= "10011"
    data['Industry']= ""


    data['OneLine'] = [{
                #This USES THE FACTCARD MACRO
                #Title of the card
                'fc_SubTitle':'One Line Description',
                'fc_Descriptions': {
                    'en': 'Entertainment Cruises, dining cruises, yacht charters and sightseeing tours.', 
                    'sp': 'espanol del product 1', 
                    'fr': 'frances del product 1'
                    }
                }]# CLOSE

    data['Description'] = [{
            #This USES THE FACTCARD MACRO
            #Title of the card
            'fc_SubTitle':'Full Description',
            'fc_Descriptions': {
                'en': 'Get up close to the Statue of Liberty and travel under the iconic Brooklyn Bridge. Come out for a cruise on beautiful New York Harbor from your choice of our dock at Chelsea Piers or Lincoln Harbor Marina in Weehawken, New Jersey.', 
                'sp': 'espanol del product 1', 
                'fr': 'frances del product 1'
                }
            }]# CLOSE

    #CONTACT
    data['Website']= "http://www.bateauxnewyork.com/new-york-metro"
    data['Mail']= "x12"
    data['Phone']= "866-817-3463"
    data['Fax']= ""
    data['Newsletter']= ""
    data['Blog']= "http://www.entertainmentcruises.com/blog/"

    #DETAILS
    data['Founded']= "x18"
    data['Closed']= "x18"
    data['ResAge']= "x09"
    data['Founded']= "x10"
    data['payments']="x12"


    #SOCIALMEDIA  
        # twitter
    data['SM1']= "entertaincruise"
        # facebook
    data['SM2']= "https://www.facebook.com/BateauxNewYork"
        # instagram
    data['SM3']= "ecnewyork"
        # youtube
    data['SM4']= "ecnewyork"
        #Other Links
    data['LINK1']= "x23"
    data['LINK2']= "x23"
    data['LINK3']= "x23"
    data['LINK4']= "x23"


    #HISTORY
    data['Facts']= "x14"
    data['Awards']= "x14"
    data['FAQ']= "x14"
    data['FactualID']= "x14"
    data['history'] = [{
                    #This USES THE FACTCARD MACRO
                    #Title of the card
                    'fc_SubTitle':'History',
                    # Fields used:  History, History2, History3
                    'fc_Descriptions': {
                        'en': 'Entertainment Cruises roots date back to 1978 when the Spirit of Norfolk was christened and began cruising the historic Elizabeth River. Today, we have 30 boats across nine locations and host more than 1.5 million guests each year. Our shipmates feel privileged to share in our guests special celebrations - and help make their experiences with us memorable. ', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    # HISTORY PHOTOS
                    'fc_Owner':'teamamerica',
                    # PHOTOS
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        }

                    }]# CLOSE
    data['OurStaff'] = [{
                    'fc_Title':'Our Staff',
                    'fc_Descriptions': {
                        'en': 'ingles del product 1', 
                        'sp': 'espanol del product 1', 
                        'fr': 'frances del product 1'
                        }
                    }]# CLOSE

    data['curious'] = [{
                    'fc_SubTitle':'Curious Facts',
                    'fc_Specs': {
                            'd1': ['1978','Spirit Cruises is founded in Norfolk, Virginia'], 
                            'd2': ['1978-1988','Spirit launches in Boston, Chicago, New York, Philadelphia and Washington DC'],  
                            'd3': ['1991','Odyssey launches at Navy Pier in Chicago'], 
                            'd4': ['1993-1995','Odyssey expands to Boston and Washington DC'], 
                            'd5': ['1996','Seadog, a speedboat excursion and architectural tour, is introduced at Chicago`s Navy Pier'], 
                            'd6': ['1998','Mystic Blue begins cruising in Chicago'], 
                            'd7': ['2006','Entertainment Cruises purchases Baltimore`s Harbor Cruises'], 
                            'd8': ['2006','ICV purchases Odyssey, Seadog and Spirit Cruises forming Entertainment Cruises'], 
                            'd9': ['2006','ICV purchases Odyssey, Seadog and Spirit Cruises forming Entertainment Cruises'], 
                            'd10': ['2006','ICV purchases Odyssey, Seadog and Spirit Cruises forming Entertainment Cruises'], 
                        },
                    }]# CLOSE

    data['contact'] = [{
                    'fc_SubTitle':'Contact',
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        }

                    }]# CLOSE

    data['Services'] = [{
                    'fc_Title':'Bateaux New York',
                    'fc_SubTitle':'Upscale. Exceptional.',
                    'fc_Category':'Cruise Waterfront',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Casual'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Get ready for the ultimate dining experience. Cruising year-round from Chelsea Piers, European-inspired Bateaux New York offers champagne brunch, lunch, dinner and full moon cruises, plus dozens of holiday cruises.', 
                        'sp': 'Preparate para la mas emocionante experiencia mientras comes una cena de lujo. Operamos todo el ano desde el puerto de Chelsea. Inspirado en el estilo europeo, ofrecemos champagne, brunch, lunch, comidas y cruceros de luna llena, ademas de muchas experiencias en distintas fiestas y aniversarios. ',
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.'], 
                            'd2': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas']
                        },

                    },
                    # SECOND ITEM
                    {
                    'fc_Title':'Spirit Cruises',
                    'fc_SubTitle':'Fresh, Fun',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Casual'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra tortor sit amet justo volutpat, et varius libero lobortis. Nullam mattis turpis quis nunc efficitur suscipit. Sed eu vestibulum nisl, quis finibus leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus. Nam nibh quam, convallis a neque at, commodo cursus tortor. Morbi mollis purus sem, vel dapibus augue ornare malesuada. Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas'], 
                            'd2': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.']
                        }



                    },
                    # THIRD ITEM
                    {
                    'fc_Title':'Elite Private Yatch',
                    'fc_SubTitle':'Fresh, Fun',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Casual'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra tortor sit amet justo volutpat, et varius libero lobortis. Nullam mattis turpis quis nunc efficitur suscipit. Sed eu vestibulum nisl, quis finibus leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus. Nam nibh quam, convallis a neque at, commodo cursus tortor. Morbi mollis purus sem, vel dapibus augue ornare malesuada. Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas'], 
                            'd2': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.']
                        }



                    }



                    ] 

                    
    data['staff'] = [{
                    'fc_SubTitle':'Our Staff',
                    'fc_Descriptions': {
                        'en': 'There`s nothing our team loves more than helping people create unforgettable memories. Each year we serve over 1.5 million guests in 8 markets, so we do a whole lot of celebrating.Our passions range from finding the hottest new recipes, to helping guests select the perfect entertainment to enhance their event theme. We love stress-free weddings, corporate events that exceed expectations and events that are unique to the cities where we cruise.', 
                        'sp': 'espanol del product 1', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        }

                    }]





    return render_template("/sandbox/factcard.html", data=data) 








@sandbox.route("/facts/example", methods=["GET", "POST"])
#@login_required

def facts_00():
    data = {}
    data['mask']= "mbf"


    
    data['Example'] = [{
                    'fc_Title':'Bateaux New York',
                    'fc_SubTitle':'The best way to see the city , unique Brunch',
                    'fc_Category':'Cruise Waterfront',
                    'fc_Specs': {
                            'd1': ['Category','Dinning Cruise'], 
                            'd2': ['Minimum Booking Age','18'],  
                            'd3': ['Attire','Casual'], 
                        },
                    'fc_Descriptions': {
                        'en': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi viverra tortor sit amet justo volutpat, et varius libero lobortis. Nullam mattis turpis quis nunc efficitur suscipit. Sed eu vestibulum nisl, quis finibus leo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus. Nam nibh quam, convallis a neque at, commodo cursus tortor. Morbi mollis purus sem, vel dapibus augue ornare malesuada. Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas', 
                        'sp': '', 
                        'fr': 'frances del product 1'
                        },
                    'fc_Owner':'teamamerica',
                    'fc_Photos': ['6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439','6896928037','3498992745','3579873745','3836044439'],
                    'fc_SmartPhotos': {
                            'p1': [1,'6896928037','ok'], 
                            'p2': [2,'3498992745','ok'],  
                            'p3': [3,'3836044439','ok'], 
                            'p4': [4,'6896928037','ok'], 
                        },
                    'fc_Links': {
                            'd1': ['Website','http://www.myring.io'], 
                            'd2': ['NewYork TImes','http://www.myring.io'],  
                            'd3': ['TimeOut','http://www.myring.io'], 
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                }
                                
                            ],

                    'fc_Schedule': {
                            'd1': ['Monday','14:00','21:00'], 
                            'd2': ['Tuesday','10:00','21:00'],  
                            'd3': ['Wednesday','10:00','21:00'], 
                            'd4': ['Thursday','10:00','21:00'], 
                            'd5': ['Friday','10:00','21:00'], 
                            'd6': ['Saturday','11:00','19:00'], 
                            'd7': ['Sunday','11:00','19:00'], 
                            },  
                    'fc_List': {
                            'd1': ['Phone','444'], 
                            'd2': ['Fax','555'],  
                            'd3': ['Toll-free','333'], 
                            'd4': ['Sales','333'], 
                        },
                        'fc_SmallNotes': {
                            'd1': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.'], 
                            'd2': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas']
                        },
                    'fc_Tags':[{'name': 'Business', 
                                'list': ['a_001','a_002','a_003']
                                },
                                {'name': 'Beauty', 
                                'list': ['b_001','b_002','b_003']
                                },
                                {'name': 'Concierge', 
                                'list': ['c_001','c_002','c_003','c_004','c_005','c_006']
                                },
                                {'name': 'Food', 
                                'list': ['d_001','d_002','d_003','d_004','d_005','d_006','d_007','d_008']
                                },
                                {'name': 'Events', 
                                'list': ['e_001','e_002','e_003']
                                },
                                {'name': 'Fitness', 
                                'list': ['f_001','f_002','f_003','f_004','f_005']
                                },
                                {'name': 'Kids', 
                                'list': ['g_001','g_002','g_003','g_004']
                                },
                                {'name': 'Leisure', 
                                'list': ['h_001','h_002','h_003','h_004']
                                },
                                {'name': 'Medical', 
                                'list': ['i_001','i_002','i_003','i_004','i_005']
                                },
                                {'name': 'pets', 
                                'list': ['j_001','j_002','j_003','j_004']
                                },
                                {'name': 'Pool', 
                                'list': ['k_001','k_002','k_003','k_004','k_005']
                                },
                                {'name': 'Shopping', 
                                'list': ['l_001','l_002','l_003','l_004','l_005']
                                },
                                {'name': 'Smoking', 
                                'list': ['m_001','m_002','m_003']
                                },
                                {'name': 'Transportation', 
                                'list': ['n_001','n_002','n_003','n_004','n_005']
                                },
                            ],
                        'fc_SmallNotes': {
                            'd1': ['Cancellation Policy','Donec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestasDonec id pulvinar enim. Praesent finibus nibh ac sapien ultrices egestas'], 
                            'd2': ['Notes','Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam hendrerit malesuada lacus.']
                        }

                  



                    }]# CLOSE

 
    return render_template("/sandbox/factcard.html", data=data)






    


