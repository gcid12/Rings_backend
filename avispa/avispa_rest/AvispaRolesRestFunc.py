# AvispaCollectionsRestFunc.py
import urlparse, random
from flask import redirect, flash
from AvispaModel import AvispaModel
from AvispaRolesModel import AvispaRolesModel
from MainModel import MainModel
from EmailModel import EmailModel
from flanker.addresslib import address
from app import flask_bcrypt


class AvispaRolesRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()
        self.ARM = AvispaRolesModel()
        self.MAM = MainModel()
        self.EMM = EmailModel()
        self.user_database = 'myring_users'


        
    def get_a(self,request,depth,handle,ring,idx,collection,api=False,*args):

        result = self.ARM.get_role(handle)

        roles = {}

        for r in result:
            print('Raw:',r.value)
            for ring in r.value:
                print('ringrole:',ring) 
                roles[ring] = r.value[ring] 

        print('Roles:',roles)

        
        d = {'template':'avispa_rest/get_a_roles.html','roles':roles}

        return d  

    def get_a_b(self,request,depth,handle,ring,idx,collection,api=False,*args):

        redirect = '/_roles/'+handle
        d = {'redirect': redirect, 'status':201}
        return d



    def post_rq_a_b(self,request,depth,handle,ring=None,idx=None,collection=None,api=False,*args):
        

        d = {'template':'avispa_rest/post_rq_a_b_roles.html'}
        
        return d


    def post_a_b(self,request,depth,handle,ring=None,idx=None,collection=None,api=False,*args):
        
        #1. Parse the request.form.get('collaborators')  string separating emails from MyRing IDs

        collabraw = request.form.get('collaborators')

        valid_emails, invalid_emails = address.validate_list(collabraw, as_tuple=True)

        print('valid_emails:',valid_emails)
        print('invalid_emails:',invalid_emails)

        #2. If it is an email, send ring subscription url/token 

        o = urlparse.urlparse(request.url)
        host_url=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

        for email in valid_emails:

            user_doc = self.MAM.select_user_doc_view('auth/userbyemail',email)         

            if user_doc:
                #You are inviting an existing myRing user
                invite_email = user_doc['email']
            else:
                #You are inviting a soon to be myRing user
                invite_email = email

            token = flask_bcrypt.generate_password_hash(invite_email+str(random.randint(0,9999)))  
            to = str(invite_email)
            subject = handle+" has invited you to collaborate in the ring : "+ring
            content = "Click here to start: "+host_url+"/_roles/"+handle+"/"+ring+"?rq=put&k="+token+"&e="+to
            self.EMM.send_one_email(to,subject,content)
            
        flash("Invitation emails sent.")

        #3. If it appears to be a MyRingID, check if it exists

        for invite_handle in invalid_emails:

            user_doc = self.MAM.select_user_doc_view('auth/userbyhandle',invite_handle)
            
                
            if user_doc:
                #4. If yes, translate it to an email and send ring subscription ulr/token
                invite_email = user_doc['email']
   
                print(invite_handle+' exists and it has the following email:',invite_email)
                if invite_email not in valid_emails:

                    token = flask_bcrypt.generate_password_hash(invite_email+str(random.randint(0,9999)))  
                    to = str(invite_email)
                    subject = handle+" has invited you to collaborate in the ring : "+ring
                    content = "Click here to start: "+host_url+"/_roles/"+handle+"/"+ring+"?rq=put&k="+token+"&e="+to                  
                    self.EMM.send_one_email(to,subject,content)
                else:
                    print(invite_email+" and "+invite_handle+" point to the same user")
                
            else:
                print(invite_handle+' is not a MyRingID. What do you want to do with it?')
                flash('Could not find '+invite_handle+'. ')


        
        #5. Keep track of everything. We are going to store it in the user document



        

        #redirect = '/_roles/'+handle
        #d = {'redirect': redirect, 'status':201}
        #return d

        d = {'message': 'Using post_a_b_role for handle '+handle , 'template':'avispa_rest/index.html'}
        return d
       


    def put_a_b(self,request,depth,handle,ring,idx,collection,api=False,*args):

        redirect = '/_roles/'+handle
        d = {'redirect': redirect, 'status':201}
        return d


    def put_rq_a_b(self,request,depth,handle,ring,idx,collection,api=False,*args):

        #1. Check that the request is coming from the original guest (checking TOKEN and EMAIL vs counterparts in DB)
            #2. If yes, check if that email is already linked to an existing MyRing account.
               #3. If yes and it is a CAPTURIST. Load the Ring into the guest account
            #4. If no, redirect to /_register but storing original intent
            #5 Once created the user, the interface will redirect to step 1


        redirect = '/_roles/'+handle
        d = {'redirect': redirect, 'status':201}
        return d




    

   

   