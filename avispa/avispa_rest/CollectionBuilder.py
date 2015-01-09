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


    
    def post_a_x(self,request,handle):

                
        if request.form.get('CollectionName'):

            collectiond = {}

            collectiond['name'] = request.form.get('CollectionName').lower() # I dont like this here
            collectiond['description'] = request.form.get('CollectionDescription').lower()
            collectiond['handle'] = handle.lower()
            if request.form.get('CollectionVersion'):
                collectiond['version'] = request.form.get('CollectionVersion').replace('.','-') # I dont like this here
            else:
                collectiond['version'] = self.collectionprotocols['defaults']['CollectionVersion'].replace('.','-')
            
            ringlist = []
          
            for p in request.form:
                pparts = p.split('_')
                ring = {}
                if pparts[0] == 'ring' and pparts[1]:
                    value = request.form.get(p)
                    vparts = value.split('_')
                    ring['handle'] = vparts[0]
                    ring['ringname'] = vparts[1]
                    ring['version'] = vparts[2].replace('.','-')
                    # Will implement this later. This is to separate from primary and secondary rings
                    ring['layer'] = 1 
                    ringlist.append(ring)

            collectiond['ringlist'] = ringlist
               
            #Here you write to the user.collection document
                     
            if self.ACM.post_a_x(handle,collectiond):
                print('New Collection created: '+collectiond['name'])
                return True
            else:
                print('The Collection '+ collectiond['name'] +' database already exists')
                return False

    def put_a_x_y(self,request,handle,collection):

        #Same as collectiongenerator
        if request.form.get('CollectionName'):

            collectiond = {}

            collectiond['name'] = request.form.get('CollectionName').lower() # I dont like this here
            collectiond['description'] = request.form.get('CollectionDescription').lower()
            collectiond['handle'] = handle.lower()
            if request.form.get('CollectionVersion'):
                collectiond['version'] = request.form.get('CollectionVersion').replace('.','-') # I dont like this here
            else:
                collectiond['version'] = self.collectionprotocols['defaults']['CollectionVersion'].replace('.','-')
            
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

            collectiond['ringlist'] = ringlist
               
            #Here you write to the user.collection document
                     
            if self.ACM.put_a_x_y(handle,collectiond):
                print('Collection updated: '+collectiond['name'])
                return True
            else:
                print('The Collection '+ collectiond['name'] +' database already exists')
                return False



        

    

