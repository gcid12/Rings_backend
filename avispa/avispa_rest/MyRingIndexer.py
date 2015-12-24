# MyRingIndexer.py
import json
import urlparse
from ElasticSearchModel import ElasticSearchModel
from AvispaModel import AvispaModel



class MyRingIndexer:

    def __init__(self):

        self.ELI = ElasticSearchModel()
        self.AVM = AvispaModel()

    def indexer(self,url,handle,ring,idx):

        o = urlparse.urlparse(url) 

        if idx:       
            path = '_api/%s/%s/%s'%(handle,ring,idx)             
        else:
            path = '_api/%s/%s'%(handle,ring)  

        origin_url = urlparse.urlunparse((o.scheme, o.netloc, path, '', '', ''))
        schema,items = self.ELI.get_items(origin_url)

        #Preprare the ES Map (as a class)
        ring_class = self.ELI.prepare_class(schema)
        print(ring_class)

        #Create the index (indempotent)
        self.ELI.create_index(ring_class,origin_url)
        
        #Index the item 
        out['indexed']=[] 
        out['not_indexed']=[]     
        for item in items:
            #try:
            if True:
                handle,ring,idx = self.ELI.index_item(ring_class,origin_url,item)
                out['indexed'].push('%s/%s/%s'%(handle,ring,idx))
            else:
            #except():
                out['not_indexed'].push('%s/%s/%s'%(handle,ring,idx))

            
        
        d = {}
        d['json_out'] = json.dumps(out)
        d['template']='base_json.html'
        return d
