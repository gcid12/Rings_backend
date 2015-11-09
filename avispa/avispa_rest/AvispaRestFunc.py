import json, collections
import urlparse, time, datetime
from flask import redirect, flash, current_app
from RingBuilder import RingBuilder
from AvispaModel import AvispaModel
from AvispaCollectionsModel import AvispaCollectionsModel
from env_config import PREVIEW_LAYER
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from timethis import timethis

class AvispaRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()

    # /a

    # GET/a
    
    def get_a(self,request,handle,ring,idx,api=False,collection=None,*args):

        ringlist = self.AVM.user_get_rings(handle)
        #current_app.logger.debug('ringlist:'+str(ringlist))

        collectionname = ''
        if collection:
            self.ACM = AvispaCollectionsModel()
            collectiond = self.ACM.get_a_x_y(handle,collection) #It comes with just one collection 
            #current_app.logger.debug('collectiond:'+str(collectiond))           
            if collectiond:
                if collectiond['valid']:
                    collectionname = collectiond['collectionname']                 
                    ringd = {}
                    for rc in collectiond['rings']:
                        #Building dictionary of collection rings
                        ringd[rc['handle']+'_'+rc['ringname']+'_'+rc['version'].replace('.','-')] = rc
                    ringlistmod = []
                    for ring in ringlist:
                        #current_app.logger.debug('trying to match:'+handle+'_'+ring['ringname']+'_'+ring['ringversion'])
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
            #current_app.logger.debug('Awesome , you just created a new Ring Schema'+str(result))
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
                unique = []
                for p in request.form:
                    q =  p+'='+request.form.get(p)
                    param_list.append(q)
                    
                    parts = p.split('_')
                    if len(parts)>=2:
                        if parts[1] not in unique:
                            print('FLAG1:',parts)
                            unique.append(parts[1])


                lpl = str(len(param_list))
                recovery_string = '&'.join(param_list)

                if collection:
                    redirect = '/'+handle+'/_collections/'+collection+'?rq=post&n='+str(len(unique))+'&'+str(recovery_string)
                else:
                    redirect = '/'+handle+'/'+collection+'?rq=post&n=10&'+str(recovery_string)

            else:
                out['Success'] = False
                out['Message'] = 'There has been an issue, please check your parameters and try again'
                status = 400

            
        if not api:
            d = {'redirect': redirect, 'status':200}
        else:
            d = {'template':'/base_json.html','raw_out':out ,'status':status}

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

        #Validate Collection
        if 'collection' in request.args:
            #TOFIX Can we avid this collectioname validation somehow?
            result = self.validate_collectioname(request.args.get('collection'))
            if result:
                d['collection'] = result
            else:
                redirect = '/'+handle+'/_home'
                return {'redirect': redirect, 'status':404}

        #Query
        if 'lastkey' in request.args:
            lastkey = request.args.get('lastkey')
        else:
            lastkey = None

        if 'endkey' in request.args:
            endkey = request.args.get('endkey')
        else:
            endkey = None

        if 'limit' in request.args:
            limit = request.args.get('limit')
        else:
            limit = "25"

        if 'sort' in request.args:
            sort = request.args.get('sort')
        else:
            sort = None

        if 'noimages' in request.args:
            noimages = request.args.get('noimages')
        else:
            noimages = None

        if 'layer' in request.args:
            layer = request.args.get('layer')
        else:
            layer = PREVIEW_LAYER

        if 'flag' in request.args:
            flag = request.args.get('flag')
        else:
            flag = None

        #Subtract Schema
        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        d['ringdescription'] = schema['rings'][0]['RingDescription']
        d['ringcount'],d['ringorigin'] = self.ring_parameters(handle,ring)
        layers,widgets,sources,labels,names = self.field_dictonaries_init(schema['fields'],layer=layer)

        #Subtract items from DB
        preitems = self.AVM.get_a_b(handle,ring,limit=limit,lastkey=lastkey,endkey=endkey,sort=sort)
        #current_app.logger.debug('PREITEMLIST:'+str(preitems))

        #Prepare data
        itemlist = []
        for preitem in preitems:          
            Item = self.prepare_item(preitem,layers,widgets,sources,labels,names,layer=layer,flag=flag,label=api)
            #current_app.logger.debug('ITEM:'+str(Item))
            itemlist.append(Item)

        
        #Output
        if api:
            out = {}
            o = urlparse.urlparse(request.url)
            host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
            out['_source'] = host_url+"/"+str(handle)+"/"+str(ring)
            if 'schema' in request.args:
                out['rings'] = schema['rings']
                out['fields'] = schema['fields']

            d['fieldtitles'] = [ f['FieldName'] for f in schema['fields'] ]

            
            out['items'] = itemlist 

            d['raw_out'] = out
            d['template'] = 'avispa_rest/get_json_a_b.html'
            #d['api_out'] = json.dumps(out)
            #d['template'] = 'avispa_rest/get_json_a_b.html'

        else:

            #Determine if there will be images

            d['imagesui'] = False
            if not noimages:
                for w in widgets:
                    ##current_app.logger.debug('if '+widgets[w]+' == images')
                    if widgets[w] == 'images':
                        d['imagesui'] = True

            

             #Pagination
            if len(itemlist)>0 and len(itemlist) == limit:
                nextlastkey=itemlist[-1]['_id']
                d['lastkey'] = nextlastkey
                #Still, if the last page has exactly as many items as limit, 
                #the next page will be empty. Please fix

            d['widget'] = widgets
            d['itemlist'] = itemlist
            d['limit'] = limit
            d['FieldLabel'] = labels
            d['rings'] = schema['rings']
            d['template'] = 'avispa_rest/get_a_b.html'

        return d


    def prepare_item(self,preitem,layers,widgets,sources,labels,names,layer=None,flag=None,label=False):

        Item = collections.OrderedDict()  
        Item[u'_id'] = preitem[u'_id']
        Item['_fieldcount'] = 0
        Item['_fullcount'] = 0


        #current_app.logger.debug('LAYERS'+str(layers))
        #current_app.logger.debug('LABELS'+str(labels))

        for fieldid in preitem:

            
            #current_app.logger.debug ('fieldid'+str(fieldid))
            
            if fieldid in layers:
                Item['_fieldcount'] += 1

                
                if preitem[fieldid] != '':
                    Item['_fullcount'] += 1

                if layer:
                    if int(layers[fieldid])>int(layer):
                        #continue
                        pass

                if label:
                    Item[names[fieldid]] = preitem[fieldid]
                else:                   
                    Item[fieldid] = preitem[fieldid]


                if fieldid+'_rich' in preitem and (sources[fieldid] is not None):


                    if label:
                        Item[names[fieldid]+'_rich'] = preitem[fieldid+'_rich']                      
                    else:
                        Item[fieldid+'_rich'] = preitem[fieldid+'_rich']
                        
                    
                    # Retrieve all the fl from the fieldsources for this specific field
                    field_sources = {}
                    list_sources = sources[fieldid].split(',')
                    for source in list_sources:
                        #current_app.logger.debug('source:'+str(source.strip()))
                        if source == '':
                            continue
                        o = urlparse.urlparse(source.strip())
                        # source_uri= urlparse.urlunparse((o1.scheme, o1.netloc, o1.path,'', '', ''))
                        
                        #current_app.logger.debug('o.scheme:'+str(o.scheme))
                        #current_app.logger.debug('o.netloc:'+str(o.netloc))
                        #current_app.logger.debug('o.path:',o.path)

                        if not o.scheme:
                            continue

                        path_parts = o.path.split('/')
                        #if len(path_parts>1):

                        if path_parts[1] == '_api':
                            del path_parts[1]
                            path = '/'.join(path_parts)
                        else:
                            path = o.path   
                            #current_app.logger.debug('corrected xo.path:',path)

                        source_id= urlparse.urlunparse((o.scheme, o.netloc, path,'', '', ''))

                        no_field = True
                        #current_app.logger.debug('o.query:',o.query)
                        queryparts = o.query.split('&')
                        if len(queryparts) > 0:
                            for querypart in queryparts:
                                qp = querypart.split('=')
                                if 'fl' in qp:
                                    qp_parts = qp[1].split('+')
                                    field_sources[source_id] = qp_parts
                                    no_field = False

                        
                            #No field was indicated. Assign the first one

                    # Create representation based on field_sources
                    ItemL = []
                    for rich_item in preitem[fieldid+'_rich']:

                        ItemPart = ''

                        #current_app.logger.debug('rich_item',rich_item)
                        if '_source' in rich_item:
                            o = urlparse.urlparse(rich_item['_source'].strip())
                            #current_app.logger.debug('xo.netloc:',o.netloc)
                            #current_app.logger.debug('xo.path:',o.path)

                            path_parts = o.path.split('/')
                            if path_parts[1] == '_api':
                                del path_parts[1]
                                
                            del path_parts[-1]
                            path = '/'.join(path_parts)  
                            
                            #current_app.logger.debug('adjusted xo.path:',path)
                            
                            source_id= urlparse.urlunparse((o.scheme, o.netloc, path,'', '', ''))
                            #current_app.logger.debug('source_id',source_id)
                            if source_id in field_sources:
                                #There is a way to translate
                                #We are going to overwrite the URLs for the REPRESENTATION
                                    
                                for fl in field_sources[source_id]:
                                    #This will happen as many times as "fl" are indicated
                                    #current_app.logger.debug(fieldid+':fl',fl)
                                    
                                    if fl in rich_item:
                                        ItemPart += rich_item[fl]+' '
                                    else:
                                        current_app.logger.error(fl+': Field Not found. Source:')
                            if no_field:
                                for fl in rich_item:
                                    #This will only happen once with the first real field
                                    if fl[:1] != '_':
                                        #current_app.logger.debug(fieldid+':Not a "_" field:',fl)
                                        ItemPart = rich_item[fl]
                                        #current_app.logger.debug('Item',Item[fieldid])
                            
                                        break

                                
                            ItemL.append(ItemPart) 

                    #In case Item[fieldid] needs to be replaced by its human version (not only URIs)
                    if len(ItemL)>0:
                        if label:
                            Item[names[fieldid]] = ','.join(ItemL)
                        else:
                            Item[fieldid] = ','.join(ItemL)
                     
                            #current_app.logger.debug('REPR:', Item[fieldid])

                if fieldid+'_flag' in preitem and flag:
                    if label:
                        Item[names[fieldid]+'_flag'] = preitem[fieldid+'_flag']
                    else:
                        Item[fieldid+'_flag'] = preitem[fieldid+'_flag']

               
                #Convert comma separated string into list. Also delete first element as it comes empty
                
                if  widgets[fieldid]=='images':
                    
                    if fieldid in Item:
                        images=Item[fieldid].split(',')                
                        del images[0]
                        Item[fieldid] = images
                    elif names[fieldid] in Item:
                        if Item[names[fieldid]]:
                            images=Item[names[fieldid]].split(',')                
                            del images[0]
                            Item[names[fieldid]] = images
                    
                


        #current_app.logger.debug('PREVIEW ITEM:',Item)
        #current_app.logger.debug(Item)
        return Item



    def ring_parameters(self,handle,ring):

        ringparameters = self.AVM.get_a_b_parameters(handle,ring)

        if ringparameters:
            return (ringparameters['count'],ringparameters['ringorigin'])
        else:
            flash(str(ring)+" does not exist or it has been deleted",'UI')
            return False

        
    def field_dictonaries_init(self,schemafields,layer=False):

        layers = {}
        widgets = {}
        sources = {}
        labels = {}
        names = {}

        for schemafield in schemafields:

            layers[schemafield['FieldId']]=int(schemafield['FieldLayer'])           
            widgets[schemafield['FieldId']]=schemafield['FieldWidget']
            sources[schemafield['FieldId']]=schemafield['FieldSource']
            names[schemafield['FieldId']]=schemafield['FieldName']

            if int(schemafield['FieldLayer']) <= int(layer) or (layer is False) :
                
                if schemafield['FieldLabel']:
                    if len(schemafield['FieldLabel']) is not 0:
                        labels[schemafield['FieldId']]=schemafield['FieldLabel']
                else:
                    labels[schemafield['FieldId']]=schemafield['FieldName']

        return layers,widgets,sources,labels,names     

    def validate_collectioname(self,precollectionname):

        collectionname = ''
        if 'collection' in request.args:
            self.ACM = AvispaCollectionsModel()
            collectiond = self.ACM.get_a_x_y(handle,precollectionname) #It comes with just one collection
            if collectiond:     
                return collectiond['collectionname'] 
            else:          
                return False   


    
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
                #current_app.logger.debug('Awesome , you just saved the item to the DB')
                current_app.logger.debug('Item saved with id: '+idx)
                flash("The new item has been created",'UI')
            else:
                out['Success'] = True
                out['Message'] = 'Item saved'
                out['item'] = str(handle+'/'+ring+'/'+idx)
                status = 200

        else:

            if not api:
                #current_app.logger.debug('There was an error creating the item')
                current_app.logger.debug('There was an error creating the item')           
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
            print(out)

            d = {'template':'/base_json.html','raw_out':out ,'status':status}

        return d

        #return redirect('/'+handle+'/'+ring)

    
    def post_rq_a_b(self,request,handle,ring,idx,api=False,collection=None):
        '''
        Form to create new item
        '''
        #current_app.logger.debug(ring)
        schema = self.AVM.ring_get_schema_from_view(handle,ring)


        #schema = self.AVM.ring_get_schema(handle,ring)

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
                    field['FieldSourceRaw'] = source


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


        #current_app.logger.debug('Changing origin?')
        current_app.logger.debug(request.form.get('ringorigin'))
        if request.form.get('ringorigin'):
            #current_app.logger.debug('Changing origin!')
            originresult = self.AVM.set_ring_origin(handle,ring,request.form.get('ringorigin'))

        RB = RingBuilder()
        result =  RB.put_a_b(request,handle,ring)

        if result:
            current_app.logger.debug('Awesome , you just put the changes in the Ring Schema')
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

        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        print('SCHEMA',schema)
        ringschema = schema['rings'][0]
        fieldsschema = schema['fields']
        numfields = len(fieldsschema)
        # current_app.logger.debug(schema) 

        #####
        # We Need to check if all FieldOrders are unique. If not it will cause trouble
        
        existingO = []
        repeatedF = []
        m = 0
        for field in fieldsschema:
            
            if str(field['FieldOrder']) not in existingO:
                # it is new
                existingO.append(field['FieldOrder'])    
            else:
                # it is repeated
                #current_app.logger.debug(field['FieldName']+'('+field['FieldId']+') FieldOrder exists already!')
                repeatedF.append(m)

            m += 1

        if len(repeatedF) > 0:
            #current_app.logger.debug('Reapairing the FieldOrders')
            #current_app.logger.debug('Existing Orders:',existingO)
            #current_app.logger.debug('FieldSchema before:',fieldsschema)
            for n in repeatedF:
                #Go through each one of the repeats and try to find a unique number for it
                for F in range(1,100):
                    #current_app.logger.debug('testing for '+ str(F))
                    if str(F) not in existingO:
                        #current_app.logger.debug(str(F),' is Unique!')
                        fieldsschema[n]['FieldOrder'] = str(F)
                        existingO.append(str(F))
                        break
                    else:
                        pass
                        #current_app.logger.debug(str(F),' already exists!')

            #current_app.logger.debug('FieldSchema after:',fieldsschema)

        #####

        d = {}
        d['message'] = 'Using post_rq_a for handle '+handle 
        d['template'] = 'avispa_rest/put_rq_a_b.html'
        d['ringschema'] = ringschema
        d['fieldsschema'] = fieldsschema
        d['numfields'] = numfields
        
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

        #Subtract Schema
        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        d['ringdescription'] = schema['rings'][0]['RingDescription']
        d['ringcount'],d['ringorigin'] = self.ring_parameters(handle,ring)
        layers,widgets,sources,labels,names = self.field_dictonaries_init(schema['fields'])
        
        #Subtract item from DB
        preitem_result = self.AVM.get_a_b_c(request,handle,ring,idx)
        if preitem_result:
            preitem = preitem_result
            #current_app.logger.debug('PREITEM get_a_b_c:',preitem)
            Item = self.prepare_item(preitem,layers,widgets,sources,labels,names,flag=1,label=api)
        else:
            Item = False
        
        #Output                
        if Item:
            #current_app.logger.debug('Awesome , you just retrieved the item from the DB')
            if api:              
                out = collections.OrderedDict()
                o = urlparse.urlparse(request.url)
                host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
                out['source'] = host_url+"/"+str(handle)+"/"+str(ring)               
                if 'schema' in request.args:
                    out['rings'] = schema['rings']
                    out['fields'] = schema['fields']

                d['fieldtitles'] = [ f['FieldName'] for f in schema['fields'] ]
                
                out['items'] = [] 
                out['items'].append(Item)
                d['raw_out'] = out
                d['template'] = 'avispa_rest/get_json_a_b_c.html'

            else:
                #Determine if there will be images
                d['imagesui'] = False
                for widget in widgets:
                    if widget == 'images':
                        d['imagesui'] = True
                
                d['widget'] = widgets
                d['FieldLabel'] = labels
                d['item'] = Item 
                d['template'] = 'avispa_rest/get_a_b_c.html'

        else: 
          
            d['status'] = '404'
            d['template'] = 'avispa_rest/get_api_a_b_c.html'                     
            flash('This item does not exist','ER')
            #current_app.logger.debug('This item does not exist')


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
            #current_app.logger.debug('Awesome , you just put the changes in the Item')
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

        #current_app.logger.debug('ITEM',item)

        #We need to check if flags are not corrupt or showing an invalid status. Repair if needed

        for i in item:
            #current_app.logger.debug(i+str(item[i]))
            if i[-5:] == '_flag':

                if not item[i]:
                    item[i] = '0000'

                elif int(item[i])<1000 or int(item[i])>=10000 : #Invalid Status
                    if len(str(item[i[:-5]])) < 1: #Empty
                        item[i] = '0000'
                    else:  # If has something
                        item[i] = '1000'

            if item[i] == None:
                item[i] = ''

        #if item['Images']:
         #   images=item['Images'].split(',')
          #  item['Images']=images
        
        schema = self.AVM.ring_get_schema(handle,ring)

        d = {}

        d['ringdescription'] = schema['rings'][0]['RingDescription']
  
        labels = {}
        for schemafield in schema['fields']:
            labels[schemafield['FieldId']]=schemafield['FieldLabel']

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
                    field['FieldSourceRaw'] = source

        

        
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

        print('flag1')

        if result:
            print('flag2')
            #current_app.logger.debug('Item deleted..')
            #msg = 'Item put with id: '+idx
            flash('Item deleted..','UI')
            if collection:
                redirect = '/'+handle+'/_collections/'+collection+'/'+ring           
            else:
                redirect = '/'+handle+'/'+ring


            if 'raw' in request.args: 
                print('flag3')         
                #o = urlparse.urlparse(request.url)
                #host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
                m = {}
                m['uri'] = handle+'/'+ring+'/'+idx
                m['ui_action'] = 'delete'
                message = json.dumps(m)
                d = {'message':message,'template':'avispa_rest/delete_a_b_c_raw.html'}

            elif api:
                out = {}
                out['uri'] = handle+'/'+ring+'/'+idx
                out['method'] = 'DELETE'
                out['success'] = True

                d = {'template':'/base_json.html','raw_out':out ,'status':200}

            else: 
                print('flag4')

                d = {'redirect': redirect, 'status':200}
                

            

        else:
            print('flag5')
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

