# AvispaCollectionsRestFunc.py
from flask import redirect, flash
from AvispaModel import AvispaModel
from AvispaCollectionsModel import AvispaCollectionsModel
from CollectionBuilder import CollectionBuilder

class AvispaCollectionsRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()
        self.ACM = AvispaCollectionsModel()

    # GET/a
    def get_a(self,request,handle,collection,idx,api=False,*args):

        collectionlist = self.ACM.get_a(handle)
        print('collectionlist:',collectionlist)
        collectionlistlen = len(collectionlist)

        d = {'template':'avispa_rest/get_a_collections.html', 'collectionlist':collectionlist, 'collectionlistlen':collectionlistlen}
        return d

        d = {'message': 'Using Collection get_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_rq_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection get_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_rs_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_q_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection get_q_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    # POST/a
    def post_a(self,request,handle,collection,idx,api=False,*args):

        #Build the actual collection
        CB = CollectionBuilder()
        result = CB.post_a(request,handle)
            
        if result:
            print('Awesome , you just created a new Collection')
            #msg = 'Item put with id: '+idx
            flash("Your new Collection has been created")
            redirect = '/'+handle+'/_collections'
            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error creating the Collection' , 'template':'avispa_rest/index.html'}
        
        return d


    def post_rq_a(self,request,handle,collection,idx,api=False,*args):

        ringlist = self.AVM.user_get_rings(handle)


        d = {'message': 'Using Collection post_rq_a for handle '+handle , 
             'template':'avispa_rest/post_rq_a_collections.html',
             'ringlist':ringlist}
        return d

    def post_rs_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection post_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a
    def put_a(self,request,handle,collection,idx,api=False,*args):
    	d = {'message': 'Using Collection put_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection put_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection put_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a
    def patch_a(self,request,handle,collection,idx,api=False,*args):
    	d = {'message': 'Using Collection patch_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection patch_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection patch_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a
    def delete_a(self,request,handle,collection,idx,api=False,*args):
    	d = {'message': 'Using Collection delete_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection delete_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d
    
    def delete_rs_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection delete_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a
    def search_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection search_a for handle '+handle , 'template':'avispa_rest/search_a.html'}
        return d

    def search_rq_a(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection search_rq_a for handle '+handle , 'template':'avispa_rest/search_rq_a.html'}
        return d

    # /a/b
    
    #GET /a/b
    def get_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection get_a_b for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_rq_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection get_rq_a_b for handle:'+handle+', collection:'+collection , 'template':'avispa_rest/get_rq_a_b.html'}
        return d

    def get_rs_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection get_rs_a_b for handle:'+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d


    #POST /a/b
    def post_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection post_a_b for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection post_rq_a_b for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def post_rs_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection post_rs_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_b(self,request,handle,collection,idx,api=False,*args):
        # Introduce de changes to the existing collection


        CB = CollectionBuilder()
        result = CB.put_a_b(request,handle,collection)

        d = {'message': 'Using Collection put_a_b for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a_b(self,request,handle,collection,idx,api=False,*args):
        #Form to edit a collection
        ringlist = self.AVM.user_get_rings(handle)
        collectionlist = self.ACM.get_a_b(handle,collection)

        print('collectionlist:',collectionlist)

        collectionrings = []
        for ring in collectionlist['rings']:
            collectionrings.append(ring['handle']+'_'+ring['ringname']+'_'+ring['version'].replace(',','-'))

        


        d = {'message': 'Using Collection put_rq_a for handle '+handle , 
             'template': 'avispa_rest/put_rq_a_b_collections.html',
             'ringlist': ringlist,
             'collectionlist': collectionlist,
             'collectionrings': collectionrings}
        return d


    def put_rs_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection put_rs_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d


    #PATCH /a/b
    def patch_a_b(self,request,handle,collection,idx,api=False,*args):
    	d = {'message': 'Using Collection patch_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection patch_rq_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection patch_rs_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    
    #DELETE /a/b
    def delete_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection delete_a_b for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection delete_rq_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection delete_rs_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d
    
    #SEARCH /a/b
    def search_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection search_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/search_a_b.html'}
        return d

    def search_rq_a_b(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection search_rq_a_b for handle '+handle+', collection:'+collection , 'template':'avispa_rest/search_rq_a_b.html'}
        return d



    # a/b/c

    #GET /a/b/c
    def get_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection get_a_b_c for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_rq_a_b_c(self,request,handle,collection,idx,api=False,*args): 
        d = {'message': 'Using Collection get_rq_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/get_rq_a_b_c.html'}
        return d

    def get_rs_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection get_rs_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #POST /a/b/c
    def post_a_b_c(self,request,handle,collection,idx,api=False,*args):
    	d = {'message': 'Using Collection post_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection post_rq_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rs_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection post_rs_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a/b/c
    def put_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection put_a_b_c for handle '+handle , 'template':'avispa_rest/index.html'}
        return d




    def put_rq_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection put_rq_a_b for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection put_rs_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a/b/c
    def patch_a_b_c(self,request,handle,collection,idx,api=False,*args):
    	d = {'message': 'Using Collection patch_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection patch_rq_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection patch_rs_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a/b/c
    def delete_a_b_c(self,request,handle,collection,idx,api=False,*args):
    	d = {'message': 'Using Collection delete_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection delete_rq_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection delete_rs_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a/b/c
    def search_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection search_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def search_rq_a_b_c(self,request,handle,collection,idx,api=False,*args):
        d = {'message': 'Using Collection search_rq_a_b_c for handle '+handle+', collection->'+collection+'  idx->'+idx , 'template':'avispa_rest/search_rq_a_b_c.html'}
        return d
