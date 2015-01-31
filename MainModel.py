# AuthModel.py
from MyRingCouchDB import MyRingCouchDB
from MyRingUser import MyRingUser
from env_config import COUCHDB_USER, COUCHDB_PASS
from couchdb.http import PreconditionFailed, ResourceNotFound


class MainModel:

    def __init__(self):

        MCD = MyRingCouchDB()
        self.couch=MCD._instantiate_couchdb_as_admin()
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        self.user_database = 'myring_users'

        self.roles = {}
        self.roles['root'] = ['get_a','get_a_b','get_a_b_c','post_a','post_a_b','put_a','put_a_b','put_a_b_c','delete_a','delete_a_b','delete_a_b_c']
        self.roles['handle_owner'] = ['get_a','get_a_b','get_a_b_c','post_a','put_a','delete_a','delete_a_b','delete_a_b_c']
        self.roles['ring_owner'] = ['get_a_b','get_a_b_c','post_a','post_a_b','put_a_b','put_a_b_c','delete_a_b','delete_a_b_c']
        self.roles['item_owner'] = ['get_a_b_c','put_a_b_c','delete_a_b_c']
        self.roles['moderator'] = ['get_a_b','get_a_b_c','put_a_b_c','delete_a_b_c']
        self.roles['capturist'] = ['get_a_b','get_a_b_c','post_a_b','put_a_b_c','delete_a_b_c']
        self.roles['fact_checker'] = ['get_a_b_c','put_a_b_c']
        self.roles['anonymous'] = ['get_a_b','get_a_b_c']

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

    def select_item_doc(self,handle,ringname,idx):

        
        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]
        AVM = AvispaModel()
        schema = AVM.ring_get_schema_from_view(handle,ringname) 
        RingClass = AVMring_create_class(schema)
        item_doc = RingClass.load(db,idx)
        return item_doc

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

    #MAINMODEL  
    def select_user(self,dbname,username):
        self.db = self.select_db(dbname)
        print('Notice: Selecting User ->'+username)
        return MyRingUser.load(self.db, username)


    def select_user_doc_view(self,dbview,key,user_database=None):
 
        if not user_database : 
            user_database = self.user_database

        db = self.select_db(self.user_database)
        options = {}
        options['key']=str(key)
        #Retrieving from ring/items view
        result = db.iterview(dbview,1,**options)
        # This is a generator. If it comes empty, the username didn't exist.
        # The only way to figure that out is trying to iterate in it.
        print(result)
        
        for r in result:     
            return r['value']

        return False


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

            for invitations in data:
                pass

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
        
        user_authorizations = []

        print('depth:',depth)

        
        if depth == '_a' or depth == '_a_b' or depth == '_a_b_c':

            if current_user == handle: 
                #This user is a Handle Owner
                print('This user is a Handle Owner')     
                user_authorizations += self.roles['handle_owner']


            if depth == '_a_b' or depth == '_a_b_c':

                
                user_doc = self.select_user(self.user_database,handle)          
                rings = user_doc['rings']

                for r in rings:

                    if r['ringname']==ring:
                        print('r:',r)

                        if 'owner' in r:
                            if current_user in r['owner']:
                                print('This user is a Ring Owner:'+r['ringname']+'_'+r['version']) 
                                user_authorizations += self.roles['ring_owner']                        
                        else:
                            #This ring has no owner. Should correct. Orphans will become handle's property
                            r['owner'] = [handle] 
                            user_doc.store(self.db)
                            print('This user just became a Ring Owner of this orphan:'+r['ringname']+'_'+r['version']) 
                            user_authorizations += self.roles['ring_owner']



                        if 'moderator' in r:
                            print('Moderator list:',r['moderator'])
                            if current_user in r['moderator']:
                                print('This user is a Ring Moderator:'+r['ringname']+'_'+r['version']) 
                                user_authorizations += self.roles['moderator']

                        if 'capturist' in r:
                            print('Capturist list:',r['capturist'])
                            if current_user in r['capturist']:
                                print('This user is a Ring Capturist:'+r['ringname']+'_'+r['version']) 
                                user_authorizations += self.roles['capturist']
                            

                        
                if depth == '_a_b_c':

                    db_ringname=str(handle)+'_'+str(ring) 
                    #print('db_ringname:',db_ringname)
                    db = self.select_db(db_ringname)
                    #print('db:',db)

                    options = {}
                    options['key']=str(idx)

                    #Retrieving from ring/items view
                    result = db.iterview('item/roles',1,**options)
                    print('item/roles:',result)

                    

                    try:
                        for roles in result:
                            print('roles for item:',roles['value'])
                            #{u'fact_checker': [u'blalab', u'camaradediputados'], u'_public': False}

                            for role in roles['value']:
                                print(roles['value'][role])
                                print(type(roles['value'][role]))


                                if type(roles['value'][role]) is list and current_user in roles['value'][role]:
                                    print('This user is an Item '+role+':'+ring) 
                                    if role in self.roles:
                                        user_authorizations += self.roles[role]
                            
                    except(ResourceNotFound):
                        #AUTOREPAIR

                        print('item/roles db view does not exist. Will regenerate')

                        from avispa.avispa_rest.AvispaModel import AvispaModel  #Loading here because I don't want to load for all MainModel.py   #TO_REFACTOR
                        AVM = AvispaModel()
                        AVM.ring_set_db_views(db_ringname,'item/roles')

                        #Now issue the same request before the exception was thrown


                        for roles in result:
                            print('roles for item:',roles['value'])
                            #{u'fact_checker': [u'blalab', u'camaradediputados'], u'_public': False}

                            for role in roles['value']:
                                print(roles['value'][role])
                                print(type(roles['value'][role]))


                                if type(roles['value'][role]) is list and current_user in roles['value'][role]:
                                    print('This user is an Item '+role+':'+ring) 
                                    if role in self.roles:
                                        user_authorizations += self.roles[role]






        #Here, add the retrieve of authorizations in deeper levels (just if required by depth)
        print('user_authorizations:',user_authorizations)

        method_parts = method.split('_')
        print('method_parts:',method_parts)
        
        
        m = method_parts[0]

        print('auth:',m.lower()+depth.lower())
        

        if m.lower()+depth.lower() in user_authorizations:
            return True
        else:
            return False

        




