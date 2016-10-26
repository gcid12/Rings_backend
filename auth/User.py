# -*- coding: utf-8 -*-
import os
import sys
import logging
from AuthModel import AuthModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from MainModel import MainModel
from flask import flash, current_app, g
from AvispaLogging import AvispaLoggerAdapter




class User(UserMixin):

    def __init__(self, username=None, email=None, passhash=None, owner=None, location=None, url=None, profilepic=None, name=None, isOrg=False, active=True, id=None, onlogin=False):

        
        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})

        self.lggr.debug('__init__()')

        self.username = username
        self.email = email
        self.location = location
        self.passhash = passhash
        self.location = location
        self.url = url
        self.profilepic = profilepic
        self.name = name
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
        user['location'] = self.location.lower()  
        user['owner'] = self.owner 
        user['location'] = self.location
        user['url'] = self.url
        user['profilepic'] = self.profilepic
        user['name'] = self.name
        user['passhash'] = self.passhash
        user['onlogin'] = self.onlogin

        self.lggr.info(user)

        if not self.isOrg:
            self.lggr.info('is an Org')
            #You are registering a regular User
            if self.ATM.saas_create_user(user):
                self.lggr.info("new user id = %s " % user['username'])     
                return user['username']
            else: 
                return False
        else:
            self.lggr.info('is NOT an Org')
            #You are registering an Organization
            if self.ATM.saas_create_orguser(user):
                self.lggr.info("new organization id = %s " % user['username'])     
                return user['username']
            else: 
                return False

        

    def set_password_key(self,key):

        self.lggr.info('set_password_key:')
        self.lggr.info(self.id)
 
        return self.ATM.saas_create_password_key(self.id,key)

    def set_password(self,passhash):

        self.lggr.info('set_password:')
        self.lggr.info(self.id)
 
        return self.ATM.saas_set_password(self.id,passhash)


    def get_by_token(self, email, token):

        try:
            
            dbUser =self.ATM.userdb_get_user_by_email(email)
            self.lggr.info(dbUser)
            if dbUser:
                self.email = dbUser['value']['email']
                self.location = dbUser['value']['location']
                self.active = dbUser['value']['is_active'] 
                self.password = dbUser['value']['passhash']
                self.id = dbUser['value']['_id']
                return self
            else:
                return None
        except:
            self.lggr.error("Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1])
            self.lggr.error("there was an error")
            return None

    def get_user(self):

        #raise Exception ('stop here')

        try:
            
            if self.email:
                self.lggr.debug('self.email:'+self.email)
                dbUser =self.ATM.userdb_get_user_by_email(self.email)
            elif self.username:
                self.lggr.info('START AUTHENTICATION:'+self.username)
                dbUser =self.ATM.userdb_get_user_by_handle(self.username)
            else:
                return None

            
            if dbUser:

                self.lggr.info("END AUTHENTICATION:%s"%dbUser['value']['name'])
                
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
                self.lggr.error('User: not found')
                return None
        except(KeyError):
            self.lggr.error("Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1])
            self.lggr.error("there was an error, we need to repair the user_document")

            preconditions = ['name','email','url','profilepic','location','onlogin']
            repaired = False
            for element_to_add in preconditions:
                MAM = MainModel()
                if MAM.repair_user_doc(element_to_add,dbUser['value']['_id']):
                    repaired = True
                    current_app.logger.info('Repaired '+element_to_add+'. ')
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
                self.lggr.info('profilepic changed!')
                changes['profilepic'] = request.form.get('profilepic')

            if request.form.get('name') != dbUser['value']['name']:
                self.lggr.info('name changed!')
                changes['name'] = request.form.get('name')
                mp_change = True
            
            if request.form.get('url') != dbUser['value']['url']:
                self.lggr.info('url changed!')
                changes['url'] = request.form.get('url')

            if request.form.get('location') != dbUser['value']['location']:
                self.lggr.info('location changed!')
                changes['location'] = request.form.get('location')

            if request.form.get('onlogin') != dbUser['value']['onlogin']:
                self.lggr.info('onlogin changed!')
                changes['onlogin'] = request.form.get('onlogin')



        return self.ATM.saas_update_user_profile(self.username,changes)

    

    def is_valid_password_key(self,email,key):

        try:
            #self.lggr.info('flag1')
            dbUser =self.ATM.userdb_get_user_by_email(email)
            #self.lggr.info('flag2')
            #self.lggr.info(dbUser)
            if dbUser['value']['new_password_key']==key:   
                return True
            else:
                return False
        except:
            self.lggr.error("Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1])
            self.lggr.error("There was an error validating the Key")
            return False


    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False




class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
