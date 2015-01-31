# AvispaCollectionsRestFunc.py
import smtplib, urlparse, random
from flask import redirect, flash
from AvispaModel import AvispaModel
from AvispaRolesModel import AvispaRolesModel
from flanker.addresslib import address
from app import flask_bcrypt
from env_config import FROMEMAIL, FROMPASS

class AvispaRolesRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()
        self.ARM = AvispaRolesModel()


        
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

            email = str(email)

            key = flask_bcrypt.generate_password_hash(email+str(random.randint(0,9999)))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()

            #Next, log in to the server
            server.login(FROMEMAIL, FROMPASS)

            #Send the mail
            msg = "\r\n".join([
              "From:"+FROMEMAIL,
              "To: "+email,
              "Subject: "+handle+" has invited you to collaborate in the ring : "+ring,
              "",
              "Click here to start: "+host_url+"/_roles/"+handle+"/"+ring+"?rq=put&k="+key+"&e="+email
              ])
            #msg = "\nHello!" # The /n separates the message from the headers
            server.sendmail(FROMEMAIL, email, msg)
            server.quit()

            print(msg)
            print("Sending invitation email to: "+email)
            
        flash("Invitation emails sent.")


        #3. If it appears to be a MyRingID, check if it exists
        #4. If yes, translate it to an email and send ring subscription ulr/token
        #5. Keep history of everything
        

        redirect = '/_roles/'+handle
        d = {'redirect': redirect, 'status':201}
        return d


    def put_a_b(self,request,depth,handle,ring,idx,collection,api=False,*args):

        redirect = '/_roles/'+handle
        d = {'redirect': redirect, 'status':201}
        return d




    

   

   