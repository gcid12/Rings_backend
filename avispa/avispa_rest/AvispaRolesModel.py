# AvispaRolesModel.py
from MainModel import MainModel

class AvispaRolesModel:


    def __init__(self):

        self.MAM = MainModel()
        self.user_database = 'myring_users'

        

    def get_role(self,depth,handle,ring=None,idx=None,collection=None,user_database=None):

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





            '''
            roles_dictionary = {}
            authorizations_dictionary = {}
            users_dictionary = {}

            if 'roles' in user_doc:
                #result_a = user_doc.roles
                #print('result_A:',result_a)

                for r1 in user_doc.roles:
                    roles_dictionary[r1['role']] = True
                    # For each role
                    if r1['authorizations']:
                        authorizations_dictionary[r1['role']] = r1['authorizations']
                    if r1['users']:
                        users_dictionary[r1['role']] = r1['users']



            roles = {}
            for ring_x in user_doc.rings:
                #For each ring
                if 'roles' in ring_x:
                    for r2 in ring_x.roles:
                        # For each role
                        if r2['authorizations']:
                            if authorizations_dictionary[r2['role']]:
                                authorizations_dictionary[r2['role']] += r2['authorizations']
                            else:
                                authorizations_dictionary[r2['role']] = r2['authorizations']
                        if r2['users']:
                            if users_dictionary[r2['role']]:
                                users_dictionary[r2['role']] += r2['users'] 
                            else:
                                users_dictionary[r2['role']] = r2['users']                




            result_b = roles[ring]
            print('result_B:',result_b)

            for rx in result_b:
                result_a.append(rx)
            
            print('resultSUM:',result_a)

            result = result_a
            '''

            

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
