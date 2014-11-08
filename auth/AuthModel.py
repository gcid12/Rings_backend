# AuthModel.py
import sys
from couchdb.http import PreconditionFailed
from couchdb.design import ViewDefinition

from MyRingCouchDB import MyRingCouchDB
from MyRingUser import MyRingUser
from MainModel import MainModel

class AuthModel:

    def __init__(self):

        MCD = MyRingCouchDB()
        self.couch=MCD._instantiate_couchdb_as_admin()
        self.user_database = 'myring_users'

        self.MAM = MainModel()


    #AUTHMODEL
    def admin_user_db_create(self,user_database=None,*args):

        if not user_database : 
            user_database = self.user_database


        try:          
            #self.db = self.couch[self.user_database]
            print('Notice: Entering TRY block')  
            self.db = self.MAM.create_db(user_database) 
            print('Notice: '+user_database+' database did not exist. Will create')

            self.userdb_set_db_views(user_database)
            print('Notice: DB Views Created')

            return True

        except(PreconditionFailed):  
            
            print('Notice: Entering EXCEPT(PreconditionFailed) block') 

            print "Notice: Expected error :", sys.exc_info()[0] , sys.exc_info()[1]
            #flash(u'Unexpected error:'+ str(sys.exc_info()[0]) + str(sys.exc_info()[1]),'error')
            self.rs_status='500'
            #raise

            # Will not get here because of 'raise'
            print "Notice: Since it already existed, selecting existing one"
            self.MAM.select_db(user_database)
            
            print('Notice: '+user_database+' database exists already')
            return False

    #AUTHMODEL
    def admin_user_create(self,data,user_database=None):

        if not user_database : 
            user_database = self.user_database

        auser = self.MAM.select_user(user_database, data['username'])

        print('Notice: User subtracted from DB ')

        if auser:
            print('Notice: '+data['username']+' exists already')
            return False

        else:
            auser = MyRingUser(email= data['email'],firstname= data['firstname'],lastname=data['lastname'], passhash= data['passhash'], guid= data['guid'], salt= data['salt'])
            auser._id = data['username']
            storeresult = auser.store(self.db)
            #print('Notice: Store Result -> '+storeresult)
            print('Notice: '+data['username'] +' created -> '+str(storeresult))
            return True

    #AUTHMODEL
    def userdb_set_db_views(self,user_database):

        db = self.couch[user_database]

        
        view = ViewDefinition('auth', 'userhash', 
                '''
                function(doc) {
                    if(doc.email) {
                        emit(doc.email,doc.passhash)
                    }
                }
                ''')

        view.get_doc(db)
        view.sync(db)

        return True

    #AUTHMODEL
    def userdb_get_userhash(self,key,user_database):

        db = self.couch[user_database]
        
        options = {}
        options['key']=key
        result = db.view('auth/userhash',**options)
               
        for row in result:

            item = {}
            item[u'key'] = row['key']
            item[u'value'] = row['value']
            

        return item