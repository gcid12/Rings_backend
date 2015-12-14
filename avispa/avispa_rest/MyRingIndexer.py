# MyRingIndexer.py
import json



class MyRingIndexer:

    def __init__(self):
        pass

  
    def indexer(self,handle,ring,idx):

        i = '%s/%s/%s'%(handle,ring,idx)
        out = {}
        out['indexed']=[i]
        out['not_indexed']=[]

        d = {}
        d['json_out'] = json.dumps(out)
        d['template']='base_json.html'
        return d
