# MainModel.py

import couchdb
import logging
import random
import inspect
import pprint
from flask import current_app, g
from MyRingUser import MyRingUser
from couchdb.http import PreconditionFailed, ResourceNotFound
from datetime import datetime
from AvispaLogging import AvispaLoggerAdapter



class MainModel:

    def __init__(self):

      
        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})

        #self.lggr.debug('__init__()')
        
        self.couch = couchdb.Server(current_app.config['COUCHDB_SERVER'])
        self.couch.resource.credentials = (current_app.config['COUCHDB_USER'],current_app.config['COUCHDB_PASS'])
        self.user_database = 'myring_users'

        self.roles = {}
        self.roles['handle_owner'] = ['get_a_home','get_a_x','post_a_x','post_a_x_y','put_a_x_y','delete_a_x_y','get_a','get_a_b','get_a_b_c','post_a','post_a_b','put_a','put_a_b','put_a_b_c','delete_a','delete_a_b','delete_a_b_c']
        self.roles['org_owner'] = ['get_a_home','get_a_p','post_a_p','delete_a_p_q','get_a_m','post_a_m','get_a_m_n','put_a_m_n','delete_a_m_n','put_a_m_n_settings','put_a_m_n_invite','get_a_x','post_a_x','post_a_x_y','put_a_x_y','delete_a_x_y','get_a','get_a_b','get_a_b_c','post_a','post_a_b','put_a','put_a_b','put_a_b_c','delete_a','delete_a_b','delete_a_b_c']
        self.roles['team_generic'] = ['get_a_home','get_a_m','get_a_x']
        self.roles['team_reader'] = ['get_a_home','get_a_m','get_a_m_n','get_a','get_a_b','get_a_b_c']
        self.roles['team_writer'] = ['get_a_home','get_a_m','get_a_m_n','get_a','get_a_b','get_a_b_c','post_a_b','put_a_b_c','delete_a_b_c']
        self.roles['team_admin'] = ['get_a_home','get_a_m','get_a_m_n','get_a','get_a_b','get_a_b_c','post_a','post_a_b','put_a','put_a_b','put_a_b_c','delete_a','delete_a_b','delete_a_b_c','put_a_m_n_invite']
        self.roles['anonymous'] = ['get_a_home']

        self.roles['handle_member'] = ['get_a','get_a_b','get_a_b_c']
        self.roles['ring_owner'] = ['get_a_b','get_a_b_c','post_a','post_a_b','put_a_b','put_a_b_c','delete_a_b','delete_a_b_c']
        self.roles['item_owner'] = ['get_a_b_c','put_a_b_c','delete_a_b_c']
        self.roles['api_user'] = ['get_a_b','get_a_b_c']
        self.roles['moderator'] = ['get_a_b','get_a_b_c','put_a_b_c','delete_a_b_c']
        self.roles['capturist'] = ['get_a_b','get_a_b_c','post_a_b','put_a_b_c','delete_a_b_c']
        self.roles['fact_checker'] = ['get_a_b_c','put_a_b_c']
        


        self.user_database = 'myring_users'

    #MAINMODEL

    def create_db(self,dbname):
        
        return self.couch.create(dbname)     

    
    def stack_parser(self,stack):
        out = []
        for frame,filename,lineno,functionname,context,index in stack:

            parts = filename.split('/')
            skip = False
            for p in parts:
                if p in ['env','venv','system','lib','library']:
                    skip = True
                    break

                    
            if not skip:
                s = filename+':'+str(lineno)+' '+functionname+' '+str(context)
                print(s)
                    #s = filename+':'+str(lineno)+' '+functionname+' -> '+str(inspect.getargvalues(frame))
                    #out.append(s)

        return out




        

    #MAINMODEL
    def select_db(self,dbname):
        
        #self.lggr.debug(self.stack_parser(inspect.stack()))
        #self.lggr.debug()
        #self.lggr.debug(inspect.trace())
        #self.lggr.debug(inspect.getouterframes(inspect.currentframe())) 
              
        result = self.couch[dbname] 
        return result
         
    #MAINMODEL
    def delete_db(self,dbname):
        
        del self.couch[dbname] 
        return True

    #MAINMODEL
    def create_doc(self,dbname,id,doc):
        
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
        
        #self.lggr.debug('flag1')
        self.db = self.select_db(dbname)
        #self.lggr.debug('flag2')

        #self.lggr.debug('Notice: Creating User ->'+userd['username'])
        auser = MyRingUser(
            email= userd['email'],
            billingemail = userd['email'],
            isorg = False, 
            passhash= userd['passhash'],
            onlogin= userd['onlogin'])

        auser._id = userd['username']
        storeresult = auser.store(self.db)
        self.lggr.info(str(storeresult))
        return True

    #MAINMODEL
    def create_orguser(self,data,dbname=None):
        
        if not dbname:
            dbname=self.user_database
        
        #self.lggr.debug('flag1')
        self.db = self.select_db(dbname)
        #self.lggr.debug('flag2')


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


        self.lggr.debug('Notice: Creating User ->'+data['username'])
        auser = MyRingUser(
            email= data['username']+'@id.myring.io',
            billingemail = data['email'],  
            is_org = True,
            passhash= data['passhash'])

        #auser.people[data['username']] = {}
        auser.people.append(handle=data['owner'],addedby=data['owner'],added=datetime.now()) 
        auser.teams.append(teamname='owner',addedby=data['owner'],added=datetime.now())
        auser.teams.append(teamname='staff',addedby=data['owner'],added=datetime.now())

        for team in auser.teams:
            self.lggr.debug("Teamowner:",team)
            self.lggr.debug("team.teamname:",team.teamname)
            self.lggr.debug("team.members:",team.members, type(team.members))
            self.lggr.debug("team.added:",team.added)
            if team.teamname == 'owner':
                team.members.append(handle=data['owner'],addedby=data['owner'],added=datetime.now())
            elif team.teamname == 'staff':
                team.members.append(handle=data['owner'],addedby=data['owner'],added=datetime.now())
                team.roles.append(role='team_admin',addedby=data['owner'],added=datetime.now())



        auser._id = data['username']
        storeresult = auser.store(self.db)
        return True

    def repair_user_doc(self,element,username,dbname=None):

        if not dbname:
            dbname=self.user_database

        db = self.select_db(dbname)
        user_doc = MyRingUser.load(db, username)

        self.lggr.debug('user_doc:',user_doc,type(user_doc))
        self.lggr.debug('element:',element,type(element))

    
        #if not hasattr(user_doc,str(element)): 
        try:
            user_doc[element]
        except(KeyError):
            self.lggr.debug('repairflag')
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
                self.lggr.debug('flag at1')
                
                teamd.members.append(handle=author,addedby=author,added=datetime.now())
                teamd.roles.append(role='team_writer',addedby=author,added=datetime.now())
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
        #self.lggr.debug('Notice: Selecting User ->'+username)
        return MyRingUser.load(self.db, username)


    def select_user_doc_view(self,dbview,key,batch=None,user_database=None):


 
        if not user_database : 
            user_database = self.user_database

        if not batch : 
            batch = 1

        db = self.select_db(self.user_database)
        options = {}
        options['key']=str(key)
        result = db.iterview(dbview,batch,**options)
        # This is a generator. If it comes empty, the username didn't exist.
        # The only way to figure that out is trying to iterate in it.
        #self.lggr.debug('iterview result for '+dbview+' with key '+key+':',result)
        #options: key, startkey, endkey
        
        if batch == 1:
            for r in result:     
                return r['value']
        else:
            out = []
            for r in result:
                out.append(r['value'])
            return out


        return False

    def select_multiple_users_doc_view(self,dbview,batch,user_database=None):

        #BUG I tried factorizing this with select_user_doc_view but it is showing users as organizations. 
        # By just changing key for startkey

        if not user_database : 
            user_database = self.user_database

        if not batch : 
            batch = 500

        db = self.select_db(self.user_database)
        options = {}
        
        result = db.iterview(dbview,batch,**options)

        return result

    def select_ring_doc_view(self,ringdb,dbview,key=None,batch=None,showall=False):

        print('select_ring_doc_view::'+ringdb+','+dbview+','+str(key)+','+str(batch))


        if not batch : 
            batch = 1

        db = self.select_db(ringdb)
        options = {}
        if key:
            options['key']=str(key)

        result = db.iterview(dbview,batch,**options)
        # This is a generator. If it comes empty, the username didn't exist.
        # The only way to figure that out is trying to iterate in it.
        #self.lggr.debug('iterview result for '+dbview+' with key '+key+':',result)

        #print('gen len:',sum(1 for _ in result))
        
        if batch == 1:           
            for r in result: 
                if showall:
                    rr = {'key':r['key'],'id':r['id'],'value':r['value']}    
                    return rr
                else:
                    return r['value']
        else:           
            out = []
            for r in result:  
                if showall: 
                    rr = {'key':r['key'],'id':r['id'],'value':r['value']}       
                    out.append(rr) 
                else:
                    out.append(r['value'])         
            return out       
        return False


    def general_daily_activity(self,handle,user_database=None):

        #0. Create the general count dictionary (with 365 slots)
        #1. Retrieve all rings for this handle. Use view myringusers:ring/count
        #2. Rerieve all the rings of all organizations where this user has something to do
        #3. For each of the rings found:
        #3a: Load its database
        #3b: Call its dailyactivity view with key=handle
        #3c: If something is found iterate through each one of the rows looking for the last 365 days
        #3d: add "New" and "Update "counts to the general count for that specific day
        pass






    #MAINMODEL  
    def delete_user(self,dbname,user):
        self.db = self.select_db(dbname)
        #self.lggr.debug('Notice: Deleting User ->'+user)
        #del self.db[user]
        return True

    def append_to_user_field(self,handle,field,data,sublist=None,wherefield=None,wherefieldvalue=None,user_database=None):
        #This only to be used by fields that hold lists

        if not user_database : 
            user_database = self.user_database
        
        
        self.db = self.couch[self.user_database]
        user =  MyRingUser.load(self.db,handle)

        if user:

            #Preparing user[field]
            if field not in user:
                user[field] = []
            else:
                if type(user[field]) is not list:
                    self.lggr.debug('Cant append things to something that is not a list')
                    return False

        
            #Preparing user[field][x][sublist]
            if sublist:
                s = 0
                for u in user[field]:
                    if u[wherefield] == wherefieldvalue:
                        #This is assuming that user[field][s][sublist] exists and it is a list
                        if sublist not in u:
                            user[field][s][sublist] = []
                        elif type(user[field][s][sublist]) is not list:
                            self.lggr.debug('Cant append things to something that is not a list..')
                            return False

                        user[field][s][sublist].append(data)
                        break
                    s += 1

            else:
                user[field].append(data)


            if user.store(self.db):  
                self.lggr.debug('Data updated succesfully')             
                return True
            else:
                self.lggr.debug('Could not update user')
                return False

        else:

            self.lggr.debug('No user:'+handle)
            return False


    #MAINMODEL 
    def update_user(self,data,user_database=None):

        #self.lggr.debug("update user data:")
        #self.lggr.debug(data)

        #self.lggr.debug("update_user 1:")

        if not user_database : 
            user_database = self.user_database


        self.db = self.couch[self.user_database]
        #self.lggr.debug("update_user 3:")
        user =  MyRingUser.load(self.db, data['id'])
        #self.lggr.debug("update_user 4:")
        #self.lggr.debug(user)

        if user:
            #self.lggr.debug("update_user 5:")

            for field in data:
                if field!='id':
                    self.lggr.debug("Old Value:"+str(user[field]))
                    self.lggr.debug("New Value:"+str(data[field]))
                    user[field]=data[field]

            if user.store(self.db):  
                self.lggr.debug('Data updated succesfully')             
                return True
            else:
                self.lggr.debug('Could not update user')
                return False

        else:
            self.lggr.debug('No user'+data['_id'])


    #ROLEMODEL
    def user_is_authorized(self,current_user,method,depth,handle,ring=None,idx=None,collection=None,team=None,api=False):

        # @method : is what is going to be checked against the user_authorization list
        # @depth : how deep to dig in the user_authorizations
        
        user_authorizations = []
        rolelist = []

        self.lggr.debug('Method:'+ method)
        self.lggr.debug('depth:'+ depth)

        if api:
            user_authorizations = self.sum_role_auth(user_authorizations,'api_user')

        
        if depth == '_a' or depth == '_a_b' or depth == '_a_b_c':

            if current_user == handle: 
                #This user is a Handle Owner
                self.lggr.debug('This user is a Handle Owner') 
                user_authorizations = self.sum_role_auth(user_authorizations,'handle_owner')
            else:

                if depth != '_a_b' or depth != '_a_b_c':
                    #This is only important if you are not going to go deeper than _a
                
                    rolelist = self.user_belongs_org_team(current_user,handle,ring='*')
                    #rolelist = self.user_belongs_org_team(current_user,handle)
                 
                    if rolelist:

                        self.lggr.debug('rolelist1:'+str(rolelist))
                        self.lggr.debug('This user is a member of a team') 

                        for role in rolelist:
                                user_authorizations = self.sum_role_auth(user_authorizations,role)

       
                    
                else:
                    self.lggr.debug('This user is Anonymous 1')
                    user_authorizations += self.roles['anonymous']





            if depth == '_a_b' or depth == '_a_b_c':

                rolelist = self.user_belongs_org_team(current_user,handle,ring=ring)

                if rolelist:
                    self.lggr.debug('rolelist2:'+str(rolelist))
                    self.lggr.debug('This user can act on this ring:'+ring) 

                    for role in rolelist:
                            user_authorizations = self.sum_role_auth(user_authorizations,role)

     
                if depth == '_a_b_c':

                    db_ringname=str(handle)+'_'+str(ring) 
                    #self.lggr.debug('db_ringname:',db_ringname)
                    db = self.select_db(db_ringname)
                    #self.lggr.debug('db:',db)

                    options = {}
                    options['key']=str(idx)

                    #Retrieving from ring/items view
                    result = db.iterview('item/roles',1,**options)
                    self.lggr.debug('item/roles:'+str(result))

                    

                    try:
                        for roles in result:
                            self.lggr.debug('roles for item:',roles['value'])
                            #{u'fact_checker': [u'blalab', u'camaradediputados'], u'_public': False}

                            for role in roles['value']:
                                self.lggr.debug(roles['value'][role])
                                self.lggr.debug(type(roles['value'][role]))


                                if type(roles['value'][role]) is list and current_user in roles['value'][role]:
                                    self.lggr.debug('This user is an Item '+role+':'+ring) 
                                    if role in self.roles:
                                        self.lggr.debug('Adding:'+role+'.')
                                        user_authorizations = self.sum_role_auth(user_authorizations,role)
                            
                    except(ResourceNotFound):
                        #AUTOREPAIR

                        self.lggr.debug('item/roles db view does not exist. Will regenerate')

                        from avispa.avispa_rest.AvispaModel import AvispaModel  #Loading here because I don't want to load for all MainModel.py   #TO_REFACTOR
                        AVM = AvispaModel()
                        AVM.ring_set_db_views(db_ringname,'item/roles')

                        #Now issue the same request before the exception was thrown


                        for roles in result:
                            self.lggr.debug('roles for item:',roles['value'])
                            #{u'fact_checker': [u'blalab', u'camaradediputados'], u'_public': False}

                            for role in roles['value']:
                                self.lggr.debug(roles['value'][role])
                                self.lggr.debug(type(roles['value'][role]))


                                if type(roles['value'][role]) is list and current_user in roles['value'][role]:
                                    self.lggr.debug('This user is an Item '+role+':'+ring) 
                                    user_authorizations = self.sum_role_auth(user_authorizations,role)


        elif depth == '_a_p' or depth == '_a_p_q':
            self.lggr.debug('Testing authorizations for /_people section')

            team = 'owner'
            rolelist = self.user_belongs_org_team(current_user,handle,team)
            if rolelist:
                self.lggr.debug('rolelist3:',rolelist)
                self.lggr.debug('This user is a member of team:'+team)
                for role in rolelist:
                    user_authorizations = self.sum_role_auth(user_authorizations,role)

            else:
                self.lggr.debug('This user is Anonymous 2')
                user_authorizations = self.sum_role_auth(user_authorizations,'anonymous')
                rolelist.append('anonymous')


        elif depth == '_a_m' or depth == '_a_m_n' or depth == '_a_m_n_settings' or depth == '_a_m_n_invite':

            if not team:
                self.lggr.debug('Testing authorizations for /_teams section')
                rolelist = self.user_belongs_org_team(current_user,handle)
            else:
                self.lggr.debug('Testing authorizations for /_teams/'+team)
                rolelist = self.user_belongs_org_team(current_user,handle,team)
                      
            
            if rolelist:
                self.lggr.debug('rolelist4:',rolelist)
                for role in rolelist:
                    user_authorizations = self.sum_role_auth(user_authorizations,role)
                    
            else:
                self.lggr.debug('This user is Anonymous 3')
                user_authorizations = self.sum_role_auth(user_authorizations,'anonymous')
                rolelist.append('anonymous')

        elif depth == '_a_x' or depth == '_a_x_y':

            if current_user == handle: 
                #This user is a Handle Owner
                rolelist.append('handle_owner')
                self.lggr.debug('This user is a Handle Owner') 
                user_authorizations = self.sum_role_auth(user_authorizations,'handle_owner')

            else:
                rolelist = self.user_belongs_org_team(current_user,handle)
                if rolelist:
                    self.lggr.debug('rolelist5:',rolelist)
                    self.lggr.debug('This user is a member of a team accesing a collection') 
                         
                    for role in rolelist:
                        user_authorizations = self.sum_role_auth(user_authorizations,role)
                           
                    '''
                    if role != 'org_owner':
                        user_authorizations = self.sum_role_auth(user_authorizations,'team_generic')
                    '''

        



        #Here, add the retrieve of authorizations in deeper levels (just if required by depth)
        self.lggr.debug('Final user_authorizations:'+str(user_authorizations))

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

        self.lggr.debug('Method for this screen:'+method)

        if method.lower() in user_authorizations:
            out['authorized'] = True
        else:
            out['authorized'] = False

        return out

    def sum_role_auth(self,user_authorizations,role):

        if type(role) is dict:

            if role['role'] in self.roles:

                if role['ring']:
                    self.lggr.debug('Adding ring role:'+role['ring']+'_'+role['role'],self.roles[role['role']])
                    for r in self.roles[role['role']]:
                        user_authorizations.append(role['ring']+'_'+r)

            else:
                self.lggr.debug(role+' was not found')


        else:

            if role in self.roles:
                self.lggr.debug('Adding role:'+role+':'+str(self.roles[role]))
                user_authorizations += self.roles[role]
            else:
                self.lggr.debug(role+' was not found')

        return user_authorizations

        
    def is_org_owner(self,handle,org):

        return True


    def user_belongs_org_team(self,username,org,team=None,ring=None):
   
        self.lggr.debug('Will check if '+username+' belongs to a team ')
        rolelist = []
        result = self.select_user_doc_view('orgs/peopleteams',org)
        if result:

            if team: #Check if this usernname belongs to a team. Assign roles of that team only
                for teamd in result['teams']:
                    for member in teamd['members']:               
                        if member['handle'] == username:  
                            self.lggr.debug(teamd['teamname']+' team has as member: '+member['handle'])
                            #Will add only those roles of a team the user belongs to
                            if teamd['teamname'] == 'owner':
                                rolelist.append('org_owner')
                            
                            else:       
                                for role in teamd['roles']:
                                    rolelist.append(role['role'])
                        

            elif ring: #Check if this username can act on this ring
                for teamd in result['teams']:

                    self.lggr.debug('flagx1')

                    if teamd['teamname'] == 'owner':
                        self.lggr.debug('Checking is this user is in owner team:'+str(teamd['members']))
                        for member in teamd['members']:
                                
                                if member['handle'] == username:
                                    rolelist.append('org_owner')

                    elif teamd['teamname'] == 'staff':
                        for member in teamd['members']:
                            
                            if member['handle'] == username:
                                for role in teamd['roles']:                   
                                    rolelist.append(role['role'])

                                    
                    else:
                        for ringd in teamd['rings']:
                            self.lggr.debug('flagx2'+ringd['ringname']+str(ring))

                            if ring == '*':
                                for member in teamd['members']:
                                    if member['handle'] == username:

                                        #Ring specific permissions
                                        for role in teamd['roles']:                   
                                            rolelist.append({"ring":ringd['ringname'],"role":role['role']})

                                        #It will show a lot of ring specific permissions but you still need to have the team_generic
                                        # to be able to see your team
                                        rolelist.append('team_generic')
                                            

                            elif ringd['ringname'] == ring: 
                                self.lggr.debug('flagx3')
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

        #MAINMODEL
    def random_hash_generator(self,bits=36):  
        if bits % 8 != 0:
          bits = bits - (bits % 8)
        if bits < 8:
          bits = 8

        required_length = bits / 8 * 2
        
        s = hex(random.getrandbits(bits)).lstrip('0x').rstrip('L')
        if len(s) < required_length:
            return self.random_hash_generator(bits)
        else:
            return s
