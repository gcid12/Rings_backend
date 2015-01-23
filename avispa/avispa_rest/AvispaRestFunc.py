import json, collections
from flask import redirect, flash
from RingBuilder import RingBuilder
from AvispaModel import AvispaModel
from AvispaCollectionsModel import AvispaCollectionsModel
from env_config import PREVIEW_LAYER
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

class AvispaRestFunc:

    def __init__(self):
        self.AVM = AvispaModel() 

        

    # /a

    # GET/a
    def get_a(self,request,handle,ring,idx,api=False,*args):

        ringlist = self.AVM.user_get_rings(handle)
        #print('ringlist:',ringlist)

        collectionname = ''
        if 'collection' in request.args:
            self.ACM = AvispaCollectionsModel()
            collectiond = self.ACM.get_a_x_y(handle,request.args.get('collection')) #It comes with just one collection             
            if collectiond:
                if 'valid' in collectiond:
                    collectionname = collectiond['collectionname']                 
                    ringd = {}
                    for rc in collectiond['rings']:
                        #Building dictionary of collection rings
                        ringd[rc['handle']+'_'+rc['ringname']+'_'+rc['version'].replace('.','-')] = rc
                    ringlistmod = []
                    for ring in ringlist:
                        print('trying to match:', handle+'_'+ring['ringname']+'_'+ring['ringversion'])
                        if handle+'_'+ring['ringname']+'_'+ring['ringversion'] in ringd:
                            # A match! One of the collection's ring. Add it to the list
                            ringlistmod.append(ring) 
                    del ringlist
                    ringlist = ringlistmod
                    invalid_collection = False
                else:
                    invalid_collection = True
            else:
                invalid_collection = True            
            if invalid_collection:
                redirect = '/'+handle+'/_home'                
                d = {'redirect': redirect, 'status':404}
                return d

        ringlistlen = len(ringlist)

        
        d = {'message': 'Using get_a for handle '+handle , 'template':'avispa_rest/get_a.html', 'ringlist':ringlist, 'ringlistlen':ringlistlen, 'collection':collectionname }
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
            print('Awesome , you just created a new Ring Schema')
            #msg = 'Item put with id: '+idx
            flash("Your new Schema has been created")
            redirect = '/'+handle
            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error creating the Schema' , 'template':'avispa_rest/index.html'}
        
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

        collectionname = ''
        if 'collection' in request.args:
            self.ACM = AvispaCollectionsModel()
            collectiond = self.ACM.get_a_x_y(handle,request.args.get('collection')) #It comes with just one collection
            if collectiond:
                collectionname = collectiond['collectionname'] 
            else:
                redirect = '/'+handle+'/_home'
                d = {'redirect': redirect, 'status':404}
                return d


        d['collection'] = collectionname


        if request.args.get('lastkey'):
            lastkey = request.args.get('lastkey')
        else:
            lastkey = None

        if request.args.get('resultsperpage'):
            resultsperpage = int(request.args.get('resultsperpage'))
        else:
            resultsperpage = 1000

        if request.args.get('sort'):
            sort = request.args.get('sort')
        else:
            sort = None

        if request.args.get('noimages'):
            noimages = request.args.get('noimages')
        else:
            noimages = None

        if request.args.get('layer'):
            layer = request.args.get('layer')
        else:
            layer = PREVIEW_LAYER

        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        #print(schema['fields'])

        layers = {}
        labels = {}
        widgets = {}
        for schemafield in schema['fields']:
            layers[schemafield['FieldName']]=int(schemafield['FieldLayer'])
            labels[schemafield['FieldName']]=schemafield['FieldLabel']
            widgets[schemafield['FieldName']]=schemafield['FieldWidget']

        print('widgets:',widgets)

        
        ringparameters = self.AVM.get_a_b_parameters(handle,ring)
        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin']




        preitemlist = self.AVM.get_a_b(handle,ring,resultsperpage,lastkey,sort)
        
        
        #print('preitemlist:')
        print('preitemlist:',preitemlist)

        itemlist = []
        d['imagesui'] = False
        for item in preitemlist:
            #item['_level']=2
            print('item:',item)
            #previewItem = {}
            previewItem = collections.OrderedDict()  

            for fieldname in item:
                print('fieldname:',fieldname)
                
                previewItem[u'_id'] = item[u'_id']
                if fieldname in layers:
                    if layers[fieldname]<=layer:
                    #if True:
                        #Only include those fields above the PREVIEWLAYER
                        print("Layer for "+fieldname+'->'+str(layers[fieldname]))
                        previewItem[fieldname] = item[fieldname] 
                    #Include id anyway     

                        if  widgets[fieldname]=='images':
                            
                            d['imagesui'] = True
                            images=previewItem[fieldname].split(',')                
                            del images[0]
                            previewItem[fieldname]=images

            #print('previewItem:')
            #print(previewItem)

            itemlist.append(previewItem)

        if noimages:
            d['imagesui'] = False


        #print('itemlist:')
        #print(itemlist)

        #print(len(itemlist))

        if len(itemlist)>0 and len(itemlist) == resultsperpage:
            nextlastkey=itemlist[-1]['_id']
            d['lastkey'] = nextlastkey
            #Still, if the last page has exactly as many items as resultsperpage, the next page will be empty. Please fix

        d['widget'] = widgets
        d['itemlist'] = itemlist
        d['resultsperpage'] = resultsperpage
        d['FieldLabel'] = labels


        


        if api:

            out = {}

            out['source'] = "/"+str(handle)+"/"+str(ring)

            if 'schema' in request.args:
                out['rings'] = schema['rings']
                out['fields'] = schema['fields']
            
            out['items'] = itemlist
            
            
            d['api_out'] = json.dumps(out)
            d['template'] = 'avispa_rest/get_api_a_b.html'
        else:
      

            d['rings'] = schema['rings']
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

        
        if request.form.get('saveandnew'):
            redirect = '/'+handle+'/'+ring+'?rq=post'
        else:
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
        schema = self.AVM.ring_get_schema(handle,ring)
        ringschema = schema['rings'][0]
        fieldsschema = schema['fields']
        numfields = len(fieldsschema)

        d = {'message': 'Using post_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/post_rq_a_b.html', 
             'ringschema':ringschema,
             'fieldsschema':fieldsschema,
             'numfields':numfields,
             'item':{} }

        
        ringparameters = self.AVM.get_a_b_parameters(handle,ring)
        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin']


        return d

    def post_rs_a_b(self,request,handle,ring,idx,api=False,*args):
        d = {'message': 'Using post_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_b(self,request,handle,ring,idx,api=False,*args):


        print('Changing origin?')
        print(request.form.get('ringorigin'))
        if request.form.get('ringorigin'):
            print('Changing origin!')
            originresult = self.AVM.set_ring_origin(handle,ring,request.form.get('ringorigin'))

        RB = RingBuilder()
        result =  RB.put_a_b(request,handle,ring)

        if result:
            print('Awesome , you just put the changes in the Ring Schema')
            #msg = 'Item put with id: '+idx
            flash("Changes saved in the Schema")
            redirect = '/'+handle+'/'+ring
            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error updating the Schema' , 'template':'avispa_rest/index.html'}
        
        return d


    def put_rq_a_b(self,request,handle,ring,idx,api=False,*args):
        '''
        Edits the Schema
        '''

        schema = self.AVM.ring_get_schema(handle,ring)
        ringschema = schema['rings'][0]
        fieldsschema = schema['fields']
        numfields = len(fieldsschema)
        # print(schema) 

        
        d = {'message': 'Using post_rq_a for handle '+handle , 'template':'avispa_rest/put_rq_a_b.html', 
             'ringschema':ringschema,
             'fieldsschema':fieldsschema,
             'numfields':numfields }
        
        ringparameters = self.AVM.get_a_b_parameters(handle,ring)
        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin']

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
        
        if self.AVM.user_delete_ring(handle,ring):
            flash('Ring '+ring+' deleted')
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
        
        ringparameters = self.AVM.get_a_b_parameters(handle,ring)
        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin']

        item = self.AVM.get_a_b_c(request,handle,ring,idx)
        print('preitem:',item)

        schema = self.AVM.ring_get_schema(handle,ring)
        print('schema:',schema)

        d['widget'] = {}

        
        for field in schema['fields']:
            

            d['widget'][field['FieldName']] = field['FieldWidget']
            

            if 'images' in field['FieldWidget']:
                images=item[field['FieldName']].split(',')
                print('contents:',item[field['FieldName']])
                print('fieldname:',field['FieldName'])
                print('images:',images)
                del images[0]
                item[field['FieldName']] = images

        print('postitem:',item)



        
        
        
        if item:
            print('Awesome , you just retrieved the item from the DB')
            print(item)

            if api:
                #out = {}
                out = collections.OrderedDict()

                out['source'] = "/"+str(handle)+"/"+str(ring)
                
                if 'schema' in request.args:
                    schema= self.AVM.ring_get_schema_from_view(handle,ring)
                    print('schema::')
                    print(schema)
                    out['rings'] = schema['rings']
                    out['fields'] = schema['fields']
                
                #del item['_id']
                #del item['_public'] 
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
        
        schema = self.AVM.ring_get_schema(handle,ring)
  
        labels = {}
        for schemafield in schema['fields']:
            labels[schemafield['FieldName']]=schemafield['FieldLabel']

        ringschema = schema['rings'][0]
        fieldsschema = schema['fields']
        numfields = len(fieldsschema)

        d = {'message': 'Using put_rq_a_b_c for handle '+handle+', ring:'+ring , 
             'template':'avispa_rest/put_rq_a_b_c.html', 
             'ringschema':ringschema,
             'fieldsschema':fieldsschema,
             'numfields':numfields,
             'item':item,
             'labels':labels }


        ringparameters = self.AVM.get_a_b_parameters(handle,ring)
        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin'] 

        

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

