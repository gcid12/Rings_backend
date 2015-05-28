import json, collections
import urlparse, time, datetime
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
    def get_a(self,request,handle,ring,idx,api=False,collection=None,*args):

        ringlist = self.AVM.user_get_rings(handle)
        #print('ringlist:',ringlist)

        collectionname = ''
        if collection:
            self.ACM = AvispaCollectionsModel()
            collectiond = self.ACM.get_a_x_y(handle,collection) #It comes with just one collection 
            print('collectiond:',collectiond)            
            if collectiond:
                if collectiond['valid']:
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
                flash('Invalid Collection','ER')
                redirect = '/'+handle+'/_home'                
                d = {'redirect': redirect, 'status':404}
                return d

        ringlistlen = len(ringlist)

        
        d = {'message': 'Using get_a for handle '+handle , 'template':'avispa_rest/get_a.html', 'ringlist':ringlist, 'ringlistlen':ringlistlen, 'collection':collectionname }
    	return d


    def get_rq_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        # To find someting in all rings
        d = {'message': 'Using get_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_rs_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def get_q_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    # POST/a
    def post_a(self,request,handle,ring,idx,api=False,collection=None,*args):

       
        RB = RingBuilder()
        result = RB.JSONRingGenerator(request,handle)
        out = {} 
            
        if result:
            print('Awesome , you just created a new Ring Schema',result)
            #msg = 'Item put with id: '+idx
            flash(" Your new Ring has been created. ",'UI')
            if collection:

                # Add this new ring to the collection ring list
                self.ACM = AvispaCollectionsModel()

                try:
                    if self.ACM.add_ring_to_collection(handle, collection,result):
                        flash(" The ring has been added to the collection.",'UI')
                        if not api:
                            redirect = '/'+handle+'/_collections/'+collection
                        else:
                            out['Success'] = True
                            out['Message'] = 'The ring has been added to the collection'
                            status = 200
                            

                except:
                    if not api:
                        redirect = '/'+result['handle']+'/'+result['ringname']+'?method=delete'
                    else:
                        out['Success'] = False
                        out['Message'] = 'The ring could not be added to the collection'
                        status = 500
             
            else: 
                if not api:
                    redirect = '/'+handle
                else:
                    out['Success'] = True
                    out['Message'] = 'The ring has been added'
                    status = 200
            
        else:

            if not api:

                flash(" There has been an issue, please check your parameters and try again. ",'UI')
                param_list = []
                for p in request.form:
                    q =  p+'='+request.form.get(p)
                    param_list.append(q)

                lpl = str(len(param_list))
                recovery_string = '&'.join(param_list)

                if collection:
                    redirect = '/'+handle+'/_collections/'+collection+'?rq=post&n=10&'+str(recovery_string)
                else:
                    redirect = '/'+handle+'/'+collection+'?rq=post&n=10&'+str(recovery_string)

            else:
                out['Success'] = False
                out['Message'] = 'There has been an issue, please check your parameters and try again'
                status = 400

            
        if not api:
            d = {'redirect': redirect, 'status':200}
        else:
            d = {'template':'/base_json.html','api_out':json.dumps(out) ,'status':status}

        return d

    def post_rq_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using post_rq_a for handle '+handle , 'template':'avispa_rest/post_rq_a.html'}
        return d

    def post_rs_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using post_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a
    def put_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using put_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rq_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using put_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def put_rs_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using put_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a
    def patch_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a
    def delete_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using delete_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using delete_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d
    
    def delete_rs_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using delete_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a
    def search_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using search_a for handle '+handle , 'template':'avispa_rest/search_a.html'}
        return d

    def search_rq_a(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using search_rq_a for handle '+handle , 'template':'avispa_rest/search_rq_a.html'}
        return d

    # /a/b
    
    #GET /a/b
    def get_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
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
            resultsperpage = 2000

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

        #print('LAYER:',layer)

        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        #print(schema['fields'])
       
        d['ringdescription'] = schema['rings'][0]['RingDescription']

        layers = {}
        labels = {}
        widgets = {}
        sources = {}
        for schemafield in schema['fields']:
            layers[schemafield['FieldName']]=int(schemafield['FieldLayer'])           
            widgets[schemafield['FieldName']]=schemafield['FieldWidget']
            sources[schemafield['FieldName']]=schemafield['FieldSource']

            if int(schemafield['FieldLayer']) <= int(layer):
                labels[schemafield['FieldName']]=schemafield['FieldLabel']


        print('widgets:',widgets)

        
        ringparameters = self.AVM.get_a_b_parameters(handle,ring)

        if not ringparameters:
            flash(str(ring)+" does not exist or it has been deleted",'UI')
            redirect = '/'+handle+'/_home'
            d = {'redirect': redirect, 'status':404}
            return d
            


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
            previewItem[u'_id'] = item[u'_id']
            previewItem['_fieldcount'] = 0
            previewItem['_fullcount'] = 0

            #print('LAYERS',layers)

            for fieldname in item:
                #print ('FIELDNAME',fieldname)
                
                if fieldname in layers:
                    previewItem['_fieldcount'] += 1

                    
                    if item[fieldname] != '':
                        previewItem['_fullcount'] += 1

                    if int(layers[fieldname])<=int(layer):

                        #print('int('+str(layers[fieldname])+')<=int('+str(layer)+'))')
                    #if True:
                        #Only include those fields below the PREVIEWLAYER
                        #print("Including in the preview:"+fieldname+'. Layer:'+str(layers[fieldname]))
                        previewItem[fieldname] = item[fieldname] 

                        if fieldname+'_rich' in item and (sources[fieldname] is not None):

                            previewItem[fieldname+'_rich'] = item[fieldname+'_rich']

                            # Retrieve all the fl from the fieldsources for this specific field
                            field_sources = {}
                            list_sources = sources[fieldname].split(',')
                            for source in list_sources:
                                print('source:',source.strip())
                                if source == '':
                                    continue
                                o = urlparse.urlparse(source.strip())
                                #source_uri= urlparse.urlunparse((o1.scheme, o1.netloc, o1.path,'', '', ''))
                                
                                print('o.netloc:',o.netloc)
                                print('o.path:',o.path)

                                path_parts = o.path.split('/')
                                if path_parts[1] == '_api':
                                    del path_parts[1]
                                    path = '/'.join(path_parts)
                                else:
                                    path = o.path   
                                    print('corrected xo.path:',path)

                                source_id= urlparse.urlunparse((o.scheme, o.netloc, path,'', '', ''))


                                print('o.query:',o.query)
                                queryparts = o.query.split('&')
                                for querypart in queryparts:
                                    qp = querypart.split('=')
                                    if 'fl' in qp:
                                        qp_parts = qp[1].split('+')
                                        field_sources[source_id] = qp_parts

                            print ('field_sources:',field_sources)

                            # Create _repr based on field_sources
                            for rich_item in item[fieldname+'_rich']:
                                if '_source' in rich_item:
                                    o = urlparse.urlparse(rich_item['_source'].strip())
                                    print('xo.netloc:',o.netloc)
                                    print('xo.path:',o.path)

                                    path_parts = o.path.split('/')
                                    if path_parts[1] == '_api':
                                        del path_parts[1]
                                        
                                    del path_parts[-1]
                                    path = '/'.join(path_parts)  
                                    
                                    print('adjusted xo.path:',path)
                                    
                                    source_id= urlparse.urlunparse((o.scheme, o.netloc, path,'', '', ''))
                                    print('source_id',source_id)
                                    if source_id in field_sources:
                                        #There is a way to translate

                                        #We are going to overwrite the URLs for the REPRESENTATION
                                        previewItem[fieldname] = ''
                                        for fl in field_sources[source_id]:
                                            if fl in rich_item:
                                                previewItem[fieldname] += rich_item[fl]+' '
                                            else:
                                                print('Not found: Fl is case sensitive')

                                        print('REPR:', previewItem[fieldname])
 
                       

                        if  widgets[fieldname]=='images':
                            
                            d['imagesui'] = True
                            images=previewItem[fieldname].split(',')                
                            del images[0]
                            previewItem[fieldname]=images

            print('PREVIEW ITEM:')
            print(previewItem)

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

            o = urlparse.urlparse(request.url)
            host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

            out['source'] = host_url+"/"+str(handle)+"/"+str(ring)

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

    def get_rq_a_b(self,request,handle,ring,idx=False,api=False,collection=None,*args):
        # To find something inside of this ring
        d = {'message': 'Using get_rq_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/get_rq_a_b.html'}
        return d

    def get_rs_a_b(self,request,handle,ring,idx=False,api=False,collection=None,*args):
        d = {'message': 'Using get_rs_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #POST /a/b
    def post_a_b(self,request,handle,ring,idx=False,api=False,collection=None,*args):
        '''
        Creates new item
        '''

        idx = self.AVM.post_a_b(request,handle,ring)
        out = {}

        if idx:

            if not api:
                print('Awesome , you just saved the item to the DB')
                print('Item saved with id: '+idx)
                flash("The new item has been created",'UI')
            else:
                out['Success'] = True
                out['Message'] = 'Item saved'
                out['item'] = str(handle+'/'+ring+'/'+idx)
                status = 200

        else:

            if not api:
                print('There was an error creating the item')
                print('Item saved with id: '+idx)           
                flash("There was an error creating the item",'ER')
            else:
                out['Success'] = False
                out['Message'] = 'Item could not be saved'
                status = 400


        if not api:

            if collection:
                if request.form.get('saveandnew'):
                    redirect = '/'+handle+'/_collections/'+collection+'/'+ring+'?rq=post'
                else:
                    redirect = '/'+handle+'/_collections/'+collection+'/'+ring
            else:
                if request.form.get('saveandnew'):
                    redirect = '/'+handle+'/'+ring+'?rq=post'
                else:
                    redirect = '/'+handle+'/'+ring

            if 'raw' in request.args:          
                #o = urlparse.urlparse(request.url)
                #host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
                m = {}
                m['uri'] = handle+'/'+ring+'/'+idx
                m['ui_action'] = 'post'
                message = json.dumps(m)
                d = {'message':message,'template':'avispa_rest/post_a_b_raw.html'}
            else:      
                d = {'redirect': redirect, 'status':201}

        else:
            d = {'template':'/base_json.html','api_out':json.dumps(out) ,'status':status}

        return d

        #return redirect('/'+handle+'/'+ring)

    def post_rq_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        '''
        Form to create new item
        '''
        #print(ring)
        schema = self.AVM.ring_get_schema(handle,ring)

        d = {}
        d['ringdescription'] = schema['rings'][0]['RingDescription']

        ringschema = schema['rings'][0]
        fieldsschema = schema['fields']
        numfields = len(fieldsschema)

        #Make FieldSource canonical
        for field in schema['fields']:
            if 'FieldSource' in field:
                if field['FieldSource']:
                    sources = field['FieldSource'].split(',')
                    canonical_uri_list = []
                    
                    for source in sources:
                        o = urlparse.urlparse(source.strip())
                        canonical_uri= urlparse.urlunparse((o.scheme, o.netloc, o.path,'', '', ''))
                        canonical_uri_list.append(canonical_uri)
                
                    field['FieldSource'] = ','.join(canonical_uri_list)


        d['message'] = 'Using post_rq_a_b for handle '+handle+', ring:'+ring 
        d['template'] = 'avispa_rest/post_rq_a_b.html' 
        d['ringschema'] = ringschema
        d['fieldsschema'] = fieldsschema
        d['numfields'] = numfields
        d['item'] = {}

        
        ringparameters = self.AVM.get_a_b_parameters(handle,ring)

        if not ringparameters:
            flash(str(ring)+" does not exist or it has been deleted",'UI')
            redirect = '/'+handle+'/_home'
            d = {'redirect': redirect, 'status':404}
            return d

        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin']


        return d

    def post_rs_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using post_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    def put_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):


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
            flash("Changes saved in the Schema",'UI')
            if collection:
                redirect = '/'+handle+'/_collections/'+collection+'/'+ring           
            else:
                redirect = '/'+handle+'/'+ring
                

            d = {'redirect': redirect, 'status':200}

        else:
            d = {'message': 'There was an error updating the Schema' , 'template':'avispa_rest/index.html'}
        
        return d


    def put_rq_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
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

        if not ringparameters:
            flash(str(ring)+" does not exist or it has been deleted",'UI')
            redirect = '/'+handle+'/_home'
            d = {'redirect': redirect, 'status':404}
            return d

        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin']

        return d

    def put_rs_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using put_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PATCH /a/b
    def patch_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    #DELETE /a/b
    def delete_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        
        if self.AVM.user_delete_ring(handle,ring):
            flash('Ring '+ring+' deleted','UI')
        else:
            flash('Could not delete the Ring','ER')
        
        if collection:
            redirect = '/'+handle+'/_collections/'+collection       
        else:
            redirect = '/'+handle
            

        d = {'redirect': redirect, 'status':200}
        d = {'message': 'Using delete_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def delete_rq_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using delete_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using delete_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d
    
    #SEARCH /a/b
    def search_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using search_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/search_a_b.html'}
        return d

    def search_rq_a_b(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using search_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/search_rq_a_b.html'}
        return d



    # a/b/c

    #GET /a/b/c
    def get_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        '''
        Gets existing item
        ''' 

        d = {}
        
        ringparameters = self.AVM.get_a_b_parameters(handle,ring)

        if not ringparameters:
            flash(str(ring)+" does not exist or it has been deleted",'UI')
            redirect = '/'+handle+'/_home'
            d = {'redirect': redirect, 'status':404}
            return d

        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin']

        item = self.AVM.get_a_b_c(request,handle,ring,idx)
        print('preitem:',item)

        schema = self.AVM.ring_get_schema(handle,ring)
        print('schema:',schema)

        d['ringdescription'] = schema['rings'][0]['RingDescription']


        d['widget'] = {}
        d['imagesui'] = False



        labels = {}

        for field in schema['fields']:

            if field['FieldLabel'] is not '':
                labels[field['FieldName']]=field['FieldLabel']
            else:
                labels[field['FieldName']]=field['FieldName']

            d['widget'][field['FieldName']] = field['FieldWidget']
            

            if 'images' in field['FieldWidget']:
                images=item[field['FieldName']].split(',')
                print('contents:',item[field['FieldName']])
                print('fieldname:',field['FieldName'])
                print('images:',images)
                del images[0]
                item[field['FieldName']] = images
                d['imagesui'] = True

        print('postitem:',item)
                
        if item:
            print('Awesome , you just retrieved the item from the DB')
            print(item)

            if api:
                
                out = collections.OrderedDict()

                out['source'] = "/"+str(handle)+"/"+str(ring)
                
                if 'schema' in request.args:
                    #schema= self.AVM.ring_get_schema_from_view(handle,ring)
                    #print('schema:',schema)
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
                d['labels'] = labels 
                d['template'] = 'avispa_rest/get_a_b_c.html'

        else: 
            d['status'] = '500'                      
            flash('This item does not exist','ER')
            print('This item does not exist')


        return d

        

    def get_rq_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args): 
        d = {'message': 'Using get_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/get_rq_a_b_c.html'}
        return d

    def get_rs_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using get_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #POST /a/b/c
    def post_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using post_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rq_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using post_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def post_rs_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using post_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a/b/c
    def put_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        '''
        Puts changes in the item
        '''        
        result = self.AVM.put_a_b_c(request,handle,ring,idx)

        if result:
            print('Awesome , you just put the changes in the Item')
            #msg = 'Item put with id: '+idx
            flash("Changes saved",'UI')
            if collection:
                redirect = '/'+handle+'/_collections/'+collection+'/'+ring     
            else:
                redirect = '/'+handle+'/'+ring

            if 'raw' in request.args:          
                #o = urlparse.urlparse(request.url)
                #host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
                m = {}
                m['uri'] = handle+'/'+ring+'/'+idx
                m['ui_action'] = 'put'
                message = json.dumps(m)
                d = {'message':message,'template':'avispa_rest/put_a_b_c_raw.html'}
            else:      
                d = {'redirect': redirect, 'status':201}

        else:
            d = {'message': 'There was an error updating this item' , 'template':'avispa_rest/index.html'}
        
        return d




    def put_rq_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        '''
        Repopulates form to be sent for a put
        '''
        item = self.AVM.get_a_b_c(request,handle,ring,idx)

        print('ITEM',item)
       
        #if item['Images']:
         #   images=item['Images'].split(',')
          #  item['Images']=images
        
        schema = self.AVM.ring_get_schema(handle,ring)

        d = {}

        d['ringdescription'] = schema['rings'][0]['RingDescription']
  
        labels = {}
        for schemafield in schema['fields']:
            labels[schemafield['FieldName']]=schemafield['FieldLabel']

        ringschema = schema['rings'][0]
        fieldsschema = schema['fields']
        numfields = len(fieldsschema)

        #Make FieldSource canonical
        for field in schema['fields']:
            if 'FieldSource' in field:
                if field['FieldSource']:
                    sources = field['FieldSource'].split(',')
                    canonical_uri_list = []
                    
                    for source in sources:
                        o = urlparse.urlparse(source.strip())
                        canonical_uri= urlparse.urlunparse((o.scheme, o.netloc, o.path,'', '', ''))
                        canonical_uri_list.append(canonical_uri)
                
                    field['FieldSource'] = ','.join(canonical_uri_list)

        
        d['message'] = 'Using put_rq_a_b_c for handle '+handle+' ring:'+ring  
        d['template'] = 'avispa_rest/put_rq_a_b_c.html' 
        d['ringschema'] = ringschema
        d['fieldsschema'] = fieldsschema
        d['numfields'] = numfields
        d['item'] = item
        d['labels'] = labels 


        ringparameters = self.AVM.get_a_b_parameters(handle,ring)

        if not ringparameters:
            flash(str(ring)+" does not exist or it has been deleted",'UI')
            redirect = '/'+handle+'/_home'
            d = {'redirect': redirect, 'status':404}
            return d

        d['ringcount']  = ringparameters['count']
        d['ringorigin'] = ringparameters['ringorigin'] 

        

        #rint(item.items[0]['Website'])

        return d

        #d = {'message': 'Using patch_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/patch_rq_a_b_c.html'}
        #return d

    def put_rs_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using put_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a/b/c
    def patch_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rq_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def patch_rs_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using patch_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a/b/c
    def delete_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        result = self.AVM.delete_a_b_c(request,handle,ring,idx)

        if result:
            print('Item deleted..')
            #msg = 'Item put with id: '+idx
            flash('Item deleted..','UI')
            if collection:
                redirect = '/'+handle+'/_collections/'+collection+'/'+ring           
            else:
                redirect = '/'+handle+'/'+ring


            if 'raw' in request.args:          
                #o = urlparse.urlparse(request.url)
                #host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
                m = {}
                m['uri'] = handle+'/'+ring+'/'+idx
                m['ui_action'] = 'delete'
                message = json.dumps(m)
                d = {'message':message,'template':'avispa_rest/delete_a_b_c_raw.html'}
            else:      
                d = {'redirect': redirect, 'status':200}
                

            

        else:
            d = {'message': 'There was an error deleting this item' , 'template':'avispa_rest/index.html'}
        
        return d



        #d = {'message': 'Using delete_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        #return d

    def delete_rq_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using delete_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def delete_rs_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using delete_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a/b/c
    def search_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using search_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    def search_rq_a_b_c(self,request,handle,ring,idx,api=False,collection=None,*args):
        d = {'message': 'Using search_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/search_rq_a_b_c.html'}
        return d

