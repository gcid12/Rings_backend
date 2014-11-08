# AuthModel.py
from MyRingCouchDB import MyRingCouchDB
from MyRingUser import MyRingUser

class MainModel:

    def __init__(self):

        MCD = MyRingCouchDB()
        self.couch=MCD._instantiate_couchdb_as_admin()
        self.user_database = 'myring_users'

    #MAINMODEL
    def create_db(self,dbname):
        print('Notice: Creating db ->'+dbname)
        return self.couch.create(dbname)     

    #MAINMODEL
    def select_db(self,dbname):
        print('Notice: Selecting db ->'+dbname)
        result = self.couch[dbname] 
        print(result)
        return result
         
    #MAINMODEL
    def delete_db(self,dbname):
        print('Notice: Deleting db ->'+dbname)
        del self.couch[dbname] 
        return True

    #MAINMODEL
    def create_doc(self,dbname,id,doc):
        print('Notice: Creating doc ->'+str(doc))
        print('Notice: in DB ->'+dbname)
        print('Notice: With ID ->'+id)
        db=self.select_db(dbname)
        doc['_id']= id
        db.save(doc)
        #doc.store(db)
        return True 

    #MAINMODEL
    def create_user(self,data,dbname=None):

        if not dbname:
            dbname=self.user_database
        
        print('flag1')
        self.db = self.select_db(dbname)
        print('flag2')
        print(data)
        print('Notice: Creating User ->'+data['username'])
        auser = MyRingUser(email= data['email'],firstname= data['firstname'],lastname=data['lastname'], passhash= data['passhash'], guid= data['guid'], salt= data['salt'])
        auser._id = data['username']
        storeresult = auser.store(self.db)
        return True

    #MAINMODEL
    def select_user(self,dbname,user):
        self.db = self.select_db(dbname)
        print('Notice: Selecting User ->'+user)
        return MyRingUser.load(self.db, user)


    #MAINMODEL
    def delete_user(self,dbname,user):
        self.db = self.select_db(dbname)
        print('Notice: Deleting User ->'+user)
        #del self.db[user]
        return True

    #MAINMODEL
    def update_user(self,dbname,docid):
        pass
