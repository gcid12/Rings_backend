#CollectionBuilder.py
from flask import flash
from AvispaCollectionsModel import AvispaCollectionsModel

class CollectionBuilder:

    def __init__(self):

        


        self.collectionprotocols = {}

        self.collectionprotocols['collectionprotocol'] = ['CollectioNname','CollectionDescription','CollectionVersion']
        self.collectionprotocols['mandatory'] = ['CollectionName']
        self.collectionprotocols['defaults'] = {'CollectionVersion':'0.1.0'}

        self.ACM = AvispaCollectionsModel()


    
    def CollectionGenerator(self,request,handle):

                
        if request.form.get('CollectionName'):

            collection = {}

            collection['name'] = request.form.get('CollectionName').lower() # I dont like this here
            collection['description'] = request.form.get('CollectionDescription').lower()
            collection['handle'] = handle.lower()
            if request.form.get('CollectionVersion'):
                collection['version'] = request.form.get('CollectionVersion').replace('.','-') # I dont like this here
            else:
                collection['version'] = self.ringprotocols['defaults']['CollectionVersion'].replace('.','-')
            
            ringlist = []
          
            for p in request.form:
                pparts = p.split('_')
                ring = {}
                if pparts[0] == 'ring' and pparts[1]:
                    value = request.form.get(p)
                    vparts = value.split('_')
                    ring['handle'] = vparts[0]
                    ring['ringname'] = vparts[1]
                    ring['version'] = vparts[2]
                    # Will implement this later. This is to separate from primary and secondary rings
                    ring['layer'] = 1 
                    ringlist.append(ring)

            collection['ringlist'] = ringlist
               
            #Here you write to the user.collection document
                     
            if self.ACM.set_collection(handle,collection):
                print('New Collection created: '+collection['name'])
                return True
            else:
                print('The Ring '+ collection['name'] +' database already exists')
                return False


        

    

