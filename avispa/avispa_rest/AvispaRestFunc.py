import json
from flask import redirect, flash
from RingBuilder import RingBuilder
from MainModel import MainModel #DELETE!
from AvispaModel import AvispaModel
from env_config import PREVIEW_LAYER

class AvispaRestFunc:

    def __init__(self):
        self.AVM = AvispaModel() 
    
    # /a

    # GET/a
    def get_a(self,request,handle,ring,idx,api=False,*args):

        ringlist = self.AVM.user_get_rings(handle)

        ringlistlen = len(ringlist)


        #print(ringlist)
        d = {'message': 'Using get_a for handle '+handle , 'template':'avispa_rest/get_a.html', 'ringlist':ringlist, 'ringlistlen':ringlistlen}
    	return d

    def get_rq_a(self,request,handle,ring,idx,api=False,*args):
        # To find someting in all rings
        d = {'message': 'Using get_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_rs_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_q_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    # POST/a
    def post_a(self,request,handle,ring,idx,api=False,*args):

       
        RB = RingBuilder()
        result = RB.JSONRingGenerator(request,handle)
            
        if result:
            print('Awesome , you just created a new Ring Blueprint')
            #msg = 'Item put with id: '+idx
            flash("Your new Blueprint has been created")
            redirect = '/'+handle
            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error creating the Blueprint' , 'template':'avispa_rest/index.html'}
        
        return d

    def post_rq_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using post_rq_a for handle '+handle , 'template':'avispa_rest/post_rq_a.html'}
        return d

    def post_rs_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using post_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a
    def put_a(self,request,handle,ring,idx,api=False,*args):
    	d = {'message': 'Using put_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using put_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using put_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a
    def patch_a(self,request,handle,ring,idx,api=False,*args):
    	d = {'message': 'Using patch_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using patch_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using patch_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a
    def delete_a(self,request,handle,ring,idx,api=False,*args):
    	d = {'message': 'Using delete_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using delete_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d
    
    def delete_rs_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using delete_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a
    def search_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using search_a for handle '+handle , 'template':'avispa_rest/search_a.html'}
        return d

    def search_rq_a(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using search_rq_a for handle '+handle , 'template':'avispa_rest/search_rq_a.html'}
        return d

    # /a/b
    
    #GET /a/b
    def get_a_b(self,request,handle,ring,idx,api=False,*args):
        '''
        List of items in the ring
        '''
        d = {}

        if request.args.get('lastkey'):
            lastkey = request.args.get('lastkey')
        else:
            lastkey = None

        if request.args.get('resultsperpage'):
            resultsperpage = request.args.get('resultsperpage')
        else:
            resultsperpage = 25

        blueprint = self.AVM.ring_get_blueprint_from_view(handle,ring)
        #print(blueprint['fields'])

        layers = {}
        for blueprintfield in blueprint['fields']:
            layers[blueprintfield['FieldName']]=int(blueprintfield['FieldLayer'])

        #print('layers:')
        #print(layers)


        preitemlist = self.AVM.get_a_b(handle,ring,resultsperpage,lastkey)
        
        #print('preitemlist:')
        #print(preitemlist)

        itemlist = []
        for item in preitemlist:
            #item['_level']=2
            #print(item)
            previewItem = {}
            for fieldname in item:
                #print(fieldname)
                
                if fieldname in layers:
                    if layers[fieldname]<=PREVIEW_LAYER:
                    #if True:
                        #Only include those fields above the PREVIEWLAYER
                        #print("Out:"+fieldname)
                        previewItem[fieldname] = item[fieldname] 
                    #Include id anyway     
                    previewItem[u'_id'] = item[u'_id']


            if 'Images' in previewItem:
                images=previewItem['Images'].split(',')                
                del images[0]
                previewItem['Images']=images
            itemlist.append(previewItem)


        #print('itemlist:')
        #print(itemlist)

        #print(len(itemlist))

        if len(itemlist)>0 and len(itemlist) == resultsperpage:
            nextlastkey=itemlist[-1]['id']
            d['lastkey'] = nextlastkey
            #Still, if the last page has exactly as many items as resultsperpage, the next page will be empty. Please fix

        
        d['itemlist'] = itemlist
        d['resultsperpage'] = resultsperpage

        if api:

            out = {}

            out['source'] = "/"+str(handle)+"/"+str(ring)

            
            if 'blueprint' in request.args:
                blueprint= self.AVM.ring_get_blueprint_from_view(handle,ring)
                out['rings'] = blueprint['rings']
                out['fields'] = blueprint['fields']

            #del itemlist['_id']
            #del item['_public'] 
            
            out['items'] = itemlist
            
            
            d['api_out'] = json.dumps(out)
            d['template'] = 'avispa_rest/get_api_a_b.html'
        else:
            d['template'] = 'avispa_rest/get_a_b.html'

        return d

    def get_rq_a_b(self,request,handle,ring,idx,api=False,*args):
        # To find something inside of this ring
        d = {'message': 'Using get_rq_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/get_rq_a_b.html'}
        return d

    def get_rs_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using get_rs_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #POST /a/b
    def post_a_b(self,request,handle,ring,idx,api=False,*args):
        '''
        Creates new item
        '''        
        idx = self.AVM.post_a_b(request,handle,ring)

        if idx:
            print('Awesome , you just saved the item to the DB')
            msg = 'Item saved with id: '+idx


        redirect = '/'+handle+'/'+ring
        print('Now redirect to:')
        print(redirect)
        flash("The new item has been created")

        d = {'redirect': redirect, 'status':201}
        return d

        #return redirect('/'+handle+'/'+ring)

    def post_rq_a_b(self,request,handle,ring,idx,api=False,*args):
        '''
        Form to create new item
        '''
        #print(ring)
        blueprint = self.AVM.ring_get_blueprint(handle,ring)
        ringblueprint = blueprint['rings'][0]
        fieldsblueprint = blueprint['fields']
        numfields = len(fieldsblueprint)

        d = {'message': 'Using post_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/post_rq_a_b.html', 
             'ringblueprint':ringblueprint,
             'fieldsblueprint':fieldsblueprint,
             'numfields':numfields,
             'item':{} }
        return d

    def post_rs_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using post_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_b(self,request,handle,ring,idx,api=False,*args):

        RB = RingBuilder()
        result =  RB.put_a_b(request,handle,ring)

        if result:
            print('Awesome , you just put the changes in the Ring Blueprint')
            #msg = 'Item put with id: '+idx
            flash("Changes saved in the Blueprint")
            redirect = '/'+handle+'/'+ring
            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error updating the Blueprint' , 'template':'avispa_rest/index.html'}
        
        return d


    def put_rq_a_b(self,request,handle,ring,idx,api=False,*args):
        '''
        Edits the Blueprint
        '''

        blueprint = self.AVM.ring_get_blueprint(handle,ring)
        ringblueprint = blueprint['rings'][0]
        fieldsblueprint = blueprint['fields']
        numfields = len(fieldsblueprint)
        # print(blueprint) 

        
        d = {'message': 'Using post_rq_a for handle '+handle , 'template':'avispa_rest/put_rq_a_b.html', 
             'ringblueprint':ringblueprint,
             'fieldsblueprint':fieldsblueprint,
             'numfields':numfields }
        return d

    def put_rs_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using put_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PATCH /a/b
    def patch_a_b(self,request,handle,ring,idx,api=False,*args):
    	d = {'message': 'Using patch_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using patch_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using patch_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    #DELETE /a/b
    def delete_a_b(self,request,handle,ring,idx,api=False,*args):

        part=ring.split('_')
        ringname = part[0]
        ringversion = part[-1]
        
        if self.AVM.user_delete_ring(handle,ringname,ringversion):
            flash('Ring '+ringname+'_'+ringversion+' deleted')
        else:
            flash('Could not delete the Ring')
        
        redirect = '/'+handle
        d = {'redirect': redirect, 'status':200}
        return d

    def delete_rq_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using delete_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using delete_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d
    
    #SEARCH /a/b
    def search_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using search_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/search_a_b.html'}
        return d

    def search_rq_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using search_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/search_rq_a_b.html'}
        return d



    # a/b/c

    #GET /a/b/c
    def get_a_b_c(self,request,handle,ring,idx,api=False,*args):
        '''
        Gets existing item
        ''' 
        d = {}       
        item = self.AVM.get_a_b_c(request,handle,ring,idx)
        if 'Images' in item:
                images=item['Images'].split(',')
                del images[0]
                item['Images']=images
        
        if item:
            print('Awesome , you just retrieved the item from the DB')
            print(item)

            if api:
                out = {}

                out['source'] = "/"+str(handle)+"/"+str(ring)
                
                if 'blueprint' in request.args:
                    blueprint= self.AVM.ring_get_blueprint_from_view(handle,ring)
                    print('blueprint::')
                    print(blueprint)
                    out['rings'] = blueprint['rings']
                    out['fields'] = blueprint['fields']
                
                #del item['_id']
                del item['_public'] 
                out['items'] = [] 
                out['items'].append(item)
                #out['items'] = item

                api_out = json.dumps(out)

                d['api_out'] = api_out
                d['template'] = 'avispa_rest/get_api_a_b_c.html'

            else:
                d['item'] = item
                d['template'] = 'avispa_rest/get_a_b_c.html'

        else: 
            d['error_status'] = '500'                      
            flash('This item does not exist')
            print('This item does not exist')


        return d

    	

    def get_rq_a_b_c(self,request,handle,ring,idx,api=False,*args): 
        d = {'message': 'Using get_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/get_rq_a_b_c.html'}
        return d

    def get_rs_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using get_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #POST /a/b/c
    def post_a_b_c(self,request,handle,ring,idx,api=False,*args):
    	d = {'message': 'Using post_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using post_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rs_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using post_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a/b/c
    def put_a_b_c(self,request,handle,ring,idx,api=False,*args):
        '''
        Puts changes in the item
        '''        
        result = self.AVM.put_a_b_c(request,handle,ring,idx)

        if result:
            print('Awesome , you just put the changes in the Item')
            #msg = 'Item put with id: '+idx
            flash("Changes saved")
            redirect = '/'+handle+'/'+ring
            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There waas an error updating this item' , 'template':'avispa_rest/index.html'}
        
        return d




    def put_rq_a_b_c(self,request,handle,ring,idx,api=False,*args):
        '''
        Prepares form to be sent for a put
        '''
        item = self.AVM.get_a_b_c(request,handle,ring,idx)
       
        

        #if item['Images']:
         #   images=item['Images'].split(',')
          #  item['Images']=images
           

        
        blueprint = self.AVM.ring_get_blueprint(handle,ring)
        ringblueprint = blueprint['rings'][0]
        fieldsblueprint = blueprint['fields']
        numfields = len(fieldsblueprint)

        d = {'message': 'Using put_rq_a_b_c for handle '+handle+', ring:'+ring , 
             'template':'avispa_rest/put_rq_a_b_c.html', 
             'ringblueprint':ringblueprint,
             'fieldsblueprint':fieldsblueprint,
             'numfields':numfields,
             'item':item }

        #rint(item.items[0]['Website'])

        return d

        #d = {'message': 'Using patch_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/patch_rq_a_b_c.html'}
        #return d

    def put_rs_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using put_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a/b/c
    def patch_a_b_c(self,request,handle,ring,idx,api=False,*args):
    	d = {'message': 'Using patch_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using patch_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using patch_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a/b/c
    def delete_a_b_c(self,request,handle,ring,idx,api=False,*args):
        result = self.AVM.delete_a_b_c(request,handle,ring,idx)

        if result:
            print('Awesome , you just put the changes in the Item')
            #msg = 'Item put with id: '+idx
            flash("Item deleted")
            redirect = '/'+handle+'/'+ring
            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error deleting this item' , 'template':'avispa_rest/index.html'}
        
        return d



    	#d = {'message': 'Using delete_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        #return d

    def delete_rq_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using delete_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using delete_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a/b/c
    def search_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using search_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def search_rq_a_b_c(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using search_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/search_rq_a_b_c.html'}
        return d

