from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections
from env_config import ES_NODE

class AvispaModel:

    # Connect to Elastic Search Node
    es_url = ES_NODE
        
    connections.create_connection(hosts=[es_url])
  
    index = 'teamamerica'
    ring = 'vendor_translations'
    field = '_all'

    searchstring = raw_input('search what?\n')

    s = Search(index=index,doc_type=ring) \
        .query("match", **{field:searchstring})

    response = s.execute()

    print(s.to_dict())


    for hit in response:
        # hit meta contains: index,score,id,doc_type
        # i.e:  hit.meta.score

        print
        print(hit.meta.score)
        print('%s/%s/%s'%(hit.meta.index,hit.meta.doc_type,hit.meta.id))

        
        for m in hit:
            
            print (m,hit[m])

    print
    print
    print('**************************************')
    print
    print
        


    


