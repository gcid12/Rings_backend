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





# REPORTS    

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






    


