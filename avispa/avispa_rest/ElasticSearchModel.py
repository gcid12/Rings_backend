import collections
from elasticsearch_dsl.connections import connections
from env_config import ES_NODE

#SEARCHING
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

#INDEXING
import json
import requests
import urlparse
from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Integer, Object

#LOGGING
import logging
from AvispaLogging import AvispaLoggerAdapter
from flask import g


class ElasticSearchModel:

    def __init__(self):
        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})


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

    def indexer(self,url,handle,ring,idx):

        print('flag1')

        # Connect to Elastic Search Node
        es_url = ES_NODE     
        connections.create_connection(hosts=[es_url])

        print('flag2')

        o = urlparse.urlparse(url) 

        if idx:       
            path = '_api/%s/%s/%s'%(handle,ring,idx)             
        else:
            path = '_api/%s/%s'%(handle,ring)  

        origin_url = urlparse.urlunparse((o.scheme, o.netloc, path, '', '', ''))
        schema,items = self.get_items(origin_url)

        print('flag3')

        #Preprare the ES Map (as a class)
        ring_class = self.prepare_class(schema)
        print(ring_class)

        print('flag4')

        #Create the index (indempotent)
        self.create_index(ring_class,origin_url)

        print('flag5')
        
        #Index the item 
        out = {}
        out['indexed']=[] 
        out['not_indexed']=[]     
        for item in items:
            #try:
            if True:
                handle,ring,idx = self.index_item(ring_class,origin_url,item)
                i = '%s/%s/%s'%(handle,ring,idx)
                out['indexed'].append(i)
                self.lggr.info('Indexed:%s'%i)
            else:
            #except():
                m = '%s/%s/%s'%(handle,ring,idx)
                out['not_indexed'].append(m)
                self.lggr.error('Not Indexed:%s'%m)
 
        d = {}
        d['json_out'] = json.dumps(out)
        d['template']='base_json.html'
        return d


    def valid_api_url(self,url):

        o = urlparse.urlparse(url)
        p = o.path.split('/')

        if p[1] != '_api':
            path = '/_api'+o.path
        else:
            path = o.path

        return urlparse.urlunparse((o.scheme,o.netloc,path,'','schema=1&limit=_all',''))


    def get_items(self,url):
        url = self.valid_api_url(url)
        print(url)
        result = requests.get(url, verify=False)
        #print(result.text)
        r = result.json()
        schema = {'rings':r['rings'],'fields':r['fields']}
        items = r['items']
        return schema,items
            
    def prepare_class(self,schema):

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

        return type(str(schema['rings'][0]['RingName']),(DocType,),d) 

    def subtract_h_r_i(self,origin_url):
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

        return handle,ringname,idx

    def create_index(self,ring_class,origin_url):

        handle,ringname,idx = self.subtract_h_r_i(origin_url)
        # create the mappings in elasticsearch 
        R = ring_class.init(handle)
        return R



    def index_item(self,ring_class,origin_url,item):

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
        return (handle,ringname,idx)

            


    


