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


    def save(self): 
        #newUser = models.User(email=self.email, password=self.password, active=self.active) 
        #newUser.save()

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

    
    def get_by_email(self, email):

        try:
            print('flag1')
            dbUser =self.ATM.userdb_get_user_by_email(email)
            print('flag2')
            print(dbUser)
            if dbUser:
                self.email = dbUser['value']['email']
                self.active = True #This needs to be implemented in the userdb
                self.password = dbUser['value']['passhash']
                self.id = dbUser['value']['_id']
                return self
            else:
                return None
        except:
            print "Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1]
            print "there was an error"
            return None

    def is_active(self):
        return True

    def get_mongo_doc(self):
        if self.id:
            return models.User.objects.with_id(self.id)
        else:
            return None

    def get_by_id(self, id):

        try:
            print('flag1')
            dbUser =self.ATM.userdb_get_user_by_id(id)
            print('flag2')
            print(dbUser)
            if dbUser:
                self.email = dbUser['value']['email']
                self.active = True #This needs to be implemented in the userdb
                self.password = dbUser['value']['passhash']
                self.id = dbUser['value']['_id']
                return self
            else:
                return None
        except:
            print "Notice: UnExpected error :", sys.exc_info()[0] , sys.exc_info()[1]
            print "there was an error"
            return None




class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
