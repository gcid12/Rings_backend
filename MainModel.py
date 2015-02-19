# AuthModel.py
from MyRingCouchDB import MyRingCouchDB
from MyRingUser import MyRingUser
from env_config import COUCHDB_USER, COUCHDB_PASS
from couchdb.http import PreconditionFailed, ResourceNotFound
from datetime import datetime


class MainModel:

    def __init__(self):

        MCD = MyRingCouchDB()
        self.couch=MCD._instantiate_couchdb_as_admin()
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        self.user_database = 'myring_users'

        self.roles = {}
        self.roles['root'] = ['get_a','get_a_b','get_a_b_c','post_a','post_a_b','put_a','put_a_b','put_a_b_c','delete_a','delete_a_b','delete_a_b_c']
        self.roles['handle_owner'] = ['get_a_home','get_a_x','post_a_x','put_a_x_y','get_a','get_a_b','get_a_b_c','post_a','post_a_b','put_a','put_a_b','put_a_b_c','delete_a','delete_a_b','delete_a_b_c']
        self.roles['org_owner'] = ['get_a_home','get_a_p','post_a_p','delete_a_p_q','get_a_m','post_a_m','get_a_m_n','put_a_m_n','delete_a_m_n','put_a_m_n_settings','get_a_x','post_a_x','put_a_x_y','get_a','get_a_b','get_a_b_c','post_a','post_a_b','put_a','put_a_b','put_a_b_c','delete_a','delete_a_b','delete_a_b_c']
        self.roles['team_generic'] = ['get_a_home','get_a_m','get_a_x']
        self.roles['team_reader'] = ['get_a_home','get_a_m','get_a_m_n','get_a','get_a_b','get_a_b_c']
        self.roles['team_writer'] = ['get_a_home','get_a_m','get_a_m_n','get_a','get_a_b','get_a_b_c','post_a_b','put_a_b_c','delete_a_b_c']
        self.roles['team_admin'] = ['get_a_home','get_a_m','get_a_m_n','get_a','get_a_b','get_a_b_c','post_a','post_a_b','put_a','put_a_b','put_a_b_c','delete_a','delete_a_b','delete_a_b_c']
        self.roles['anonymous'] = ['get_a_home']

        self.roles['handle_member'] = ['get_a','get_a_b','get_a_b_c']
        self.roles['ring_owner'] = ['get_a_b','get_a_b_c','post_a','post_a_b','put_a_b','put_a_b_c','delete_a_b','delete_a_b_c']
        self.roles['item_owner'] = ['get_a_b_c','put_a_b_c','delete_a_b_c']
        self.roles['moderator'] = ['get_a_b','get_a_b_c','put_a_b_c','delete_a_b_c']
        self.roles['capturist'] = ['get_a_b','get_a_b_c','post_a_b','put_a_b_c','delete_a_b_c']
        self.roles['fact_checker'] = ['get_a_b_c','put_a_b_c']
        


        self.user_database = 'myring_users'

    #MAINMODEL
    def create_db(self,dbname):
        #print('Notice: Creating db ->>'+dbname)
        return self.couch.create(dbname)     

    #MAINMODEL
    def select_db(self,dbname):
        #print('Notice: Selecting db ->'+dbname)
        result = self.couch[dbname] 
        #print('db selected!')
        return result
         
    #MAINMODEL
    def delete_db(self,dbname):
        #print('Notice: Deleting db ->'+dbname)
        del self.couch[dbname] 
        return True

    #MAINMODEL
    def create_doc(self,dbname,id,doc):
        #print('Notice: Creating doc ->'+str(doc))
        #print('Notice: in DB ->'+dbname)
        #print('Notice: With ID ->'+id)
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
    def create_user(self,userd,dbname=None):

        if not dbname:
            dbname=self.user_database
        
        #print('flag1')
        self.db = self.select_db(dbname)
        #print('flag2')

        #print('Notice: Creating User ->'+userd['username'])
        auser = MyRingUser(
            email= userd['email'],
            billingemail = userd['email'],
            isorg = False, 
            passhash= userd['passhash'])

        auser._id = userd['username']
        storeresult = auser.store(self.db)
        return True

    #MAINMODEL
    def create_orguser(self,data,dbname=None):

        if not dbname:
            dbname=self.user_database
        
        #print('flag1')
        self.db = self.select_db(dbname)
        #print('flag2')


        people = {}
        people[data['username']] = {}
        people[data['username']]['addedby'] = data['username']
        people[data['username']]['added'] = str(datetime.now())

        teams = {}
        teams['owner'] = {}
        teams['owner']['members'] = []
        teams['owner']['members'].append(data['username'])
        teams['owner']['addedby'] = data['username']
        teams['owner']['added'] = str(datetime.now())
        
        #dict(data['username']:dict("addedby":data['username'],"added":datetime.now()))
        #dict(data['username']=dict("addedby"=data['username'],"added"=datetime.now()))

        people2 = {}
        people2['addedby'] = 'moco'
        people2['added'] = datetime.now()


        print('Notice: Creating User ->'+data['username'])
        auser = MyRingUser(
            email= data['username']+'@id.myring.io',
            billingemail = data['email'],  
            is_org = True,
            passhash= data['passhash'])

        #auser.people[data['username']] = {}
        auser.people.append(handle=data['owner'],addedby=data['owner'],added=datetime.now()) 
        auser.teams.append(teamname='owner',addedby=data['owner'],added=datetime.now())

        for team in auser.teams:
            if team.teamname == 'owner':
                print("Teamowner:",team)
                print("team.teamname:",team.teamname)
                print("team.members:",team.members, type(team.members))
                print("team.added:",team.added)
                team.members.append(handle=data['owner'],addedby=data['owner'],added=datetime.now())

        auser._id = data['username']
        storeresult = auser.store(self.db)
        return True

    def repair_user_doc(self,element,username,dbname=None):

        print('Repairing user_doc for '+username+'. Adding element: '+str(element))
        if not dbname:
            dbname=self.user_database

        db = self.select_db(dbname)
        user_doc = MyRingUser.load(db, username)

        print('user_doc:',user_doc,type(user_doc))
        print('element:',element,type(element))

    
        #if not hasattr(user_doc,str(element)): 
        try:
            user_doc[element]
        except(KeyError):
            print('repairflag')
            user_doc[element] = ''
            if user_doc.store(db):
                return True
            
        return False

    def add_team(self,handle,team,author,user_database=None):

        if not user_database:
            user_database=self.user_database
        
        db = self.select_db(user_database)
        user_doc = MyRingUser.load(db,handle)
        
        user_doc.teams.append(teamname=team,addedby=author,added=datetime.now())

        for teamd in user_doc.teams:
            
            if teamd['teamname'] == team:
                
                teamd.members.append(handle=author,addedby=author,added=datetime.now())
                teamd.roles.append(role='read_team',addedby=author,added=datetime.now())
                storeresult = user_doc.store(db)
                return True

        return False

    def delete_team(self,handle,team,user_database=None):

        if not user_database:
            user_database=self.user_database
        
        db = self.select_db(user_database)
        user_doc = MyRingUser.load(db,handle)

        count = 0
        for teamd in user_doc.teams:
            if teamd['teamname'] == team:
                del user_doc.teams[count] 
                if user_doc.store(db):
                    return True

            count += 1

                
        return False


    #MAINMODEL
    def is_org(self,username,user_database=None):
   
        result = self.select_user_doc_view('orgs/peopleteams',username)
        return result

    def user_exists(self,username,user_database=None):
   
        result = self.select_user_doc_view('auth/userbyhandle',username)
        return result

    #MAINMODEL
    def user_orgs(self,username,user_database=None):
   
        result = self.select_user_doc_view('orgs/user2orgs',username,10)
        return result

    #MAINMODEL  
    def select_user(self,dbname,username):
        self.db = self.select_db(dbname)
        #print('Notice: Selecting User ->'+username)
        return MyRingUser.load(self.db, username)


    def select_user_doc_view(self,dbview,key,batch=None,user_database=None):
 
        if not user_database : 
            user_database = self.user_database

        if not batch : 
            batch = 1

        db = self.select_db(self.user_database)
        options = {}
        options['key']=str(key)
        #Retrieving from ring/items view
        result = db.iterview(dbview,batch,**options)
        # This is a generator. If it comes empty, the username didn't exist.
        # The only way to figure that out is trying to iterate in it.
        #print('iterview result for '+dbview+' with key '+key+':',result)
        
        if batch == 1:
            for r in result:     
                return r['value']
        else:
            out = []
            for r in result:
                out.append(r['value'])
            return out


        return False


    #MAINMODEL  
    def delete_user(self,dbname,user):
        self.db = self.select_db(dbname)
        #print('Notice: Deleting User ->'+user)
        #del self.db[user]
        return True

    #MAINMODEL  
    def update_user(self,data,user_database=None):

        #print("update user data:")
        #print(data)

        #print("update_user 1:")

        if not user_database : 
            user_database = self.user_database

        #print("update_user 2:")

        self.db = self.couch[self.user_database]
        #print("update_user 3:")
        user =  MyRingUser.load(self.db, data['id'])
        #print("update_user 4:")
        #print(user)

        if user:
            #print("update_user 5:")

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
    def user_is_authorized(self,current_user,method,depth,handle,ring=None,idx=None,collection=None,team=None):

        # @method : is what is going to be checked against the user_authorization list
        # @depth : how deep to dig in the user_authorizations
        
        user_authorizations = []
        rolelist = []

        print('Method:', method)
        print('depth:',depth)

        
        if depth == '_a' or depth == '_a_b' or depth == '_a_b_c':

            if current_user == handle: 
                #This user is a Handle Owner
                print('This user is a Handle Owner') 
                user_authorizations = self.sum_role_auth(user_authorizations,'handle_owner')
            else:
                
                rolelist = self.user_belongs_org_team(current_user,handle)
                if rolelist:
                    print('rolelist1:',rolelist)
                    print('This user is a member of a team') 

                    for role in rolelist:
                            user_authorizations = self.sum_role_auth(user_authorizations,role)
                           

                    
                else:
                    print('This user is Anonymous 1')
                    user_authorizations += self.roles['anonymous']



            if depth == '_a_b' or depth == '_a_b_c':

                rolelist = self.user_belongs_org_team(current_user,handle,ring=ring)

                if rolelist:
                    print('rolelist2:',rolelist)
                    print('This user can act on this ring:'+ring) 

                    for role in rolelist:
                            user_authorizations = self.sum_role_auth(user_authorizations,role)


                
                '''
                user_doc = self.select_user(self.user_database,handle)          
                rings = user_doc['rings']

                for r in rings:

                    if r['ringname']==ring:
                        print('r:',r)

                        if 'owner' in r:
                            if current_user in r['owner']:
                                print('This user is a Ring Owner:'+r['ringname']+'_'+r['version']) 
                                user_authorizations = self.sum_role_auth(user_authorizations,'ring_owner')                      
                        else:
                            #This ring has no owner. Should correct. Orphans will become handle's property
                            r['owner'] = [handle] 
                            user_doc.store(self.db)
                            print('This user just became a Ring Owner of this orphan:'+r['ringname']+'_'+r['version']) 
                            user_authorizations = self.sum_role_auth(user_authorizations,'ring_owner')



                        if 'moderator' in r:
                            print('Moderator list:',r['moderator'])
                            if current_user in r['moderator']:
                                print('This user is a Ring Moderator:'+r['ringname']+'_'+r['version']) 
                                user_authorizations = self.sum_role_auth(user_authorizations,'moderator')

                        if 'capturist' in r:
                            print('Capturist list:',r['capturist'])
                            if current_user in r['capturist']:
                                print('This user is a Ring Capturist:'+r['ringname']+'_'+r['version'])
                                user_authorizations = self.sum_role_auth(user_authorizations,'capturist')
                '''
                            

                        
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
                                        print('Adding:'+role+'.')
                                        user_authorizations = self.sum_role_auth(user_authorizations,role)
                            
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
                                    user_authorizations = self.sum_role_auth(user_authorizations,role)


        elif depth == '_a_p':
            print('Testing authorizations for /_people section')

            team = 'owner'
            rolelist = self.user_belongs_org_team(current_user,handle,team)
            if rolelist:
                print('rolelist3:',rolelist)
                print('This user is a member of team:'+team)
                for role in rolelist:
                    user_authorizations = self.sum_role_auth(user_authorizations,role)

            else:
                print('This user is Anonymous 2')
                user_authorizations = self.sum_role_auth(user_authorizations,'anonymous')
                rolelist.append('anonymous')


        elif depth == '_a_m' or depth == '_a_m_n' or depth == '_a_m_n_settings':

            if not team:
                print('Testing authorizations for /_teams section')
                rolelist = self.user_belongs_org_team(current_user,handle)
            else:
                print('Testing authorizations for /_teams/'+team)
                rolelist = self.user_belongs_org_team(current_user,handle,team)
                      
            
            if rolelist:
                print('rolelist4:',rolelist)
                for role in rolelist:
                    user_authorizations = self.sum_role_auth(user_authorizations,role)
                    
            else:
                print('This user is Anonymous 3')
                user_authorizations = self.sum_role_auth(user_authorizations,'anonymous')
                rolelist.append('anonymous')

        elif depth == '_a_x' or depth == '_a_x_y':

            if current_user == handle: 
                #This user is a Handle Owner
                rolelist.append('handle_owner')
                print('This user is a Handle Owner') 
                user_authorizations = self.sum_role_auth(user_authorizations,'handle_owner')

            else:
                rolelist = self.user_belongs_org_team(current_user,handle)
                if rolelist:
                    print('rolelist5:',rolelist)
                    print('This user is a member of a team accesing a collection') 
                         
                    for role in rolelist:
                        user_authorizations = self.sum_role_auth(user_authorizations,role)
                           
                    '''
                    if role != 'org_owner':
                        user_authorizations = self.sum_role_auth(user_authorizations,'team_generic')
                    '''

                        
        








        #Here, add the retrieve of authorizations in deeper levels (just if required by depth)
        print('user_authorizations:',user_authorizations)

        method_parts = method.split('_')

        separator = '_'
        if 'rq' in method_parts:
            position = method_parts.index('rq')
            del method_parts[position]
            method = separator.join(method_parts)

        if 'rs' in method_parts:
            position = method_parts.index('rs')
            del method_parts[position]
            method = separator.join(method_parts)
       
        
        out={}
        out['user_authorizations'] = user_authorizations

        print('Method for this screen:',method)

        if method.lower() in user_authorizations:
            out['authorized'] = True
        else:
            out['authorized'] = False

        return out

    def sum_role_auth(self,user_authorizations,role):

        if role in self.roles:
            print('Adding role:'+role,self.roles[role])
            user_authorizations += self.roles[role]
        else:
            print(role+' was not found')

        return user_authorizations

        
    def is_org_owner(self,handle,org):

        return True


    def user_belongs_org_team(self,username,org,team=None,ring=None):
        print('Will chech if '+username+' belongs to a team ')
        rolelist = []
        result = self.select_user_doc_view('orgs/peopleteams',org)
        if result:

            if team: #Check if this usernname belongs to a team. Assign roles of that team only
                for teamd in result['teams']:
                    for member in teamd['members']:               
                        if member['handle'] == username:  
                            print(teamd['teamname']+' team has as member: '+member['handle'])
                            #Will add only those roles of a team the user belongs to
                            if teamd['teamname'] == 'owner':
                                rolelist.append('org_owner')
                            else:       
                                for role in teamd['roles']:
                                    rolelist.append(role['role'])
                        

            elif ring: #Check if this username can act on this ring
                for teamd in result['teams']:
                    print('flagx1')
                    for ringd in teamd['rings']:
                        print('flagx2',ringd['ringname'] , ring)
                        if ringd['ringname'] == ring: 
                            print('flagx3')
                            #This team acts on this ring!
                            for member in teamd['members']:
                                if member['handle'] == username:
                                    #This user belongs to this team that can act on this ring!
                                    for role in teamd['roles']:
                                        rolelist.append(role['role'])


            else: #This is only used in  /_home and /_teams to prove membership in ANY team
                for teamd in result['teams']:                    
                    for member in teamd['members']:
                        if member['handle'] == username: 
                            if teamd['teamname'] == 'owner':
                                rolelist.append('org_owner')
                            else:
                                rolelist.append('team_generic')
                   

                            
                            
            return rolelist
                            
        return False
