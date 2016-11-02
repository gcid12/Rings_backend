# AvispaCollectionsRestFunc.py
import json
import logging
from flask import redirect,flash,url_for
from TypesModel import TypesModel
from AvispaCollectionsModel import AvispaCollectionsModel
from CollectionBuilder import CollectionBuilder
from AvispaLogging import AvispaLoggerAdapter
from env_config import URL_SCHEME

class AvispaCollectionsRestFunc:

    def __init__(self,tid=None,ip=None):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})

        self.TYM = TypesModel(tid=tid,ip=ip)
        self.ACM = AvispaCollectionsModel(tid=tid,ip=ip)
        self.CB = CollectionBuilder(tid=tid,ip=ip)

    # GET/a
    def get_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        'Show list of collections'
     
        collectionlist = self.ACM.get_a_x(handle)
        #self.lggr.debug('collectionlist:%s'%collectionlist)

        count = 0
        if collectionlist:          
            for collection in collectionlist:
                if collection['valid']:
                    count = count + 1
            
        else:
            collectionlist = []

        collectionlistlen = count

        d = {'template':'avispa_rest/get_a_x.html', 'collectionlist':collectionlist, 'collectionlistlen':collectionlistlen}
        return d

    def get_rq_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection get_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_rs_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_q_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection get_q_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    # POST/a
    def post_a_x(self,handle,collection,idx,api=False,rqform=None,*args,**kargs):

        #Build the actual collection
        
        result = self.CB.post_a_x(rqform,handle)
            
        if result:
            self.lggr.debug('Awesome , you just created a new Collection')
            #msg = 'Item put with id: '+idx

            if api:
                out = {} 
                out['Success'] = True
                out['Message'] = 'The collection has been created'
                d = {}
                d['api_out'] = json.dumps(out)
                d['template'] = '/base_json.html'
                
            else:
                flash("Your new Collection has been created",'UI')
                #redirect = '/'+handle
                redirect = url_for('avispa_rest.home',
                                     handle=handle,
                                     _external=True,
                                     _scheme=URL_SCHEME) 

                d = {'redirect': redirect, 'status':200}

        else:

            if api:
                out = {} 
                out['Sucess'] = False
                out['Message'] = 'There was an error creating the Collection'
                data = {}
                data['api_out'] = json.dumps(out)
                d['template'] = '/base_json.html'
                

            else:
                flash("There was an error creating the Collection",'UI')

        return d


    def post_rq_a_x(self,handle,collection,idx,api=False,*args,**kargs):

        #Generates de form to create the collection

        ringlist = self.TYM.user_get_rings(handle)


        d = {'message': 'Using Collection post_rq_a_x for handle '+handle , 
             'template':'avispa_rest/post_rq_a_x.html',
             'ringlist':ringlist}
        return d

    def post_rs_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection post_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a
    def put_a_x(self,handle,collection,idx,api=False,*args,**kargs):
    	d = {'message': 'Using Collection put_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection put_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection put_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a
    def patch_a_x(self,handle,collection,idx,api=False,*args,**kargs):
    	d = {'message': 'Using Collection patch_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection patch_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection patch_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a
    def delete_a_x(self,handle,collection,idx,api=False,*args,**kargs):
    	d = {'message': 'Using Collection delete_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection delete_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d
    
    def delete_rs_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection delete_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a
    def search_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection search_a for handle '+handle , 'template':'avispa_rest/search_a.html'}
        return d

    def search_rq_a_x(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection search_rq_a for handle '+handle , 'template':'avispa_rest/search_rq_a.html'}
        return d

    # /a/b
    
    #GET /a/b
    def get_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        #THIS IS NOT USED . SEE AvispaRestFunc.get_a() instead 

        d = {'message': 'Using Collection get_a_x_y for handle '+handle , 'template':'avispa_rest/get_a.html'}
        return d

    def get_rq_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection get_rq_a_x_y for handle:'+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    def get_rs_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection get_rs_a_x_y for handle:'+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d


    #POST /a/b
    def post_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection post_a_x_y for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection post_rq_a_x_y for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def post_rs_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection post_rs_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_x_y(self,handle,collection,idx,api=False,rqform=None,*args,**kargs):
        # Introduce the changes to the existing collection


        CB = CollectionBuilder()
        result = CB.put_a_x_y(rqform,handle,collection)

        if result:
            self.lggr.debug('Awesome , you just updated a Collection')
            #msg = 'Item put with id: '+idx
            flash("Your Collection has been updated",'UI')
            
            redirect = url_for('avispa_rest.collections_route_a_x_y',
                                     handle=handle,
                                     collection=collection,
                                     _external=True,
                                     _scheme=URL_SCHEME) 

            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error updating the collection' , 'template':'avispa_rest/index.html'}
        
        return d

    def put_rq_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        #Form to edit a collection
        ringlist = self.TYM.user_get_rings(handle)
        collectiond = self.ACM.get_a_x_y(handle,collection) #It comes with just one collection

        self.lggr.debug('collectiond:%s'%collectiond)

        collectionrings = []
        for ring in collectiond['rings']:
            collectionrings.append(ring['handle']+'_'+ring['ringname']+'_'+ring['version'].replace('-','.'))

        
        d = {'message': 'Using Collection put_rq_a_x_y for handle '+handle , 
             'template': 'avispa_rest/put_rq_a_x_y.html',
             'ringlist': ringlist,
             'collectionlist': collectiond,
             'collectionrings': collectionrings}

        self.lggr.debug("d:%s"%d)

        return d


    def put_rs_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection put_rs_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d


    #PATCH /a/b
    def patch_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
    	d = {'message': 'Using Collection patch_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection patch_rq_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection patch_rs_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    
    #DELETE /a/b
    def delete_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        #Will delete an existing collection

        result = self.ACM.delete_a_x_y(handle,collection)

        if result:
            self.lggr.debug('Awesome , you just deleted a Collection')
            #msg = 'Item put with id: '+idx
            flash("Your Collection has been deleted",'UI')
            #redirect = '/'+handle
            redirect = url_for('avispa_rest.home',
                                handle=handle,
                                _external=True,
                                _scheme=URL_SCHEME)           

            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error deleting the collection' , 'template':'avispa_rest/index.html'}
        
        return d


    def delete_rq_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection delete_rq_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection delete_rs_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/index.html'}
        return d
    
    #SEARCH /a/b
    def search_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection search_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/search_a_b.html'}
        return d

    def search_rq_a_x_y(self,handle,collection,idx,api=False,*args,**kargs):
        d = {'message': 'Using Collection search_rq_a_x_y for handle '+handle+', collection:'+collection , 'template':'avispa_rest/search_rq_a_b.html'}
        return d



    # a/x/y/b and a/x/y/b/c are served by the regular AvispaRestFunc.py