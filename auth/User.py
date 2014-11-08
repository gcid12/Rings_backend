# -*- coding: utf-8 -*-
import os

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
        user['username'] = self.username
        user['email'] = self.email
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

        dbUser =self.ATM.userdb_get_user_by_email(email)
        #print(dbUser['key'])
        #print(dbUser['value'])

        
        if dbUser:
            self.email = dbUser['email']
            self.active = True #This needs to be implemented in the userdb
            self.id = dbUser['_id']
            return self
        else:
            return None
    
    def get_by_email_w_password(self, email):

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
        dbUser = models.User.objects.with_id(id)
        if dbUser:
            self.email = dbUser.email
            self.active = dbUser.active
            self.id = dbUser.id

            return self
        else:
            return None



class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
