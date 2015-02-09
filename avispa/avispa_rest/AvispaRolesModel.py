# AvispaRolesModel.py
from MainModel import MainModel

class AvispaRolesModel:


    def __init__(self):

        self.MAM = MainModel()
        self.user_database = 'myring_users'

    def get_role(self,handle,user_database=None):

        
        

        '''
        if not user_database : 
            user_database = self.user_database

        user_doc = self.MAM.select_user(user_database,handle)


        if 'rings' in user_doc:
            for ring in user_doc['rings']: 
                result[ring['ringname']] = {}            
                if 'owner' in ring:
                    result[ring['ringname']]['owner'] = ring['owner']
                if 'capturist' in ring:
                    result[ring['ringname']]['capturist'] = ring['owner']
                if 'moderator' in ring:
                    result[ring['ringname']]['moderator'] = ring['owner']
        '''

        if not user_database : 
            user_database = self.user_database

        db = self.MAM.select_db(user_database)

        options = {}
        options['key']=str(handle)

        #Retrieving from ring/items view
        roles = db.iterview('rings/roles',1,**options)

        return roles

        

    def x_get_role(self,depth,handle,ring=None,idx=None,collection=None,user_database=None):

        result = {}

        if not user_database : 
            user_database = self.user_database

        user_doc = self.MAM.select_user(user_database,handle)
        
        if depth == '_a':
            if 'roles' in user_doc:
                #result['local'] = user_doc.roles
                result['local'] = {}
                for rolx in user_doc.roles:
                    result['local'][rolx['role']] = rolx
            # show roles for <handle>
            
        elif depth == '_a_b':
            # show roles for ring <handle>/<ring>
            '''
            if 'roles' in user_doc:
                result['inherited'] = user_doc.roles
            '''
            if 'roles' in user_doc:
                #result['local'] = user_doc.roles
                result['inherited'] = {}
                print('user_doc.roles:',user_doc.roles)

                for rolx in user_doc['roles']:
                    
                    result['inherited'][rolx['role']] = rolx


            r = {}
            for ring_n in user_doc.rings:
                #For each ring
                if 'roles' in ring_n:
                    #I need to prepare a ring roles dictionary just to find the ring I'm interested in
                    r[ring_n['ringname']] = ring_n['roles']

            if ring in r:
                #Found it!
                result['local'] = {}
                for rolx2 in r[ring]:
                    result['local'][rolx2['role']] = rolx2

                #result['local'] = r[ring]





            

        elif depth == '_a_b_c':
            # show roles for item <handle>/<ring>/<idx>
            pass

        elif depth == '_a_x':
            # show roles for collections
            pass

            
        elif depth == '_a_x_y':
            # show roles for collection <handle>/_collections/<collection>
            roles = {}
            for collection in user_doc.collections:
                if 'roles' in collection:
                    roles[ring['collectionname']] = collection.roles
            result =  roles
            

        print('Roles:',result)
        return result


    def post_role(self,depth,handle,ring=None,idx=None,collection=None):

        result = False
        
        if depth == '_a':
            pass
        elif depth == '_a_b':
            pass
        elif depth == '_a_b_c':
            pass
        elif depth == '_a_x':
            pass
        elif depth == '_a_x_y':
            pass

        return result

    def put_role(self,depth,handle,ring=None,idx=None,collection=None):

        result = False
        
        if depth == '_a':
            pass
        elif depth == '_a_b':
            pass
        elif depth == '_a_b_c':
            pass
        elif depth == '_a_x':
            pass
        elif depth == '_a_x_y':
            pass

        return result

    def delete_role(self,depth,handle,ring=None,idx=None,collection=None):

        result = False
        
        if depth == '_a':
            pass
        elif depth == '_a_b':
            pass
        elif depth == '_a_b_c':
            pass
        elif depth == '_a_x':
            pass
        elif depth == '_a_x_y':
            pass

        return result