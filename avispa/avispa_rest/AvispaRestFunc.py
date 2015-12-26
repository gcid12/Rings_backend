import json, collections
import logging
import urlparse, time, datetime
from flask import redirect, flash, current_app, g
from RingBuilder import RingBuilder
from AvispaModel import AvispaModel
from ElasticSearchModel import ElasticSearchModel
from AvispaCollectionsModel import AvispaCollectionsModel
from env_config import PREVIEW_LAYER
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from timethis import timethis
from AvispaLogging import AvispaLoggerAdapter

class AvispaRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})


    # /a

    # GET/a
    
    def get_a(self,request,handle,ring,idx,api=False,collection=None,*args):

        ringlist = self.AVM.user_get_rings(handle)

        collectionname = ''
        if collection:
            self.ACM = AvispaCollectionsModel()
            collectiond = self.ACM.get_a_x_y(handle,collection) #It comes with just one collection 
         
            if collectiond:
                if collectiond['valid']:
                    collectionname = collectiond['collectionname']                 
                    ringd = {}
                    for rc in collectiond['rings']:
                        #Building dictionary of collection rings
                        ringd[rc['handle']+'_'+rc['ringname']+'_'+rc['version'].replace('.','-')] = rc
                    ringlistmod = []
                    for ring in ringlist:
                        # Trying to find a match
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
            # New Schema has been created
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

        if 'fieldid' in request.args:
            if request.args.get('fieldid') == '1':
                idlabel = True
            else:
                idlabel = False
        else:
            idlabel = True

        if 'q' in request.args:
            q = request.args.get('q')
        else:
            q = ''


        #Subtract Schema
        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        d['ringdescription'] = schema['rings'][0]['RingDescription']
        d['ringcount'],d['ringorigin'] = self.ring_parameters(handle,ring)
        layers,widgets,sources,labels,names = self.field_dictionaries_init(schema['fields'],layer=layer)

        '''
        #Subtract items from DB
        preitems = self.AVM.get_a_b(handle,ring,limit=limit,lastkey=lastkey,endkey=endkey,sort=sort)
        #current_app.logger.debug('PREITEMLIST:'+str(preitems))
        #print
        #print('PREITEMS:')
        #print(preitems)
        '''
        
        
        #Search ElasticSearch
        if q != '' :
            self.ESM = ElasticSearchModel()
            preitems = self.ESM.get_a_b(handle,ring,q=q)
        else:
            preitems = self.AVM.get_a_b(handle,ring,limit=limit,lastkey=lastkey,endkey=endkey,sort=sort)

        
        print
        print('ES PREITEMS:')
        print(preitems)
        
        

        #Prepare data
        itemlist = []
        for preitem in preitems:          
            Item = self.prepare_item(preitem,layers,widgets,sources,labels,names,layer=layer,flag=flag,idlabel=idlabel)
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


    def prepare_item(self,preitem,layers,widgets,sources,labels,names,layer=None,flag=None,idlabel=True):

        Item = collections.OrderedDict()  
        Item[u'_id'] = preitem[u'_id']
        Item['_fieldcount'] = 0
        Item['_fullcount'] = 0

        for fieldid in preitem:
            
            if fieldid in layers:
                Item['_fieldcount'] += 1

                
                if preitem[fieldid] != '':
                    Item['_fullcount'] += 1

                if layer:
                    if int(layers[fieldid])>int(layer):
                        #continue
                        pass

                if idlabel:
                    Item[fieldid] = preitem[fieldid]
                else:                   
                    Item[names[fieldid]] = preitem[fieldid]


                if fieldid+'_rich' in preitem and (sources[fieldid] is not None):


                    if idlabel:
                        Item[names[fieldid]+'_rich'] = preitem[fieldid+'_rich']                      
                    else:
                        Item[fieldid+'_rich'] = preitem[fieldid+'_rich']
                        
                    
                    # Retrieve all the fl from the fieldsources for this specific field
                    field_sources = {}
                    list_sources = sources[fieldid].split(',')
                    for source in list_sources:
                        
                        if source == '':
                            continue
                        o = urlparse.urlparse(source.strip())

                        if not o.scheme:
                            continue

                        path_parts = o.path.split('/')

                        if path_parts[1] == '_api':
                            del path_parts[1]
                            path = '/'.join(path_parts)
                        else:
                            # Corrected path
                            path = o.path   
                            

                        source_id= urlparse.urlunparse((o.scheme, o.netloc, path,'', '', ''))

                        no_field = True
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
                        
                        if '_source' in rich_item:
                            o = urlparse.urlparse(rich_item['_source'].strip())

                            path_parts = o.path.split('/')
                            if path_parts[1] == '_api':
                                del path_parts[1]
                                
                            del path_parts[-1]
                            path = '/'.join(path_parts)  
                            
                            # Adjusted path
                            
                            source_id= urlparse.urlunparse((o.scheme, o.netloc, path,'', '', ''))
                            if source_id in field_sources:
                                #There is a way to translate
                                #We are going to overwrite the URLs for the REPRESENTATION
                                    
                                for fl in field_sources[source_id]:
                                    #This will happen as many times as "fl" are indicated
                                 
                                    if fl in rich_item:
                                        ItemPart += rich_item[fl]+' '
                                    else:
                                        current_app.logger.error(fl+': Field Not found. Source:')
                            if no_field:
                                for fl in rich_item:
                                    #This will only happen once with the first real field
                                    if fl[:1] != '_':                                       
                                        ItemPart = rich_item[fl]                          
                                        break

                                
                            ItemL.append(ItemPart) 

                    #In case Item[fieldid] needs to be replaced by its human version (not only URIs)
                    if len(ItemL)>0:
                        if idlabel:
                            Item[names[fieldid]] = ','.join(ItemL)
                        else:
                            Item[fieldid] = ','.join(ItemL)

                if fieldid+'_flag' in preitem and flag:
                    if idlabel:
                        Item[fieldid+'_flag'] = preitem[fieldid+'_flag']
                    else:
                        Item[names[fieldid]+'_flag'] = preitem[fieldid+'_flag']

               
                #Convert comma separated string into list. Also delete first element as it comes empty
                #If the item comes from the index it will be a list (not a string)
                            
                if  widgets[fieldid]=='images':

                    print('PREIMAGES:',Item[fieldid])

                    if fieldid in Item:
                        #Using fieldid 
                        print('XX Using fieldid' )     
                        if Item[fieldid]:
                            if(isinstance(Item[fieldid],str) or 
                               isinstance(Item[fieldid],unicode)): 
                                print('f11')
                                images=Item[fieldid].split(',')                
                                del images[0]
                                Item[fieldid] = images
                    elif names[fieldid] in Item: 
                        #Using fieldname  
                        print('XX Using fieldname' )  
                        if Item[names[fieldid]]:
                            if(isinstance(Item[names[fieldid]],str) or 
                               isinstance(Item[fieldid],unicode)):
                                images=Item[names[fieldid]].split(',')                
                                del images[0]
                                Item[names[fieldid]] = images

                    print('IMAGES:',Item[fieldid])

                    
        return Item



    def ring_parameters(self,handle,ring):

        ringparameters = self.AVM.get_a_b_parameters(handle,ring)

        if ringparameters:
            return (ringparameters['count'],ringparameters['ringorigin'])
        else:
            flash(str(ring)+" does not exist or it has been deleted",'UI')
            return False

        
    def field_dictionaries_init(self,schemafields,layer=False):

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
                self.lggr.info('Item saved with id: '+idx)
                flash("The new item has been created",'UI')
            else:
                out['Success'] = True
                out['Message'] = 'Item saved'
                out['item'] = str(handle+'/'+ring+'/'+idx)
                status = 200

        else:

            if not api:
                
                self.lggr.error('There was an error creating the item')           
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
        schema = self.AVM.ring_get_schema_from_view(handle,ring)

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

        # Changing origin?
        current_app.logger.debug(request.form.get('ringorigin'))
        if request.form.get('ringorigin'):
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
                # It is new
                existingO.append(field['FieldOrder'])    
            else:
                # It is repeated
                repeatedF.append(m)

            m += 1

        if len(repeatedF) > 0:
            # 'Reapairing the FieldOrders'
            for n in repeatedF:
                #Go through each one of the repeats and try to find a unique number for it
                for F in range(1,100):
                    # Testing for F 
                    if str(F) not in existingO:
                        # It is Unique!
                        fieldsschema[n]['FieldOrder'] = str(F)
                        existingO.append(str(F))
                        break
                    else:
                        pass
                        # F already exists!

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

        if 'fieldid' in request.args:
            if request.args.get('fieldid') == '1':
                idlabel = True
            else:
                idlabel = False
        else:
            idlabel = True

        #Subtract Schema
        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        d['ringdescription'] = schema['rings'][0]['RingDescription']
        d['ringcount'],d['ringorigin'] = self.ring_parameters(handle,ring)
        layers,widgets,sources,labels,names = self.field_dictionaries_init(schema['fields'])
        
        #Subtract item from DB
        preitem_result = self.AVM.get_a_b_c(request,handle,ring,idx)
        

        if preitem_result:
            preitem = preitem_result  
            Item = self.prepare_item(preitem,layers,widgets,sources,labels,names,flag=1,idlabel=idlabel)
        else:
            Item = False
        
        #Output               
        if Item:
            
            # Awesome , you just retrieved the item from the DB
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
            # Awesome , you just put the changes in the Item
            flash("Changes saved",'UI')
            if collection:
                redirect = '/'+handle+'/_collections/'+collection+'/'+ring     
            else:
                redirect = '/'+handle+'/'+ring

            if 'raw' in request.args:          
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
        schema = self.AVM.ring_get_schema(handle,ring)

        d = {}

        d['ringdescription'] = schema['rings'][0]['RingDescription']
  
        labels = {}
        
        for schemafield in schema['fields']:
            labels[schemafield['FieldId']] = schemafield['FieldLabel']
            

        ringschema = schema['rings'][0]
        fieldsschema = schema['fields']
        numfields = len(fieldsschema)
        item = self.AVM.get_a_b_c(request,handle,ring,idx)

        print(labels)

        #REPAIR FIELDS!
        for f in item:
            print('XXXXX',f)
            
            #REPAIR FLAGS
            if f[-5:] == '_flag':
                if not item[f]:
                    item[f] = '0000'

                elif int(item[f])<1000 or int(item[f])>=10000 : #Invalid Status
                    if len(str(item[f[:-5]])) < 1: #Empty
                        item[f] = '0000'
                    else:  # If has something
                        item[f] = '1000'

            #REPAIR NULLS
            if item[f] == None:
                item[f] = '' 


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

        if result:
            
            # Item deleted..
            flash('Item deleted..','UI')
            if collection:
                redirect = '/'+handle+'/_collections/'+collection+'/'+ring           
            else:
                redirect = '/'+handle+'/'+ring


            if 'raw' in request.args: 
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

