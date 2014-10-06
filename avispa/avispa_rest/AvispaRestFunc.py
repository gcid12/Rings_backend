from RingBuilder import RingBuilder
from AvispaModel import AvispaModel

class AvispaRestFunc:

    def __init__(self):
        self.avispamodel = AvispaModel()
    
    # /a

    # GET/a
    def get_a(self,request,handle,*args):

        ringlist = self.avispamodel.user_get_rings(handle)
        d = {'message': 'Using get_a for handle '+handle , 'template':'avispa_rest/get_a.html', 'ringlist':ringlist}
    	return d

    def get_rq_a(self,request,handle,*args):
        # To find someting in all rings
        d = {'message': 'Using get_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_rs_a(self,request,handle,*args):
        d = {'message': 'Using get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_q_a(self,request,handle,*args):
        d = {'message': 'Using get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    # POST/a
    def post_a(self,request,handle,*args):

       
        RB = RingBuilder()
        if RB.JSONRingGenerator(request,handle):
            print('200')
        

    	d = {'message': 'Using post_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a(self,request,handle,*args):
        d = {'message': 'Using post_rq_a for handle '+handle , 'template':'avispa_rest/post_rq_a.html'}
        return d

    def post_rs_a(self,request,handle,*args):
        d = {'message': 'Using post_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a
    def put_a(self,request,handle,*args):
    	d = {'message': 'Using put_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a(self,request,handle,*args):
        d = {'message': 'Using put_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a(self,request,handle,*args):
        d = {'message': 'Using put_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a
    def patch_a(self,request,handle,*args):
    	d = {'message': 'Using patch_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a(self,request,handle,*args):
        d = {'message': 'Using patch_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a(self,request,handle,*args):
        d = {'message': 'Using patch_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a
    def delete_a(self,request,handle,*args):
    	d = {'message': 'Using delete_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a(self,request,handle,*args):
        d = {'message': 'Using delete_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d
    
    def delete_rs_a(self,request,handle,*args):
        d = {'message': 'Using delete_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a
    def search_a(self,request,handle,*args):
        d = {'message': 'Using search_a for handle '+handle , 'template':'avispa_rest/search_a.html'}
        return d

    def search_rq_a(self,request,handle,*args):
        d = {'message': 'Using search_rq_a for handle '+handle , 'template':'avispa_rest/search_rq_a.html'}
        return d

    # /a/b
    
    #GET /a/b
    def get_a_b(self,request,handle,ring,*args):
    	d = {'message': 'Using get_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/get_a_b.html'}
        return d

    def get_rq_a_b(self,request,handle,ring,*args):
        # To find something inside of this ring
        d = {'message': 'Using get_rq_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/get_rq_a_b.html'}
        return d

    def get_rs_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using get_rs_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #POST /a/b
    def post_a_b(self,request,handle,ring,*args):
        '''
        Creates new item
        '''        
        idx = self.avispamodel.post_a_b(request,handle,ring)

        if idx:
            print('Awesome , you just saved the item to the DB')
            msg = 'Item saved with id: '+idx

    	d = {'message': msg+' -> handle: '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b(self,request,handle,ring,*args):
        '''
        Form to create new item
        '''
        blueprint = self.avispamodel.ring_get_blueprint(handle,ring)
        ringblueprint = blueprint['rings'][0]
        fieldsblueprint = blueprint['fields']
        numfields = len(fieldsblueprint)

        d = {'message': 'Using post_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/post_rq_a_b.html', 
             'ringblueprint':ringblueprint,
             'fieldsblueprint':fieldsblueprint,
             'numfields':numfields,
             'item':{} }
        return d

    def post_rs_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using post_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_b(self,request,handle,ring,*args):
    	d = {'message': 'Using put_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a_b(self,request,handle,ring,*args):
        '''
        Edits the Blueprint
        '''

        blueprint = self.avispamodel.ring_get_blueprint(handle,ring)
        ringblueprint = blueprint['rings'][0]
        fieldsblueprint = blueprint['fields']
        numfields = len(fieldsblueprint)
        # print(blueprint) 

        
        d = {'message': 'Using post_rq_a for handle '+handle , 'template':'avispa_rest/put_rq_a_b.html', 
             'ringblueprint':ringblueprint,
             'fieldsblueprint':fieldsblueprint,
             'numfields':numfields }
        return d

    def put_rs_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using put_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PATCH /a/b
    def patch_a_b(self,request,handle,ring,*args):
    	d = {'message': 'Using patch_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using patch_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using patch_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    #DELETE /a/b
    def delete_a_b(self,request,handle,ring,*args):
    	d = {'message': 'Using delete_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using delete_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using delete_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d
    
    #SEARCH /a/b
    def search_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using search_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/search_a_b.html'}
        return d

    def search_rq_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using search_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/search_rq_a_b.html'}
        return d



    # a/b/c

    #GET /a/b/c
    def get_a_b_c(self,request,handle,ring,idx,*args):
        '''
        Gets existing item
        '''        
        item = self.avispamodel.get_a_b_c(request,handle,ring,idx)

        if item:
            print('Awesome , you just retrieved the item from the DB')
            print(item)
            msg = 'Item retrieved with id: '+idx

        d = {'message': 'Using get_a_b_c for handle '+handle+', ring->'+ring+' idx->'+idx , 'template':'avispa_rest/get_a_b_c.html'}
        return d

    	

    def get_rq_a_b_c(self,request,handle,ring,idx,*args): 
        d = {'message': 'Using get_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/get_rq_a_b_c.html'}
        return d

    def get_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using get_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #POST /a/b/c
    def post_a_b_c(self,request,handle,ring,idx,*args):
    	d = {'message': 'Using post_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using post_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using post_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a/b/c
    def put_a_b_c(self,request,handle,ring,idx,*args):
    	d = {'message': 'Using put_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using put_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using put_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a/b/c
    def patch_a_b_c(self,request,handle,ring,idx,*args):
    	d = {'message': 'Using patch_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b_c(self,request,handle,ring,idx,*args):
        '''
        Prepares form to be sent for a patch
        '''
        item = self.avispamodel.get_a_b_c(request,handle,ring,idx)

        blueprint = self.avispamodel.ring_get_blueprint(handle,ring)
        ringblueprint = blueprint['rings'][0]
        fieldsblueprint = blueprint['fields']
        numfields = len(fieldsblueprint)

        d = {'message': 'Using post_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/post_rq_a_b.html', 
             'ringblueprint':ringblueprint,
             'fieldsblueprint':fieldsblueprint,
             'numfields':numfields,
             'item':item.items[0] }

        #rint(item.items[0]['Website'])

        return d

        #d = {'message': 'Using patch_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/patch_rq_a_b_c.html'}
        #return d

    def patch_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using patch_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a/b/c
    def delete_a_b_c(self,request,handle,ring,idx,*args):
    	d = {'message': 'Using delete_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using delete_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using delete_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a/b/c
    def search_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using search_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def search_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using search_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/search_rq_a_b_c.html'}
        return d

