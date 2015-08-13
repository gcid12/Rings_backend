# AuthModel.py
import sys
import os
import errno
from couchdb.http import PreconditionFailed
from couchdb.design import ViewDefinition
from flask import flash, current_app,g
from AvispaLogging import AvispaLoggerAdapter


import couchdb
from MyRingUser import MyRingUser
from MainModel import MainModel
from env_config import COUCHDB_SERVER, COUCHDB_USER, COUCHDB_PASS, IMAGE_STORE

class AuthModel:

    def __init__(self):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})

        self.lggr.info('__init__()')

        self.couch = couchdb.Server(COUCHDB_SERVER)
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        #self.lggr.info('self.couch :ATM')
        #self.lggr.info(self.couch)
        #self.lggr.info('self.couch.resource.credentials :ATM')
        #self.lggr.info(self.couch.resource.credentials)
        self.user_database = 'myring_users'

        self.MAM = MainModel()

        self.officialsizes = {'r100':100,'r240':240,'r320':320,'r500':500,'r640':640,'r800':800,'r1024':1024}
        self.thumbnailsizes = {'t75':75,'t150':150}

    #AUTHMODEL
    def saas_create_user(self,user):
        #Added validation for SaaS users go here

        #Check if that username or email exists before trying to create the new user. Reject if TRUE
             
        if self.userdb_get_user_by_email(user['email']):
            self.lggr.info('User with this email already exists')
            flash('User with this email already exists','UI')
            return False

        self.lggr.info("self.userdb_get_user_by_handle")
        if self.userdb_get_user_by_handle(user['username']):
            self.lggr.info('Organization or User with this username already exists')
            flash('Organization or User with this username already exists','UI')
            return False



        if self.MAM.create_user(user):
            self.lggr.info("User created in DB. Attempting to create image folders...")
            self.create_user_imagefolder(user['username'])
            return True

        #AUTHMODEL
    def saas_create_orguser(self,user):
        #Added validation for SaaS users go here

        #Check if that username exists before trying to create the new orguser. Reject if TRUE     
        self.lggr.info("self.userdb_get_user_by_handle")
        if self.userdb_get_user_by_handle(user['username']):
            self.lggr.info('Organization or User with this username already exists')
            flash('Organization or User with this username already exists','UI')
            return False

        if self.MAM.create_orguser(user):
            self.lggr.info("Organization created in DB. Attempting to create image folders...")
            self.create_user_imagefolder(user['username'])
            return True

    def saas_create_password_key(self,user,key):

        self.lggr.info("saas_create_password_key")
        self.lggr.info(user)
        self.lggr.info(key)

        data = {}
        data['id']=user
        data['new_password_key']=key

        return self.MAM.update_user(data)

    def saas_set_password(self,user,passhash):

        self.lggr.info("saas_set_password")
        self.lggr.info(user)
        self.lggr.info(passhash)

        data = {}
        data['id']=user
        data['passhash']=passhash

        return self.MAM.update_user(data)

    def saas_update_user_profile(self,user,changes):

        changes['id']=user
        
        return self.MAM.update_user(changes)

    def create_user_imagefolder(self,username):         
        self.safe_create_dir(IMAGE_STORE+'/'+username+'/o') #Original folder

        for r in self.officialsizes:
            self.safe_create_dir(IMAGE_STORE+'/'+username+'/'+r)  # Scale-down version folders


        for t in self.thumbnailsizes:
            self.safe_create_dir(IMAGE_STORE+'/'+username+'/'+t)  # Thumbnail folders

        return True

    def safe_create_dir(self,path): 
        self.lggr.info(path)
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        self.lggr.info('Folder created:'+path)
        return True


    #AUTHMODEL
    def admin_user_db_create(self,user_database=None,*args):

        if not user_database : 
            user_database = self.user_database


        try:          
            #self.db = self.couch[self.user_database]
            self.lggr.info('Notice: Entering TRY block')

            self.db = self.MAM.create_db(user_database) 
            self.lggr.info('Notice: '+user_database+' database did not exist. Will create')

            self.userdb_set_db_views(user_database)
            self.lggr.info('Notice: DB Views Created')

            return True

        except(PreconditionFailed):  

            current_app.logger.info("Notice: Expected error :", sys.exc_info()[0] , sys.exc_info()[1])
            #flash(u'Unexpected error:'+ str(sys.exc_info()[0]) + str(sys.exc_info()[1]),'error')
            self.rs_status='500'
            #raise

            # Will not get here because of 'raise'
            current_app.logger.info("Notice: Since it already existed, selecting existing one")
            self.MAM.select_db(user_database)
            
            self.lggr.info('Notice: '+user_database+' database exists already')
            return False

    #AUTHMODEL
    def admin_user_create(self,data,user_database=None):

        if not user_database : 
            user_database = self.user_database
        
        
        db = self.couch[user_database]

        auser = self.MAM.select_user(user_database, data['username'])

        self.lggr.info('Notice: User subtracted from DB ')

        if auser:
            self.lggr.info('Notice: '+data['username']+' exists already')
            return False

        else:
            auser = MyRingUser(email= data['email'],firstname= data['firstname'],lastname=data['lastname'], passhash= data['passhash'], guid= data['guid'], salt= data['salt'])
            auser._id = data['username']
            storeresult = auser.store(db)
            
            self.lggr.info('Notice: '+data['username'] +' created -> '+str(storeresult))
            return True

    #AUTHMODEL
    def userdb_set_db_views(self,user_database=None):

        if not user_database : 
            user_database = self.user_database

        self.lggr.info('#couchdb_call:'+user_database+'->userdb_set_db_views()')
        db = self.couch[user_database]

        
        view = ViewDefinition('auth', 'userbyemail', 
                '''
                function(doc) {
                    if(doc.email) {
                        emit(doc.email,doc);
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)

        view = ViewDefinition('auth', 'userbyhandle', 
                '''
                function(doc) {
                    if(doc.email) {
                        emit(doc._id,doc);
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)

        view = ViewDefinition('auth', 'userbasic', 
                '''
                function(doc) {
                    if(doc.email) {
                        var x = {};
                        x['name'] = doc.name;  
                        x['location'] = doc.location;
                        x['is_org'] = doc.is_org;

                        if(doc.profilepic===''){
                            x['profilepic'] = '';
                        }else{        
                            parts = doc.profilepic.split(',')
                            if(parts[0]==''){
                              x['profilepic'] = parts[1];
                            }else{
                              x['profilepic'] = parts[0];
                            }
                        }

                        
                        
                        emit(doc._id,x);
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)

        view = ViewDefinition('rings', 'count', 
                '''
                function(doc) {
                    if(doc.email) {
                        var x = {};
                        for (var key in doc.rings){
                            if(!doc.rings[key]['deleted']){
                                x[doc.rings[key]['ringname']]=doc.rings[key]['count'];
                            }        
                        }
                        emit(doc._id,x);
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)


        view = ViewDefinition('rings', 'origin', 
                '''
                function(doc) {
                    if(doc.email) {
                        var x = {};
                            for (var key in doc.rings){
                                if(!doc.rings[key]['deleted']){
                                    x[doc.rings[key]['origin']] = doc.rings[key]['origin'];
                                }
                            }
                        emit(doc._id,x);
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)


        view = ViewDefinition('rings', 'roles', 
                '''
                function(doc) {
                    if(doc.email) {
                        var x = {};
                        for (var key in doc.rings){
                            if(!doc.rings[key]['deleted']){
                                x[doc.rings[key]['ringname']] = new Object();
                                x[doc.rings[key]['ringname']]['owner']=doc.rings[key]['owner'];
                                x[doc.rings[key]['ringname']]['capturist']=doc.rings[key]['capturist'];
                                x[doc.rings[key]['ringname']]['moderator']=doc.rings[key]['moderator'];
                            }
                        }
                        emit(doc._id,x);
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)


        view = ViewDefinition('orgs', 'peopleteams', 
                '''
                function(doc) {
                    if(doc.is_org) {
                        var x = {};
                        x['people']=doc.people;
                        x['teams']=doc.teams;
                        emit(doc._id,x);
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)


        view = ViewDefinition('orgs', 'user2orgs', 
                '''
                function(doc) {
                    if(doc.is_org) {
                        var x = {};
                        x['handle']=doc._id;
                        
                        x['name']=''
                        if(doc.name){
                            x['name']=doc.name;
                        }

                        x['profilepic']='';     
                        if(doc.profilepic){
                            if(doc.profilepic===''){
                                x['profilepic'] = '';
                            }else{        
                                parts = doc.profilepic.split(',')
                                if(parts[0]==''){
                                  x['profilepic'] = parts[1];
                                }else{
                                  x['profilepic'] = parts[0];
                                }
                            }
                        }

                        if(doc.collections){
                            x['collections'] = doc.collections;
                        }

                        for (var key in doc.people){
                            emit(doc.people[key]['handle'],x);          
                        }      
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)


        view = ViewDefinition('orgs', 'invitations', 
                '''
                function(doc) {
                    if(doc.is_org) {
                        var x = {};
                        x['invitations']=doc.invitations;
                        emit(doc._id,x);
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)

        return True

    #AUTHMODEL
    def userdb_get_user_by_email(self,email,user_database=None):

        #self.lggr.info('flag1.1')

        if not user_database : 
            user_database = self.user_database

        #self.lggr.info('flag1.2')
        
        db = self.couch[user_database]

        #self.lggr.info('flag1.3')
        
        options = {}
        options['key']=email
        result = db.view('auth/userbyemail',**options)
        #result = db.iterview('auth/userhash',1,**options)

        #self.lggr.info(result)

        #self.lggr.info('flag1.4')
        item = {}
               
        for row in result:

            item = {}
            item[u'id'] = row['id']
            item[u'key'] = row['key']
            item[u'value'] = row['value']

        #self.lggr.info('flag1.5')
            
        if item:
            return item
        else:
            return False

    #AUTHMODEL
    def userdb_get_user_by_handle(self,handle,user_database=None):

        #self.lggr.info('flag1.1')

        if not user_database : 
            user_database = self.user_database

        #self.lggr.info('flag1.2')
        
        db = self.couch[user_database]

        #self.lggr.info('flag1.3')
        
        options = {}
        # options will only accept this: 'key', 'startkey', 'endkey'
        options['key']=handle
        result = db.view('auth/userbyhandle',**options)
        #result = db.iterview('auth/userhash',1,**options)

        #self.lggr.info(result)

        #self.lggr.info('flag1.4')
        item = {}
               
        for row in result:

            item = {}
            item[u'id'] = row['id']
            item[u'key'] = row['key']
            item[u'value'] = row['value']

        #self.lggr.info('flag1.5')
            

        return item


    