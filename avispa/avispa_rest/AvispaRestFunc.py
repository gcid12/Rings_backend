class AvispaRestFunc:
    
    # /a

    def get_a(self,user,*args):
        d = {'message': 'Using get_a for user '+user , 'template':'avispa_rest/index.html'}
    	return d

    def post_a(self,user,*args):
    	d = {'message': 'Using post_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def put_a(self,user,*args):
    	d = {'message': 'Using put_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def patch_a(self,user,*args):
    	d = {'message': 'Using patch_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    def delete_a(self,user,*args):
    	d = {'message': 'Using delete_a for user '+user , 'template':'avispa_rest/index.html'}
        return d

    # /a/b

    def get_a_b(self,user,ring,*args):
    	d = {'message': 'Using get_a_b for user:'+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def post_a_b(self,user,ring,*args):
    	d = {'message': 'Using post_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def put_a_b(self,user,ring,*args):
    	d = {'message': 'Using put_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_a_b(self,user,ring,*args):
    	d = {'message': 'Using patch_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def delete_a_b(self,user,ring,*args):
    	d = {'message': 'Using delete_a_b for user '+user+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    # a/b/c

    def get_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using get_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using post_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def put_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using put_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using patch_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_a_b_c(self,user,ring,idx,*args):
    	d = {'message': 'Using delete_a_b_c for user '+user+', ring:'+ring+', idx:'+idx , 'template':'avispa_rest/index.html'}
        return d

