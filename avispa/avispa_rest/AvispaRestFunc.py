from RingBuilder import RingBuilder
from AvispaModel import AvispaModel

class AvispaRestFunc:

    def __init__(self):
        self.avispamodel = AvispaModel()
    
    # /a

    # GET/a
    def get_a(self,request,handle,*args):

        ringlist = self.avispamodel.get_a(handle)
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
    	d = {'message': 'Using post_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using post_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/post_rq_a_b.html'}
        return d

    def post_rs_a_b(self,request,handle,ring,*args):
        d = {'message': 'Using post_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_b(self,request,handle,ring,*args):
    	d = {'message': 'Using put_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a_b(self,request,handle,ring,*args):

        #HERE TO EDIT RING BLUEPRINT
        d = {'message': 'Using post_rq_a for handle '+handle , 'template':'avispa_rest/put_rq_a_b.html'}
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
    	d = {'message': 'Using get_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/get_a_b_c.html'}
        return d

    def get_rq_a_b_c(self,request,handle,ring,idx,*args): 
        d = {'message': 'Using get_rq_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/get_rq_a_b_c.html'}
        return d

    def get_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using get_rs_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #POST /a/b/c
    def post_a_b_c(self,request,handle,ring,idx,*args):
    	d = {'message': 'Using post_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using post_rq_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using post_rs_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a/b/c
    def put_a_b_c(self,request,handle,ring,idx,*args):
    	d = {'message': 'Using put_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using put_rq_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using put_rs_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a/b/c
    def patch_a_b_c(self,request,handle,ring,idx,*args):
    	d = {'message': 'Using patch_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using patch_rq_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/patch_rq_a_b_c.html'}
        return d

    def patch_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using patch_rs_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a/b/c
    def delete_a_b_c(self,request,handle,ring,idx,*args):
    	d = {'message': 'Using delete_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using delete_rq_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using delete_rs_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a/b/c
    def search_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using search_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def search_rq_a_b_c(self,request,handle,ring,idx,*args):
        d = {'message': 'Using search_rq_a_b_c for handle '+handle+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/search_rq_a_b_c.html'}
        return d

