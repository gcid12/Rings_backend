# -*- coding: utf-8 -*-
import os
import sys
from AuthModel import AuthModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from MainModel import MainModel
from flask import flash, current_app



class User(UserMixin):
    def __init__(self, username=None, email=None, passhash=None, owner=None, isOrg=False, active=True, id=None, onlogin=False):
        self.username = username
        self.email = email
        self.passhash = passhash
        self.isOrg = isOrg
        self.active = active
        self.isAdmin = False
        self.id = None
        self.onlogin = onlogin

        if owner:
            self.owner = owner
        else:
            self.owner = username
        

        self.ATM = AuthModel()


    def set_user(self): 

        
        user = {}
        # Defaults coming via self

        user['username'] = self.username.lower()
        user['email'] = self.email.lower()  
        user['owner'] = self.owner 
        user['passhash'] = self.passhash
        user['onlogin'] = self.onlogin
        

        current_app.logger.debug(user)

        if not self.isOrg:
            #You are registering a regular User
            if self.ATM.saas_create_user(user):
                current_app.logger.debug("new user id = %s " % user['username'])     
                return user['username']
            else: 
                return False
        else:
            #You are registering an Organization
            if self.ATM.saas_create_orguser(user):
                current_app.logger.debug("new organization id = %s " % user['username'])     
                return user['username']
            else: 
                return False

        

    def set_password_key(self,key):

        current_app.logger.debug('set_password_key:')
        current_app.logger.debug(self.id)
 
        return self.ATM.saas_create_password_key(self.id,key)

    def set_password(self,passhash):

        current_app.logger.debug('set_password:')
        current_app.logger.debug(self.id)
 
        return self.ATM.saas_set_password(self.id,passhash)


    def get_by_token(self, email, token):

        try:
            current_app.logger.debug('flag1')
            dbUser =self.ATM.userdb_get_user_by_email(email)
            current_app.logger.debug('flag2')
            current_app.logger.debug(dbUser)
            if dbUser:
                self.email = dbUser['value']['email']
                self.active = dbUser['value']['is_active'] 
                self.password = dbUser['value']['passhash']
                self.id = dbUser['value']['_id']
                return self
            else:
                return None
        except:
            current_app.logger.debug("Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1])
            current_app.logger.debug("there was an error")
            return None

    def get_user(self):

        try:
            current_app.logger.debug('get_user_flag1')
            if self.email:
                current_app.logger.debug('self.email:'+self.email)
                dbUser =self.ATM.userdb_get_user_by_email(self.email)
            elif self.username:
                current_app.logger.debug('self.username'+self.username)
                dbUser =self.ATM.userdb_get_user_by_handle(self.username)

            
            if dbUser:

                current_app.logger.debug('DBUSER:'+dbUser['value']['name'])
                
                self.name = dbUser['value']['name']
                self.email = dbUser['value']['email']
                self.url = dbUser['value']['url']
                self.profilepic = dbUser['value']['profilepic']
                self.location = dbUser['value']['location']
                self.onlogin = dbUser['value']['onlogin']
                self.active = dbUser['value']['is_active'] 
                self.password = dbUser['value']['passhash']
                self.id = dbUser['value']['_id']
                return self
            else:
                current_app.logger.debug('User not found')
                return None
        except(KeyError):
            current_app.logger.debug("Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1])
            current_app.logger.debug("there was an error, we need to repair the user_document")

            preconditions = ['name','email','url','profilepic','location','onlogin']
            repaired = False
            for element_to_add in preconditions:
                MAM = MainModel()
                if MAM.repair_user_doc(element_to_add,dbUser['value']['_id']):
                    repaired = True
                    current_app.logger.debug('Repaired '+element_to_add+'. ')
                    #flash('Repaired '+element_to_add+'. ')

            #Let's try again
            if repaired:

                if self.email:
                    dbUser =self.ATM.userdb_get_user_by_email(self.email)
                elif self.username:
                    dbUser =self.ATM.userdb_get_user_by_handle(self.username)

                if dbUser:                   



                    self.name = dbUser['value']['name']
                    self.email = dbUser['value']['email']
                    self.url = dbUser['value']['url']
                    self.profilepic = dbUser['value']['profilepic']
                    self.location = dbUser['value']['location']
                    self.active = dbUser['value']['is_active'] 
                    self.password = dbUser['value']['passhash']
                    self.id = dbUser['value']['_id']
                    return self
                else:
                    return False

            else:
                return False


    def update_user_profile(self,request):

        dbUser =self.ATM.userdb_get_user_by_handle(self.username)
        changes = {}

        if dbUser:
            if request.form.get('profilepic') != dbUser['value']['profilepic']:
                current_app.logger.debug('profilepic changed!')
                changes['profilepic'] = request.form.get('profilepic')

            if request.form.get('name') != dbUser['value']['name']:
                current_app.logger.debug('name changed!')
                changes['name'] = request.form.get('name')
                mp_change = True
            
            if request.form.get('url') != dbUser['value']['url']:
                current_app.logger.debug('url changed!')
                changes['url'] = request.form.get('url')

            if request.form.get('location') != dbUser['value']['location']:
                current_app.logger.debug('location changed!')
                changes['location'] = request.form.get('location')

            if request.form.get('onlogin') != dbUser['value']['onlogin']:
                current_app.logger.debug('onlogin changed!')
                changes['onlogin'] = request.form.get('onlogin')



        return self.ATM.saas_update_user_profile(self.username,changes)

    

    def is_valid_password_key(self,email,key):

        try:
            #current_app.logger.debug('flag1')
            dbUser =self.ATM.userdb_get_user_by_email(email)
            #current_app.logger.debug('flag2')
            #current_app.logger.debug(dbUser)
            if dbUser['value']['new_password_key']==key:   
                return True
            else:
                return False
        except:
            current_app.logger.debug("Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1])
            current_app.logger.debug("There was an error validating the Key")
            return False


    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False




class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
