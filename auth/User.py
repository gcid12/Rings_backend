# -*- coding: utf-8 -*-
import os
import sys
from AuthModel import AuthModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin



class User(UserMixin):
    def __init__(self, username=None, email=None, passhash=None, owner=None, isOrg=False, active=True, id=None):
        self.username = username
        self.email = email
        self.passhash = passhash
        self.isOrg = isOrg
        self.active = active
        self.isAdmin = False
        self.id = None

        if owner:
            self.owner = owner
        else:
            self.owner = username
        

        self.ATM = AuthModel()


    def set_user(self): 

        
        user = {}
        # Defaults
        
        #user['lastname'] = 'testlastname'
        #user['firstname'] = 'testfirstname'
        user['guid'] = 'testguid'
        user['salt'] = 'testsalt'
        # Via self
        user['username'] = self.username.lower()
        user['email'] = self.email.lower()  
        user['owner'] = self.owner 
        user['passhash'] = self.passhash
        

        print(user)

        if not self.isOrg:
            #You are registering a regular User
            if self.ATM.saas_create_user(user):
                print "new user id = %s " % user['username']       
                return user['username']
            else: 
                return False
        else:
            #You are registering an Organization
            if self.ATM.saas_create_orguser(user):
                print "new organization id = %s " % user['username']       
                return user['username']
            else: 
                return False

        

    def set_password_key(self,key):

        print('set_password_key:')
        print(self.id)
 
        return self.ATM.saas_create_password_key(self.id,key)

    def set_password(self,passhash):

        print('set_password:')
        print(self.id)
 
        return self.ATM.saas_set_password(self.id,passhash)


    def get_by_token(self, email, token):

        try:
            print('flag1')
            dbUser =self.ATM.userdb_get_user_by_email(email)
            print('flag2')
            print(dbUser)
            if dbUser:
                self.email = dbUser['value']['email']
                self.active = dbUser['value']['is_active'] 
                self.password = dbUser['value']['passhash']
                self.id = dbUser['value']['_id']
                return self
            else:
                return None
        except:
            print "Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1]
            print "there was an error"
            return None

    def get_user(self):

        try:
            #print('flag1')
            if self.email:
                dbUser =self.ATM.userdb_get_user_by_email(self.email)
            elif self.username:
                dbUser =self.ATM.userdb_get_user_by_handle(self.username)

            #print('flag2')
            #print(dbUser)
            if dbUser:
                self.profilepic = dbUser['value']['profilepic']
                self.name = dbUser['value']['name']
                self.email = dbUser['value']['email']
                self.url = dbUser['value']['url']
                self.location = dbUser['value']['location']
                self.active = dbUser['value']['is_active'] 
                self.password = dbUser['value']['passhash']
                self.id = dbUser['value']['_id']
                return self
            else:
                return None
        except:
            print "Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1]
            print "there was an error"
            return None

    def update_user_profile(self,request):

        dbUser =self.ATM.userdb_get_user_by_handle(self.username)
        changes = {}

        if dbUser:
            if request.form.get('profilepic') != dbUser['value']['profilepic']:
                print('profilepic changed!')
                changes['profilepic'] = request.form.get('profilepic')

            if request.form.get('name') != dbUser['value']['name']:
                print('name changed!')
                changes['name'] = request.form.get('name')
            
            if request.form.get('url') != dbUser['value']['url']:
                print('url changed!')
                changes['url'] = request.form.get('url')

            if request.form.get('location') != dbUser['value']['location']:
                print('location changed!')
                changes['location'] = request.form.get('location')

        return self.ATM.saas_update_user_profile(self.username,changes)
                

    

    def is_valid_password_key(self,email,key):

        try:
            #print('flag1')
            dbUser =self.ATM.userdb_get_user_by_email(email)
            #print('flag2')
            #print(dbUser)
            if dbUser['value']['new_password_key']==key:   
                return True
            else:
                return False
        except:
            print "Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1]
            print "There was an error validating the Key"
            return False


    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False




class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
