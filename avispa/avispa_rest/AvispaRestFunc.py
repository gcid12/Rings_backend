from RingBuilder import RingBuilder

class AvispaRestFunc:
    
    # /a

    # GET/a
    def get_a(self,request,user,*args):
        d = {'message': 'Using get_a for user '+user , 'template':'avispa_rest/get_a.html'}
    	return d

    def get_rq_a(self,request,user,*args):
        # To find someting in all rings
        d = {'message': 'Using get_rq_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def get_rs_a(self,request,user,*args):
        d = {'message': 'Using get_rs_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def get_q_a(self,request,user,*args):
        d = {'message': 'Using get_rs_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    # POST/a
    def post_a(self,request,user,*args):

       
        RB = RingBuilder()
        #result = 'request'
        result = RB.JSONRingGenerator(request)

    	d = {'message': 'Using post_a for user '+user+' JSONRing:'+result , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a(self,request,user,*args):
        d = {'message': 'Using post_rq_a for user '+user , 'template':'avispa_rest/post_rq_a.html'}
        return d

    def post_rs_a(self,request,user,*args):
        d = {'message': 'Using post_rs_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a
    def put_a(self,request,user,*args):
    	d = {'message': 'Using put_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a(self,request,user,*args):
        d = {'message': 'Using put_rq_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a(self,request,user,*args):
        d = {'message': 'Using put_rs_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a
    def patch_a(self,request,user,*args):
    	d = {'message': 'Using patch_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a(self,request,user,*args):
        d = {'message': 'Using patch_rq_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a(self,request,user,*args):
        d = {'message': 'Using patch_rs_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a
    def delete_a(self,request,user,*args):
    	d = {'message': 'Using delete_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a(self,request,user,*args):
        d = {'message': 'Using delete_rq_a for user '+user , 'template':'avispa_rest/index.html'}
        return d
    
    def delete_rs_a(self,request,user,*args):
        d = {'message': 'Using delete_rs_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a
    def search_a(self,request,user,*args):
        d = {'message': 'Using search_a for user '+user , 'template':'avispa_rest/search_a.html'}
        return d

    def search_rq_a(self,request,user,*args):
        d = {'message': 'Using search_rq_a for user '+user , 'template':'avispa_rest/search_rq_a.html'}
        return d

    # /a/b
    
    #GET /a/b
    def get_a_b(self,request,user,ring,*args):
    	d = {'message': 'Using get_a_b for user:'+user+', ring:'+ring , 'template':'avispa_rest/get_a_b.html'}
        return d

    def get_rq_a_b(self,request,user,ring,*args):
        # To find something inside of this ring
        d = {'message': 'Using get_rq_a_b for user:'+user+', ring:'+ring , 'template':'avispa_rest/get_rq_a_b.html'}
        return d

    def get_rs_a_b(self,request,user,ring,*args):
        d = {'message': 'Using get_rs_a_b for user:'+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #POST /a/b
    def post_a_b(self,request,user,ring,*args):
    	d = {'message': 'Using post_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b(self,request,user,ring,*args):
        d = {'message': 'Using post_rq_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/post_rq_a_b.html'}
        return d

    def post_rs_a_b(self,request,user,ring,*args):
        d = {'message': 'Using post_rs_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_b(self,request,user,ring,*args):
    	d = {'message': 'Using put_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a_b(self,request,user,ring,*args):
        d = {'message': 'Using put_rq_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a_b(self,request,user,ring,*args):
        d = {'message': 'Using put_rs_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PATCH /a/b
    def patch_a_b(self,request,user,ring,*args):
    	d = {'message': 'Using patch_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b(self,request,user,ring,*args):
        d = {'message': 'Using patch_rq_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_b(self,request,user,ring,*args):
        d = {'message': 'Using patch_rs_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    #DELETE /a/b
    def delete_a_b(self,request,user,ring,*args):
    	d = {'message': 'Using delete_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_b(self,request,user,ring,*args):
        d = {'message': 'Using delete_rq_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b(self,request,user,ring,*args):
        d = {'message': 'Using delete_rs_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d
    
    #SEARCH /a/b
    def search_a_b(self,request,user,ring,*args):
        d = {'message': 'Using search_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/search_a_b.html'}
        return d

    def search_rq_a_b(self,request,user,ring,*args):
        d = {'message': 'Using search_rq_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/search_rq_a_b.html'}
        return d



    # a/b/c

    #GET /a/b/c
    def get_a_b_c(self,request,user,ring,idx,*args):
    	d = {'message': 'Using get_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/get_a_b_c.html'}
        return d

    def get_rq_a_b_c(self,request,user,ring,idx,*args): 
        d = {'message': 'Using get_rq_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/get_rq_a_b_c.html'}
        return d

    def get_rs_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using get_rs_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #POST /a/b/c
    def post_a_b_c(self,request,user,ring,idx,*args):
    	d = {'message': 'Using post_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using post_rq_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rs_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using post_rs_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a/b/c
    def put_a_b_c(self,request,user,ring,idx,*args):
    	d = {'message': 'Using put_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using put_rq_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using put_rs_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a/b/c
    def patch_a_b_c(self,request,user,ring,idx,*args):
    	d = {'message': 'Using patch_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using patch_rq_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/patch_rq_a_b_c.html'}
        return d

    def patch_rs_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using patch_rs_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a/b/c
    def delete_a_b_c(self,request,user,ring,idx,*args):
    	d = {'message': 'Using delete_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using delete_rq_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using delete_rs_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a/b/c
    def search_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using search_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def search_rq_a_b_c(self,request,user,ring,idx,*args):
        d = {'message': 'Using search_rq_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/search_rq_a_b_c.html'}
        return d

