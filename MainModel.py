# AuthModel.py
from MyRingCouchDB import MyRingCouchDB
from MyRingUser import MyRingUser
from env_config import COUCHDB_USER, COUCHDB_PASS


class MainModel:

    def __init__(self):

        MCD = MyRingCouchDB()
        self.couch=MCD._instantiate_couchdb_as_admin()
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        self.user_database = 'myring_users'

    #MAINMODEL
    def create_db(self,dbname):
        print('Notice: Creating db ->>'+dbname)
        return self.couch.create(dbname)     

    #MAINMODEL
    def select_db(self,dbname):
        print('Notice: Selecting db ->'+dbname)
        result = self.couch[dbname] 
        print('db selected!')
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

        print('Notice: Creating User ->'+data['username'])
        auser = MyRingUser(
            email= data['email'],
            firstname= data['firstname'],
            lastname=data['lastname'], 
            passhash= data['passhash'], 
            guid= data['guid'], 
            salt= data['salt'])

        auser._id = data['username']
        storeresult = auser.store(self.db)
        return True

    #MAINMODEL  Rarely Used directly. It is better to use the DB Views
    def select_user(self,dbname,username):
        self.db = self.select_db(dbname)
        print('Notice: Selecting User ->'+username)
        return MyRingUser.load(self.db, username)


    #MAINMODEL  
    def delete_user(self,dbname,user):
        self.db = self.select_db(dbname)
        print('Notice: Deleting User ->'+user)
        #del self.db[user]
        return True

    #MAINMODEL  
    def update_user(self,data,user_database=None):

        print("update user data:")
        print(data)

        print("update_user 1:")

        if not user_database : 
            user_database = self.user_database

        print("update_user 2:")

        self.db = self.couch[self.user_database]
        print("update_user 3:")
        user =  MyRingUser.load(self.db, data['id'])
        print("update_user 4:")
        print(user)

        if user:
            print("update_user 5:")



            


            for field in data:
                if field!='id':
                    print("Old Value:"+str(user[field]))
                    print("New Value:"+str(data[field]))
                    user[field]=data[field]

            if user.store(self.db):  
                print('Data updated succesfully')             
                return True
            else:
                print('Could not update user')
                return False

        else:
            print('No user'+data['_id'])


    #ROLEMODEL
    def user_is_authorized(self,current_user,method,depth,handle,ring,idx):
        #Go to the DB and figure out if current user is authorized to enter the route using the method indicated
        return True
        




