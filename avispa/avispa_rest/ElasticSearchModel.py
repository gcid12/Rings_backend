import collections
from elasticsearch_dsl.connections import connections
from env_config import ES_NODE, TEMP_ACCESS_TOKEN,URL_SCHEME

#SEARCHING
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

#INDEXING
import json
import requests
import urlparse
from AvispaModel import AvispaModel
from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Integer, Object

#LOGGING
import logging
from AvispaLogging import AvispaLoggerAdapter
from flask import g


class ElasticSearchModel:

    def __init__(self,tid=None,ip=None):
        
        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})


    def get_a_b(self,handle,ring,q=None):

        # Connect to Elastic Search Node
        es_url = ES_NODE     
        connections.create_connection(hosts=[es_url])
      
        field = '_all'

        s = Search(index=handle,doc_type=ring) \
            .query("match", **{field:q})

        response = s.execute()

        print("Searching in %s/%s"%(handle,ring))
        print(s.to_dict())

        #return response
        
        out = []
  
        for hit in response:
            # hit meta contains: index,score,id,doc_type
            # i.e:  hit.meta.score

            item = collections.OrderedDict()
            item['_id'] = hit.meta.id

            #print
            #print(hit.meta.score)
            #print('%s/%s/%s'%(hit.meta.index,hit.meta.doc_type,hit.meta.id))

            for m in hit:
                item[m] = hit[m] 
                item[m+'_flag'] = u'1000'
                  
                #print (m,hit[m])   

            out.append(item)

        return out 


    def unindexer(self,handle,ring=None,idx=None):
        
        # Connect to Elastic Search Node
        es = Elasticsearch([ES_NODE])

        out = {}
        out['unindexed']=[]

        if handle and ring and idx:

            es.delete(index=handle,doc_type=ring,id=idx, ignore=[400, 404])
            i = '%s/%s/%s'%(handle,ring,idx)
        elif handle and ring:
            #es.delete(index=handle,doc_type=ring, ignore=[400, 404]) This doesnt work
            # Could not make elasticsearch_py delete a doc_type only
            requests.delete('%s/%s/%s'%(ES_NODE,handle,ring))
            i = '%s/%s'%(handle,ring)
        elif handle:
            es.indices.delete(index=handle, ignore=[400, 404])
            i = '%s'%(handle)

        self.lggr.info('UnIndexing:%s'%i)

        out['unindexed'].append(i)
        
        d = {}
        d['json_out'] = json.dumps(out)
        d['template']='base_json.html'
        return d


        #'index':handle,'type':ringname,'id': idx

    def handle_indexer(self,url,handle):

        #1. Get all the active rings for this handle
        self.AVM = AvispaModel()
        ringlist = self.AVM.user_get_rings(handle)
        print('RINGLIST:',ringlist)

        #2. Index one by one
        out = {}
        out['indexed'] = []

        for ring in ringlist:

            result = self.indexer(url,handle,ring['ringname'])

            x = json.loads(result['json_out'])
            out['indexed'] += x['indexed']

        self.lggr.info('Handle Indexed:%s'%handle)
        
        d = {}
        d['json_out'] = json.dumps(out)
        d['template']='base_json.html'
        return d



    def indexer(self,url,handle,ring,idx=None):
        self.lggr.info('START indexer')
        # Good to Index (a/b) and (a/b/c) as they use same ring_class. 
        # If you want to index a whole handle (a) use handle_indexer

        # Connect to Elastic Search Node
        es_url = ES_NODE
        self.lggr.info('START @ create_connection')     
        connections.create_connection(hosts=[es_url])
        self.lggr.info('END @ create_connection') 
        o = urlparse.urlparse(url) 

        if idx:       
            path = '_api/%s/%s/%s'%(handle,ring,idx)             
        else:
            path = '_api/%s/%s'%(handle,ring)  
        origin_url = urlparse.urlunparse((URL_SCHEME, o.netloc, path, '', '', ''))
        schema,items = self.get_items(origin_url)
        #Preprare the ES Map (as a class)
        ring_class,ring_map = self.prepare_class(schema)
        #Create the index in the ES Cluster (indempotent action)
        self.create_index(ring_class,origin_url)
        #Index the item
        d = {} 
        out = {}
        out['indexed']=[] 
            
        for item in items:
            #Check that item is valid before attempting to index it
            if self.valid_item(item,ring_map):
                
                #try:
                if True:
                    handle,ring,idx = self.index_item(ring_class,origin_url,item)
                    i = '%s/%s/%s'%(handle,ring,idx)
                    out['indexed'].append(i)
                    self.lggr.info('Indexed:%s'%i)

            else:
            
                #Here we store possible indexing errors
                if 'not_indexed' not in out:
                    out['not_indexed']=[] 
 
                out['not_indexed'].append(item)
                self.lggr.error('Document invalid. Not Indexed:%s'%item)
                
        
        d['json_out'] = json.dumps(out)
        d['template']='base_json.html'

        self.lggr.info('END indexer')
        return d

    def valid_item(self,item,ring_map):

        self.lggr.info('START valid_item')

        print("Check item against map:")
        print(ring_map)
        v_item = {}

        for f in ring_map:

            #print(f)
            valid = False
            if f in item:

                #print(ring_map[f],type(ring_map[f]))
                #if ring_map[f] is elasticsearch_dsl.field.String:
                if isinstance(ring_map[f],String):
                    #Check if item[f] is a string 
                    if(isinstance(item[f],str) or 
                       isinstance(item[f],unicode)): 
                        valid = True
                        self.lggr.info('%s -> %s is a string (%s)'%(f,item[f],type(item[f])))
                    else:
                        self.lggr.error('%s -> %s not a string (%s)'%(f,item[f],type(item[f])))


                #elif ring_map[f] is elasticsearch_dsl.field.Object:
                elif isinstance(ring_map[f],Object):
                    #Check if item[f] is an object
                    if isinstance(item[f],dict):
                        v_item[f]={}
                        
                        print(ring_map[f].properties)

                        for p in ring_map[f].properties:
                            #Check if the property exists in the item
                            if p in item[f]:
                                #Check if the property is an elasticsearch_dsl.field.String:
                                if isinstance(ring_map[f].properties[p],String):
                                    #Check if item[f] is a string 
                                    if(isinstance(item[f][p],str) or 
                                       isinstance(item[f][p],unicode)):
                                        v_item[f][p]= item[f][p]
                                        valid = True
                                else:
                                    self.lggr.error('%s not a string (%s)'%(item[f],type(item[f])))
                            else: 
                                self.lggr.error('%s not in item'%p)

                    else:
                        self.lggr.error('%s not a dictionary (%s)'%(item[f],type(item[f])))

                                # TO-DO: Do we want nested objects? If yes develop.

                if valid:
                    # Add field to the output
                    v_item[f] = item[f]
                    self.lggr.info('Valid item. Will Index')
                else:
                    self.lggr.info('Invalid item. Will not index')

            else:
                self.lggr.info('%s not in map'%f)

        self.lggr.info('END valid_item')        
        
        if len(v_item)>0:
            return v_item
        else:
            return False



    def valid_api_url(self,url):

        o = urlparse.urlparse(url)
        p = o.path.split('/')

        if p[1] != '_api':
            path = '/_api'+o.path
        else:
            path = o.path

        return urlparse.urlunparse((URL_SCHEME,o.netloc,path,'','schema=1&limit=_all',''))


    def get_items(self,url):
        url = self.valid_api_url(url)+'&access_token=%s&fieldid=1'%TEMP_ACCESS_TOKEN
        self.lggr.info('START get_items ->%s'%url)
        result = requests.get(url, verify=False)
        self.lggr.info('result ->%s'%result.text)
        self.lggr.info('result.text ->%s'%result.text)
        r = result.json()
        self.lggr.info('result.json() ->%s'%r)
        schema = {'rings':r['rings'],'fields':r['fields']}
        items = r['items']
        self.lggr.info('END get_items')
        return schema,items
            
    def prepare_class(self,schema):
        self.lggr.info('START prepare_class') 

        d = {}
        for field in schema['fields']:

            if field['FieldType'] == 'INTEGER':
                d[field['FieldId']] = Integer()
            elif field['FieldType'] == 'OBJECT':
                if field['FieldMultilingual']:
                    f = {} 
                    f['spa'] = String(analyzer='spanish')
                    f['eng'] = String(analyzer='english')
                    f['ita'] = String(analyzer='italian')
                    f['fra'] = String(analyzer='french')
                    d[field['FieldId']] = Object(properties=f)
                else:
                    #Some other kind of object 
                    d[field['FieldId']] = String()
            elif field['FieldType'] == 'ARRAY':
                d[field['FieldId']] = String()
            elif field['FieldType'] == 'BOOLEAN':
                d[field['FieldId']] = Integer()
            else:
                d[field['FieldId']] = String()

        print(d)
        raw_map = d.copy()

        self.lggr.info('END prepare_class') 
        return type(str(schema['rings'][0]['RingName']),(DocType,),d),raw_map

    def subtract_h_r_i(self,origin_url):
        self.lggr.info('START subtract_h_r_i') 
        url = self.valid_api_url(origin_url)
        print(url)
        o = urlparse.urlparse(url)
        p = o.path.split('/')
        handle = p[2]
        if len(p)>=4:
            ringname = p[3]
        else:
            ringname = None
        if len(p)>=5:
            idx = p[4]
        else:
            idx = None

        self.lggr.info('END subtract_h_r_i') 
        return handle,ringname,idx

    def create_index(self,ring_class,origin_url):
        self.lggr.info('START create_index') 

        handle,ringname,idx = self.subtract_h_r_i(origin_url)
        # create the mappings in elasticsearch 
        R = ring_class.init(handle)
        self.lggr.info('END create_index') 
        return R



    def index_item(self,ring_class,origin_url,item):
        self.lggr.info('START index_item') 

        handle,ringname,idx = self.subtract_h_r_i(origin_url)

        #overwrite the idx with items
        idx = item['_id']

        # create the mappings in elasticsearch 
    
        #print(R)
        #print(handle)
        #print(ringname)
        #print(idx)
        #print(item)

        # create and save an item
        article = ring_class(meta={'index':handle,'type':ringname,'id': idx}, **item)
        print(article)  
        article.save()
        print('SAVED')

        self.lggr.info('END index_item') 
        return (handle,ringname,idx)




            


    


