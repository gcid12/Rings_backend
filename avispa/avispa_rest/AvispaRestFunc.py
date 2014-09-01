class AvispaRestFunc:
    
    # /a

    # GET/a
    def get_a(self,user,*args):
        """
        This function shows the rings from source 'a'
        @use: To see all rings used by source 'a'
        """
        d = {'message': 'Using get_a for user '+user , 'template':'avispa_rest/get_a.html'}
    	return d

    def rq_get_a(self,user,*args):
        """
        This function shows how to formulate a get request with or without filters. 
        @use: To filter rings used by source 'a' (Its default is no filter which is the same a get_a)
        """
        d = {'message': 'Using rq_get_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def rs_get_a(self,user,*args):
        """
        This function shows how the response from a get request will look like
        """
        d = {'message': 'Using rs_get_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    # POST/a
    def post_a(self,user,*args):
    	d = {'message': 'Using post_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def rq_post_a(self,user,*args):
        d = {'message': 'Using rq_post_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def rs_post_a(self,user,*args):
        d = {'message': 'Using rs_post_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a
    def put_a(self,user,*args):
    	d = {'message': 'Using put_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def rq_put_a(self,user,*args):
        d = {'message': 'Using rq_put_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def rs_put_a(self,user,*args):
        d = {'message': 'Using rs_put_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a
    def patch_a(self,user,*args):
    	d = {'message': 'Using patch_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def rq_patch_a(self,user,*args):
        d = {'message': 'Using rq_patch_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def rs_patch_a(self,user,*args):
        d = {'message': 'Using rs_patch_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a
    def delete_a(self,user,*args):
    	d = {'message': 'Using delete_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def rq_delete_a(self,user,*args):
        d = {'message': 'Using rq_delete_a for user '+user , 'template':'avispa_rest/index.html'}
        return d
    
    def rs_delete_a(self,user,*args):
        d = {'message': 'Using rs_delete_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    # /a/b
    
    #GET /a/b
    def get_a_b(self,user,ring,*args):
    	d = {'message': 'Using get_a_b for user:'+user+', ring:'+ring , 'template':'avispa_rest/get_a_b.html'}
        return d

    def rq_get_a_b(self,user,ring,*args):
        d = {'message': 'Using rq_get_a_b for user:'+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rs_get_a_b(self,user,ring,*args):
        d = {'message': 'Using rs_get_a_b for user:'+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #POST /a/b
    def post_a_b(self,user,ring,*args):
    	d = {'message': 'Using post_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rq_post_a_b(self,user,ring,*args):
        d = {'message': 'Using rq_post_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rs_post_a_b(self,user,ring,*args):
        d = {'message': 'Using rs_post_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_b(self,user,ring,*args):
    	d = {'message': 'Using put_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rq_put_a_b(self,user,ring,*args):
        d = {'message': 'Using rq_put_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rs_put_a_b(self,user,ring,*args):
        d = {'message': 'Using rs_put_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PATCH /a/b
    def patch_a_b(self,user,ring,*args):
    	d = {'message': 'Using patch_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rq_patch_a_b(self,user,ring,*args):
        d = {'message': 'Using rq_patch_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rs_patch_a_b(self,user,ring,*args):
        d = {'message': 'Using rs_patch_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    #DELETE /a/b
    def delete_a_b(self,user,ring,*args):
    	d = {'message': 'Using delete_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rq_delete_a_b(self,user,ring,*args):
        d = {'message': 'Using rq_delete_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def rs_delete_a_b(self,user,ring,*args):
        d = {'message': 'Using rs_delete_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    # a/b/c

    #GET /a/b/c
    def get_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using get_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rq_get_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rq_get_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rs_get_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rs_get_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #POST /a/b/c
    def post_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using post_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rq_post_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rq_post_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rs_post_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rs_post_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a/b/c
    def put_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using put_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rq_put_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rq_put_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rs_put_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rs_put_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a/b/c
    def patch_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using patch_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rq_patch_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rq_patch_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rs_patch_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rs_patch_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a/b/c
    def delete_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using delete_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rq_delete_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rq_delete_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def rs_delete_a_b_c(self,user,ring,idx,*args):
        d = {'message': 'Using rs_delete_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

