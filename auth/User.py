# -*- coding: utf-8 -*-
import os
import sys

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)

from AuthModel import AuthModel


class User(UserMixin):
    def __init__(self, username=None, email=None, passhash=None, active=True, id=None):
        self.username = username
        self.email = email
        self.passhash = passhash
        self.active = active
        self.isAdmin = False
        self.id = None

        self.ATM = AuthModel()


    def set_user(self): 

        user = {}
        user['username'] = self.username.lower()
        user['email'] = self.email.lower()
        user['lastname'] = 'testlastname'
        user['firstname'] = 'testfirstname'
        user['passhash'] = self.passhash
        user['guid'] = 'testguid'
        user['salt'] = 'testsalt'

        print(user)

        if self.ATM.saas_create_user(user):
            print "new user id = %s " % user['username']       
            return user['username']
        else:
            return None

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
            print('flag1')
            if self.email:
                dbUser =self.ATM.userdb_get_user_by_email(self.email)
            elif self.username:
                dbUser =self.ATM.userdb_get_user_by_handle(self.username)

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


    def is_valid_password_key(self,email,key):

        try:
            print('flag1')
            dbUser =self.ATM.userdb_get_user_by_email(email)
            print('flag2')
            print(dbUser)
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
