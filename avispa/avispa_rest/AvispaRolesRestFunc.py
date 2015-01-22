# AvispaCollectionsRestFunc.py
from flask import redirect, flash
from AvispaModel import AvispaModel
from AvispaRolesModel import AvispaRolesModel

class AvispaRolesRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()
        self.ARM = AvispaRolesModel()


        
    def get(self,request,depth,handle,ring,idx,collection,api=False,*args):

        '''
        if ring == None:
            ring = '<any ring>'

        if idx == None:
            idx = '<any item>'

        if collection == None:
            collection = '<any collection>'
        '''


        # Show roles

        roles = self.ARM.get_role(depth,handle,ring,idx,collection)
        roledictionary = self.generate_roledictionary(handle,ring,idx,collection)

        d = {'template':'avispa_rest/roles.html','roles':roles,'roledictionary':roledictionary}
        return d

    


    def post(self,request,depth,handle,ring=None,idx=None,collection=None,api=False,*args):
        # Create new role in <handle>
        
        result = self.ARM.post_role(depth,handle,ring,idx,collection)

        if result:
            flash("The new role has been created")
            
            redirect = self.determine_redirect_route(depth)

            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error creating the role' , 'template':'avispa_rest/index.html'}
        
        return d

    def post_rq(self,request,depth,handle,ring=None,idx=None,collection=None,api=False,*args):
        
        d = {'template':'avispa_rest/post_rq_roles.html'}
        
        return d

    def put(self,request,depth,handle,ring=None,idx=None,collection=None,api=False,*args):
        # Edit a role in <handle>
        
        result = self.ARM.put_role(depth,handle,ring,idx,collection)

        if result:
            flash("The new role has been created")
            
            redirect = self.determine_redirect_route(depth)

            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error creating the role' , 'template':'avispa_rest/index.html'}
        
        return d

    def put_rq(self,request,depth,handle,ring=None,idx=None,collection=None,api=False,*args):
        
        d = {'template':'avispa_rest/put_rq_roles.html'}
        
        return d

    def delete_role(self,request,depth,handle,ring=None,idx=None,collection=None,api=False,*args):
        # Delete a role in <handle>
        
        result = self.ARM.delete_role(depth,handle,ring,idx,collection)

        if result:
            flash("The new role has been created")
            
            redirect = self.determine_redirect_route(depth)

            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error creating the role' , 'template':'avispa_rest/index.html'}
        
        return d


    def generate_roledictionary(self,handle,ring,idx,collection):

        roledictionary = {}

        if handle and (not ring and not idx):
            # A LEVEL
            roledictionary['get_a'] =  'See a list of all rings that belong to @'+handle       
            roledictionary['get_a_b'] =  'See a list of all items from any ring that belongs to @'+handle 
            roledictionary['get_a_b_c'] = 'See details from any item in any ring that belongs to @'+handle
            roledictionary['get_a_x'] = 'See a list of all collections that belong to @'+handle
            roledictionary['get_a_x_y'] = 'See details from any collection that belongs to @'+handle
            
            roledictionary['post_a'] = 'Create a new ring for @'+handle
            roledictionary['post_a_b'] = 'Create a new item in any ring that belongs to @'+handle
            roledictionary['post_a_x'] = 'Create a new collection for @'+handle

            roledictionary['put_a'] = 'Modify @'+handle+' settings'
            roledictionary['put_a_b'] = 'Modify schema from any ring that belongs to @'+handle
            roledictionary['put_a_b_c'] = 'Modify any item from any ring that belongs to @'+handle
            roledictionary['put_a_x_y'] = 'Modify any collection that belongs to @'+handle

            roledictionary['delete_a'] = 'Delete @'+handle
            roledictionary['delete_a_b'] = 'Delete any ring that belongs to @'+handle
            roledictionary['delete_a_b_c'] = 'Delete any item in any ring that belongs to @'+handle
            roledictionary['delete_a_x_y'] = 'Delete any collection that belongs to @'+handle

        elif (handle and ring) and not idx:
            # B LEVEL               
            roledictionary['get_a_b'] =  'See a list of all items from ring @'+handle+'/'+ring 
            roledictionary['get_a_b_c'] = 'See details from any item in ring @'+handle+'/'+ring           
            
            roledictionary['post_a_b'] = 'Create a new item in ring @'+handle+'/'+ring 
            
            roledictionary['put_a_b'] = 'Modify schema from ring @'+handle+'/'+ring 
            roledictionary['put_a_b_c'] = 'Modify any item from ring @'+handle+'/'+ring 
                       
            roledictionary['delete_a_b'] = 'Delete ring @'+handle+'/'+ring 
            roledictionary['delete_a_b_c'] = 'Delete any item from ring @'+handle+'/'+ring 

        elif (handle and ring) and not idx:
            # C LEVEL                       
            roledictionary['get_a_b_c'] = 'See details from item @'+handle+'/'+ring+'/'+idx          

            roledictionary['put_a_b_c'] = 'Modify item @'+handle+'/'+ring+'/'+idx
                                   
            roledictionary['delete_a_b_c'] = 'Delete item @'+handle+'/'+ring+'/'+idx 

        return roledictionary


    def determine_redirect_route(self,depth):

        if depth == '_a':
            return '/_roles/'+handle
        elif depth == '_a_b':
            return '/_roles/'+handle+'/'+ring
        elif depth == '_a_b_c':
            return '/_roles/'+handle+'/'+ring+'/'+idx
        elif depth == '_a_x':
            return '/_roles/'+handle+'/_collections'
        elif depth == '_a_x_y':
            return '/_roles/'+handle+'/_collections/'+collection






   