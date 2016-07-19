import json, collections
import logging
import urlparse, time, datetime
from flask import redirect, flash
from RingBuilder import RingBuilder
from AvispaModel import AvispaModel
from ElasticSearchModel import ElasticSearchModel
from AvispaCollectionsModel import AvispaCollectionsModel
from env_config import PREVIEW_LAYER
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from AvispaLogging import AvispaLoggerAdapter

class AvispaRestFunc:

    def __init__(self,tid=None,ip=None):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})
        self.tid = tid
        self.ip = ip

        self.AVM = AvispaModel(tid=tid,ip=ip)

    # /a

    # GET/a
    def get_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        #NOT CURRENTLY USED. Look for get_a_x  
        d = {'message': 'Using get_a for handle '+handle , 'template':'avispa_rest/index.html' }
    	return d

    
    def get_rq_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        # To find someting in all rings
        d = {'message': 'Using get_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d
 
    
    def get_rs_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    
    def get_q_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using get_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #TESTABLE
    def form_args_to_string(self,rqform):
        ''' This is to avoid the user to have to enter everything again
        We capture all the form args and put them in a string for template to
        repopulate them in ring modeler'''

        param_list = []
        unique = []
        for p in rqform:
            q =  p+'='+rqform.get(p)
            param_list.append(q)
            
            parts = p.split('_')
            if len(parts)>=2:
                if parts[1] not in unique:
                    print('FLAG1:',parts)
                    unique.append(parts[1])

        lpl = str(len(param_list))
        return '&'.join(param_list)

    # POST/a
    
    def post_a(self,handle,ring,idx,api=False,collection=None,rqform=None,*args,**kargs):
        ''' Creates a new ring '''
       
        RB = RingBuilder(tid=self.tid,ip=self.ip)
        result = RB.post_a(rqurl,rqform,handle)
        out = {} 
            
        if result:
            # New Schema has been created
            flash(" Your new Ring has been created. ",'UI')

            #Attach ring to a collection (if collection is provided)
            if collection:

                # Add this new ring to the collection ring list
                ACM = AvispaCollectionsModel(tid=self.tid,ip=self.ip)

                try:
                    if ACM.add_ring_to_collection(handle, collection,result):
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
            #Error. Something went wrong

            if not api:

                flash(" There has been an issue, please check your parameters and try again. ",'UI')

                recovery_string = self.form_args_to_string(rqform)

                if collection:
                    redirect = '/'+handle+'/_collections/'+collection+'?rq=post&n='+str(len(unique))+'&'+str(recovery_string)
                else:
                    redirect = '/'+handle+'/'+ring+'?rq=post&n=10&'+str(recovery_string)

            else:
                out['Success'] = False
                out['Message'] = 'There has been an issue, please check your parameters and try again'
                status = 400

            
        if not api:
            d = {'redirect': redirect, 'status':200}
        else:
            d = {'template':'/base_json.html','raw_out':out ,'status':status}

        return d

    
    def post_rq_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        '''Shows Ring Modeler for new ring'''
        d = {'message': 'Using post_rq_a for handle '+handle , 'template':'avispa_rest/post_rq_a.html'}
        return d

    
    def post_rs_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using post_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a
    
    def put_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using put_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    
    def put_rq_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using put_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    
    def put_rs_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using put_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a
    
    def patch_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using patch_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    
    def patch_rq_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using patch_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    
    def patch_rs_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using patch_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a
    
    def delete_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using delete_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    
    def delete_rq_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using delete_rq_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d
 
       
    def delete_rs_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using delete_rs_a for handle '+handle , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a
    
    def search_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using search_a for handle '+handle , 'template':'avispa_rest/search_a.html'}
        return d

    
    def search_rq_a(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using search_rq_a for handle '+handle , 'template':'avispa_rest/search_rq_a.html'}
        return d

    # /a/b

    def subtract_page_parameters(self,rqargs):
        '''Subtract page related parameters'''

        page = {}

        #Query

        if 'lastkey' in rqargs:
            page['lastkey'] = rqargs.get('lastkey')
        else:
            page['lastkey'] = None
        
        if 'endkey' in rqargs:
            page['endkey'] = rqargs.get('endkey')
        else:
            page['endkey'] = None

        if 'limit' in rqargs:
            page['limit'] = rqargs.get('limit')
        else:
            page['limit'] = "25"

        if 'sort' in rqargs:
            page['sort'] = rqargs.get('sort')
        else:
            page['sort'] = None

        if 'noimages' in rqargs:
            page['noimages'] = rqargs.get('noimages')
        else:
            page['noimages'] = None

        if 'layer' in rqargs:
            page['layer'] = rqargs.get('layer')
        else:
            page['layer'] = PREVIEW_LAYER

        if 'flag' in rqargs:
            page['flag'] = rqargs.get('flag')
        else:
            page['flag'] = None

        if 'fieldid' in rqargs:
            if rqargs.get('fieldid') == '1':
                page['idlabel'] = True
            else:
                page['idlabel'] = False
        else:
            page['idlabel'] = True

        if 'q' in rqargs:
            page['q'] = rqargs.get('q')
        else:
            page['q'] = ''

        return page

    #GET /a/b
    def get_a_b(self,handle,ring,idx,api=False,collection=None,rqargs=None,rqurl=None,*args,**kargs):
        '''List of items in the ring '''

        d = {}
        #Validate Collection
        if collection:
            
            #TOFIX Can we avid this collectioname validation somehow?
            result = self.validate_collection(handle,collection) #Active Collaboration
            if result:
                d['collection'] = result['collectionname'] 
            else:
                redirect = '/'+handle+'/_home'
                return {'redirect': redirect, 'status':404}

        page = self.subtract_page_parameters(rqargs)

        #Subtract Ring info
        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        d['ringdescription'] = schema['rings'][0]['RingDescription']
        d['ringcount'],d['ringorigin'] = self.ring_parameters(handle,ring)

        layers,widgets,sources,labels,names,types = self.field_dictionaries_init(schema['fields'],layer=page['layer'])  
        
        if page['q'] != '' :
            #Search ElasticSearch
            ESM = ElasticSearchModel(tid=self.tid,ip=self.ip)
            preitems = ESM.get_a_b(handle,ring,q=q)
        else:
            #Subtract from DB
            preitems = self.AVM.get_a_b(handle,ring,limit=page['limit'],lastkey=page['lastkey'],endkey=page['endkey'],sort=page['sort'])


        #Prepare data
        itemlist = []
        for preitem in preitems:          
            Item = self.prepare_item(preitem,layers,widgets,sources,labels,names,types,layer=page['layer'],flag=page['flag'],idlabel=page['idlabel'])
            itemlist.append(Item)
        
        #Output
        if api:
            out = {}
            o = urlparse.urlparse(rqurl)
            host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
            out['_source'] = host_url+"/"+str(handle)+"/"+str(ring)
            if 'schema' in rqargs:
                out['rings'] = schema['rings']
                out['fields'] = schema['fields']

            d['fieldnames'] = {}
            for f in schema['fields']:
                d['fieldnames'][f['FieldId']] = f['FieldName'] 

            d['fieldlabels'] = {}
            for f in schema['fields']:
                d['fieldlabels'][f['FieldId']] = f['FieldLabel'] 

            d['fieldids'] = [ f['FieldId'] for f in schema['fields'] ]

            
            out['items'] = itemlist 

            d['raw_out'] = out
            d['template'] = 'avispa_rest/get_json_a_b.html'
            #d['api_out'] = json.dumps(out)
            #d['template'] = 'avispa_rest/get_json_a_b.html'

        else:

            #Determine if there will be images

            d['imagesui'] = False
            if not page['noimages']:
                for w in widgets:
                    if widgets[w] == 'images':
                        d['imagesui'] = True

             #Pagination
            if len(itemlist)>0 and len(itemlist) == page['limit']:
                nextlastkey=itemlist[-1]['_id']
                d['lastkey'] = nextlastkey
                #Still, if the last page has exactly as many items as limit, 
                #the next page will be empty. Please fix

            d['widget'] = widgets
            d['itemlist'] = itemlist
            d['limit'] = page['limit']
            d['FieldLabel'] = labels
            d['rings'] = schema['rings']
            d['template'] = 'avispa_rest/get_a_b.html'

        return d


    def prepare_item(self,preitem,layers,widgets,sources,labels,names,types,layer=None,flag=None,idlabel=True):

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
                                        self.lggr.error(fl+': Field Not found. Source:')
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

                    if fieldid in Item:
                        #Using fieldid                            
                        if Item[fieldid]:
                            if(isinstance(Item[fieldid],str) or 
                               isinstance(Item[fieldid],unicode)): 
                                
                                images=Item[fieldid].split(',')                
                                del images[0]
                                Item[fieldid] = images
                    elif names[fieldid] in Item: 
                        #Using fieldname                         
                        if Item[names[fieldid]]:
                            if(isinstance(Item[names[fieldid]],str) or 
                               isinstance(Item[fieldid],unicode)):
                                images=Item[names[fieldid]].split(',')                
                                del images[0]
                                Item[names[fieldid]] = images

                if types[fieldid].upper()=='OBJECT':
                    print('THIS IS AN OBJECT!!!')
                    
                    if fieldid in Item:
                        print('USING FIELDID:',fieldid)
                        #Using fieldid                            
                        if Item[fieldid]:
                            print('F1')
                            if not isinstance(Item[fieldid],dict):  
                                print('F2')  
                                Item[fieldid] = {}
                        else:
                            Item[fieldid] = {}

                    elif names[fieldid] in Item: 
                        #Using fieldname                         
                        if Item[names[fieldid]]:
                            if not isinstance(Item[names[fieldid]],dict):     
                                Item[names[fieldid]] = {}

                        else:
                            Item[names[fieldid]] = {}

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
        types = {}

        for schemafield in schemafields:

            layers[schemafield['FieldId']]=int(schemafield['FieldLayer'])           
            widgets[schemafield['FieldId']]=schemafield['FieldWidget']
            sources[schemafield['FieldId']]=schemafield['FieldSource']
            names[schemafield['FieldId']]=schemafield['FieldName']
            types[schemafield['FieldId']]=schemafield['FieldType']

            if int(schemafield['FieldLayer']) <= int(layer) or (layer is False) :
                
                if schemafield['FieldLabel']:
                    if len(schemafield['FieldLabel']) is not 0:
                        labels[schemafield['FieldId']]=schemafield['FieldLabel']
                else:
                    labels[schemafield['FieldId']]=schemafield['FieldName']

        return layers,widgets,sources,labels,names,types     

    def validate_collection(self,handle,collectionname=None):

        self.ACM = AvispaCollectionsModel(tid=self.tid,ip=self.ip)
        collectiond = self.ACM.get_a_x_y(handle,collectionname) #Active Collaboration
        if collectiond['collectionname'] == collectionname :     
            return collectiond
        else:          
            return False

    
    def get_rq_a_b(self,handle,ring,idx=False,api=False,collection=None,*args,**kargs):
        # To find something inside of this ring
        d = {'message': 'Using get_rq_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/get_rq_a_b.html'}
        return d

    
    def get_rs_a_b(self,handle,ring,idx=False,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using get_rs_a_b for handle:'+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #POST /a/b
    
    def post_a_b(self,handle,ring,idx=False,api=False,rqargs=None,rqform=None,rqurl=None,collection=None,*args,**kargs):
        '''
        Creates new item
        '''

        idx = self.AVM.post_a_b(rqurl,rqform,handle,ring)
        out = {}

        if idx:

            #Index new item in the search engine
            ESM = ElasticSearchModel(tid=self.tid,ip=self.ip)
            ESM.indexer(rqurl,handle,ring,idx)

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
                if rqform.get('saveandnew'):
                    redirect = '/'+handle+'/_collections/'+collection+'/'+ring+'?rq=post'
                else:
                    redirect = '/'+handle+'/_collections/'+collection+'/'+ring
            else:
                if rqform.get('saveandnew'):
                    redirect = '/'+handle+'/'+ring+'?rq=post'
                else:
                    redirect = '/'+handle+'/'+ring

            if 'raw' in rqargs:          
                
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

    
    def post_rq_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
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

    
    def post_rs_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using post_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PUT /a/b
    
    def put_a_b(self,handle,ring,idx,api=False,collection=None,rqform=None,*args,**kargs):

        # Changing origin?
        if rqform.get('ringorigin'):
            originresult = self.AVM.set_ring_origin(handle,ring,rqform.get('ringorigin'))

        RB = RingBuilder(tid=self.tid,ip=self.ip)
        result =  RB.put_a_b(rqform,handle,ring)

        if result:
            self.lggr.debug('Awesome , you just put the changes in the Ring Schema')
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


    
    def put_rq_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        '''
        Edits the Schema
        '''

        schema = self.AVM.ring_get_schema_from_view(handle,ring)
        print('SCHEMA',schema)
        ringschema = schema['rings'][0]
        fieldsschema = schema['fields']
        numfields = len(fieldsschema)
        # self.lggr.debug(schema) 

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

    
    def put_rs_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using put_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d


    #PATCH /a/b
    
    def patch_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using patch_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    def patch_rq_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using patch_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    def patch_rs_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using patch_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    #DELETE /a/b
    
    def delete_a_b(self,handle,ring,idx=False,api=False,rqargs=None,rqurl=None,collection=None,*args,**kargs):
        
        if self.AVM.user_delete_ring(handle,ring):

            ESM = ElasticSearchModel(tid=self.tid,ip=self.ip)
            ESM.unindexer(rqurl,handle,ring)
            flash('Ring '+ring+' deleted','UI')
        else:
            flash('Could not delete the Ring','ER')
        
        if collection:
            redirect = '/'+handle+'/_collections/'+collection       
        else:
            redirect = '/'+handle
            

        d = {'redirect': redirect, 'status':200}
        
        return d

    
    def delete_rq_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using delete_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d

    
    def delete_rs_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using delete_rs_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/index.html'}
        return d
    
    #SEARCH /a/b
    
    def search_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using search_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/search_a_b.html'}
        return d

    
    def search_rq_a_b(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using search_rq_a_b for handle '+handle+', ring:'+ring , 'template':'avispa_rest/search_rq_a_b.html'}
        return d

    # a/b/c
    #GET /a/b/c
    
    def get_a_b_c(self,handle,ring,idx,api=False,rqargs=None,rqurl=None,collection=None,*args,**kargs):
        '''
        Gets existing item
        ''' 

        self.lggr.debug('++ ARF_get_a_b_c')

        d = {}

        if 'fieldid' in rqargs:
            if rqargs.get('fieldid') == '1':
                idlabel = True
            else:
                idlabel = False
        else:
            idlabel = True

        #Subtract Ring info      
        schema = self.AVM.ring_get_schema_from_view(handle,ring) 
        d['ringdescription'] = schema['rings'][0]['RingDescription']
        d['ringcount'],d['ringorigin'] = self.ring_parameters(handle,ring)

        layers,widgets,sources,labels,names,types = self.field_dictionaries_init(schema['fields'])
        
        print('TYPES:',types)
        #Subtract item from DB
        
        preitem_result = self.AVM.get_a_b_c(handle,ring,idx)
        

        if preitem_result:
            preitem = preitem_result  
            Item = self.prepare_item(preitem,layers,widgets,sources,labels,names,types,flag=1,idlabel=idlabel)
        else:
            Item = False
        
        #Output               
        if Item:
            
            # Awesome , you just retrieved the item from the DB
            if api:              
                out = collections.OrderedDict()
                o = urlparse.urlparse(rqurl)
                host_url= urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
                out['source'] = host_url+"/"+str(handle)+"/"+str(ring)               
                if 'schema' in rqargs:
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
            d['redirect'] = '/'+handle+'/'+ring
            self.lggr.info('This item does not exist')            
            flash('This item does not exist','ER')
        
        self.lggr.debug('-- ARF_get_a_b_c')
        return d
  
    def get_rq_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs): 
        d = {'message': 'Using get_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/get_rq_a_b_c.html'}
        return d

    
    def get_rs_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using get_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #POST /a/b/c
    
    def post_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using post_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    
    def post_rq_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using post_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    
    def post_rs_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using post_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PUT /a/b/c
    
    def put_a_b_c(self,handle,ring,idx,api=False,rqargs=None,rqurl=None,rqform=None,collection=None,*args,**kargs):
        '''
        Puts changes in the item
        '''        
        result = self.AVM.put_a_b_c(rqurl,rqform,handle,ring,idx)

        if result:

            #Index new item in the search engine
            ESM = ElasticSearchModel(tid=self.tid,ip=self.ip)
            ESM.indexer(rqurl,handle,ring,idx)

            # Awesome , you just put the changes in the Item
            flash("Changes saved",'UI')
            if collection:
                redirect = '/'+handle+'/_collections/'+collection+'/'+ring     
            else:
                redirect = '/'+handle+'/'+ring

            if 'raw' in rqargs:          
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

    
    def put_rq_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
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
        item = self.AVM.get_a_b_c(handle,ring,idx)

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

    
    def put_rs_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using put_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #PATCH /a/b/c
    
    def patch_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargss):
        d = {'message': 'Using patch_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    
    def patch_rq_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using patch_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    
    def patch_rs_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using patch_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #DELETE /a/b/c
    
    def delete_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        result = self.AVM.delete_a_b_c(handle,ring,idx)

        if result:

            ESM = ElasticSearchModel(tid=self.tid,ip=self.ip)
            ESM.unindexer(handle,ring,idx)
            
            # Item deleted..
            flash('Item deleted..','UI')
            if collection:
                redirect = '/'+handle+'/_collections/'+collection+'/'+ring           
            else:
                redirect = '/'+handle+'/'+ring


            if 'raw' in rqargs: 
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


    
    def delete_rq_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using delete_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    
    def delete_rs_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using delete_rs_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    #SEARCH /a/b/c
    
    def search_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using search_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/index.html'}
        return d

    
    def search_rq_a_b_c(self,handle,ring,idx,api=False,collection=None,*args,**kargs):
        d = {'message': 'Using search_rq_a_b_c for handle '+handle+', ring->'+ring+'  idx->'+idx , 'template':'avispa_rest/search_rq_a_b_c.html'}
        return d

