#RingBuilder.py
import collections
import urllib2
import json
import urlparse
import requests
from couchdb.http import PreconditionFailed
from flask import flash

from AvispaModel import AvispaModel


class RingBuilder:

    def __init__(self):

        


        self.ringprotocols = {}

        self.ringprotocols['ringprotocol'] = ['RingName','RingDescription','RingVersion','RingURI','RingBuild']
        self.ringprotocols['mandatory'] = ['RingName']
        self.ringprotocols['defaults'] = {'RingVersion':'0.1.0','RingBuild':'1'}

        self.fieldprotocols = {}

        self.fieldprotocols['fieldprotocol'] = ['FieldName', 'FieldLabel', 'FieldSemantic', 'FieldType', 'FieldSource',\
                           'FieldWidget','FieldOrder', 'FieldCardinality', 'FieldMultilingual',\
                           'FieldRequired', 'FieldDefault', 'FieldHint', 'FieldLayer', 'FieldOrder']
        self.fieldprotocols['mandatory'] = ['FieldName']
        self.fieldprotocols['defaults'] = {'FieldType':'TEXT','FieldWidget':'text','FieldCardinality':'single',\
                                  'FieldMultilingual':'FALSE', 'FieldRequired':'FALSE', 'FieldLayer':'2', 'FieldOrder':'1' }


        self.AVM = AvispaModel()


    
    def JSONRingGenerator(self,request,handle):

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):

            pinput = collections.OrderedDict()

            ringname = request.form.get('RingName').lower() # I dont like this here
            handle = handle.lower()
            if request.form.get('RingVersion'):
                ringversion = request.form.get('RingVersion').replace('.','-') # I dont like this here
            else:
                ringversion = self.ringprotocols['defaults']['RingVersion'].replace('.','-')


            print('ringversion:')
            print(ringversion)
            
            requestparameters = {}
            for p in request.form:
                requestparameters[p] = request.form.get(p)
                print(p+':'+request.form.get(p))
 
            # Generate rings block                         
            pinput['rings'] = self._generate_ring_block(requestparameters)
            # Generate fields block
            pinput['fields'] = self._generate_field_block(requestparameters)

            print(pinput)
            
            
            if self.AVM.ring_set_db(handle,ringname,ringversion):
                print('New Ring database created: '+ ringname)
            else:
                print('The Ring '+ ringname +' database already exists')

            if self.AVM.ring_set_blueprint(handle,
                                        ringname,
                                        ringversion,
                                        pinput,
                                        self.ringprotocols['ringprotocol'],
                                        self.fieldprotocols['fieldprotocol']):

                print('Blueprint inserted/updated')
                return True
            else:
                print('Blueprint could not be inserted')
                return False

        elif request.form.get('ringurl') :
            #We are cloning a Ring!!!

            pinput = collections.OrderedDict()              
            
            o1 = urlparse.urlparse(request.url)
            host_url=urlparse.urlunparse((o1.scheme, o1.netloc, '', '', '', ''))
            print(host_url)

            

            o2 = urlparse.urlparse(request.form.get('ringurl'))

            pathparts = o2.path.split('/')
            print(pathparts)
            if pathparts[1]!='_api':
                corrected_path = '/_api'+o2.path
            else:
                corrected_path = o2.path

            corrected_query = 'blueprint'

            ring_url=urlparse.urlunparse((o2.scheme, o2.netloc, corrected_path, '', corrected_query, ''))
            host_ring_url=urlparse.urlunparse((o2.scheme, o2.netloc, '', '', '', ''))
            print(host_ring_url)
 

            
            if host_url==host_ring_url:
                #You are cloning a ring from your localhost
                #Although the result is like doing a put_a_b with no changes as system won't allow duplicates
                print('Cloning local ring')

                pathparts=corrected_path.split('/')
                origin_handle = pathparts[2] #BUG! This will set origin database as handle for new ring 
                handle = handle.lower()
                ringnameparts = pathparts[3].split('_')
                ringname = ringnameparts[0]
                ringversion = ringnameparts[1]
                
                #original blueprint
                blueprint = self.AVM.ring_get_blueprint_from_view(origin_handle,ringname+'_'+ringversion)
                print(blueprint) 
                #Generate pinput from blueprint

                requestparameters = {}


                print('blueprint rings:')


                print(blueprint['rings'])

                
                for k in blueprint['rings'][0]:
                    requestparameters[k] = blueprint['rings'][0][k]

                i = 0
                for n in blueprint['fields']:
                    print('n')
                    print(n)
                    i = i + 1
                    for k in n:   
                        requestparameters[k+'_'+str(i)] = n[k]

                print('requestparameters:')
                print(requestparameters)

                # Generate rings block                         
                pinput['rings'] = self._generate_ring_block(requestparameters)
                # Generate fields block
                pinput['fields'] = self._generate_field_block(requestparameters)

                

            else:
                # You are cloning a ring from another server 
                print('Cloning non local ring')
                r = requests.get(ring_url)
                #r = requests.get('http://localhost:8080/_api/blalab2/reactivoexamen_0-1-2')             
                
                print('Raw JSON Blueprint:')
                print(r.text)
                blueprint = json.loads(r.text)
                
                #Generate pinput from r.text

                #x = '{"source": "/blalab/mecanismos_0-3-0", "items": [{"Descripcion": "Cigue\u00f1al de cuatro codos", "Referencia": "2.1 f", "Imagen": "", "Clasificacion": "Eslabon", "Subclasificacion": "Manivela", "_id": "1378154159"}], "rings": [{"RingVersion": "0.3.0", "RingDescription": "Descripcion de Mecanismos", "RingName": "Mecanismos", "RingURI": "http://ring.apiring.org/mecanismos", "RingBuild": "1"}], "fields": [{"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "1", "FieldRequired": false, "FieldWidget": "textarea", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Descripcion", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}, {"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "1", "FieldRequired": false, "FieldWidget": "images", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Imagen", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}, {"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "2", "FieldRequired": false, "FieldWidget": "text", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Clasificacion", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}, {"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "2", "FieldRequired": false, "FieldWidget": "text", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Subclasificacion", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}, {"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "2", "FieldRequired": false, "FieldWidget": "text", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Referencia", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}]} '
                #blueprint = json.loads(x)
                print('blueprint:')
                print(blueprint)


                handle = handle.lower()
                ringname = blueprint['rings'][0]['RingName'].lower()
                ringversion = blueprint['rings'][0]['RingVersion'].replace('.','-')
                
                requestparameters = {}

                for k in blueprint['rings'][0]:
                    requestparameters[k] = blueprint['rings'][0][k]

                i = 0
                for n in blueprint['fields']:
                    print('n')
                    print(n)
                    i = i + 1
                    for k in n:   
                        requestparameters[k+'_'+str(i)] = n[k]

                print('requestparameters:')
                print(requestparameters)


               

                    # Generate rings block                         
                pinput['rings'] = self._generate_ring_block(requestparameters)
                # Generate fields block
                pinput['fields'] = self._generate_field_block(requestparameters)
 

            try: 
                self.AVM.ring_set_db(handle,ringname,ringversion)
                print('New Ring database created:'+handle+'_'+ringname+'_'+ringversion)
            except(PreconditionFailed):
                print('The Ring '+ ringname +' database already exists')
                flash('The Ring '+ ringname+'_'+ringversion +' already exists')
                return False

            try:
                self.AVM.ring_set_blueprint(handle,
                                        ringname,
                                        ringversion,
                                        pinput,
                                        self.ringprotocols['ringprotocol'],
                                        self.fieldprotocols['fieldprotocol'])

                print('Blueprint inserted/updated')
                return True
            except(ValueError):
                #Delete db you just created
                self.AVM.user_hard_delete_ring(handle,ringname,ringversion)
                print('Blueprint could not be inserted, Delete all trace.')
                return False
                

            
        else:

            print('There is not enough information to create a Ring')
            return False

    def put_a_b(self,request,handle,ring):
        #Same as JSONRingGenerator but to edit blueprint

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):

            pinput = collections.OrderedDict()

            ringname = request.form.get('RingName').lower() # I dont like this here
            handle = handle.lower()
            ringversion = request.form.get('RingVersion').replace('.','-') # I dont like this here
            
            # Generate rings block  

            requestparameters = {}
            for p in request.form:
                requestparameters[p] = request.form.get(p)
                print(p+':'+request.form.get(p))
            

            pinput['rings'] = self._generate_ring_block(requestparameters)
            # Generate fields block
            pinput['fields'] = self._generate_field_block(requestparameters)

            print(pinput)
            
            

            if self.AVM.ring_set_blueprint(handle,
                                        ringname,
                                        ringversion,
                                        pinput,
                                        self.ringprotocols['ringprotocol'],
                                        self.fieldprotocols['fieldprotocol']):

                print('Blueprint inserted/updated')
                return True
            else:
                print('Blueprint could not be inserted')
                return False


        else:

            print('There is not enough information to create a Ring')
            return False



    def _generate_ring_block(self, requestparameters):

        ringsbuffer = collections.OrderedDict()

        
        # Collect all the 'Ring*' fields coming via the RQ
        for k in self.ringprotocols['ringprotocol']:
            print('generate_ring_block iteration:')
            print(k)
            if k in requestparameters:
                print('in')
            #if request.form.get(k):
                #ringsbuffer[k] = request.form[k]
                ringsbuffer[k] = requestparameters[k]
                #print(k)

                if requestparameters[k]=='':

                    if k in self.ringprotocols['mandatory']:
                        raise Exception('Field in Ring Protocol missing : '+k)
                        #print('Field in Ring Protocol missing : '+k)
                    else:
                        if k in self.ringprotocols['defaults']:
                            ringsbuffer[k] = self.ringprotocols['defaults'][k]
                        else:
                            ringsbuffer[k] = ''

        print('ringsbuffer:')
        print(ringsbuffer)

        ringblock = []
        ringblock.append(ringsbuffer)

        return ringblock

    
    def _generate_field_block(self,requestparameters):

        fieldsbuffer = collections.OrderedDict()

        self._generate_fieldindex(requestparameters)

        #ringname = request.form.get('RingName')
        ringname = requestparameters['RingName']
            

        i = 0
        for n in self.fieldindex:
            
            i = i + 1

            for val in self.fieldprotocols['fieldprotocol']:
                
                if i not in fieldsbuffer.keys(): 
                    # Just first for every field. Creates Dictionary that will hold it
                    fieldsbuffer[i] = collections.OrderedDict()

                #if request.form.get(val+'_'+str(i)):
                #if requestparameters[val+'_'+str(i)]:
                print(val+'_'+str(i))
                print('gfb1')
                #print('requestparameters')
                #print(requestparameters)
                if val+'_'+str(i) in requestparameters:

                    print('gfb2')
                    
                    if requestparameters[val+'_'+str(i)] and requestparameters[val+'_'+str(i)]!='None' :

                        print('gfb3')
                        print(requestparameters[val+'_'+str(i)])

                        fieldsbuffer[i][val] = requestparameters[val+'_'+str(i)]
                        #print(val+'_'+str(i))
                    else:
                        #The parameter exists but it is empty
                        print('gfb4')
                        print(val+'_'+str(i))
                        print('gone none')
                        #print
                        fieldsbuffer[i][val] = ''

                        if val in self.fieldprotocols['mandatory']:
                            raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))

                        if val in self.fieldprotocols['defaults']:
                            print("DEFAULTS:")
                            print(val+'_'+str(i))
                            print(self.fieldprotocols['defaults'][val])
                            #print
                            fieldsbuffer[i][val] = self.fieldprotocols['defaults'][val]
                            #fieldsbuffer[i][val] = True
                    

                else:
                    #The checkboxes or fields could not be in the request but still need to be introduced in the database
                    print('gfb5')
                
                    if val in self.fieldprotocols['mandatory']:
                        raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))

                    if val in self.fieldprotocols['defaults']:
                        print('gfb6')
                        print("DEFAULTS 2:")
                        print(val+'_'+str(i))
                        print(self.fieldprotocols['defaults'][val])
                        #print
                        fieldsbuffer[i][val] = self.fieldprotocols['defaults'][val]
                        print(fieldsbuffer[i][val])

                
                
        print("fieldsbuffer:")
        print(fieldsbuffer)
         
        fieldblock = []

        for fieldkey in fieldsbuffer: #Prepare them to be shown in Ring Format 

            tempdict = collections.OrderedDict()
            tempdict['RingName'] = ringname
            tempdict.update(fieldsbuffer[fieldkey])
            fieldblock.append(tempdict)


        return fieldblock


    def _generate_fieldindex(self, requestparameters):

        # Look for 'Field*' sent via POST. Even if they are non-sequential

        self.fieldindex=[]
        #for postkey in request.form:
        for postkey in requestparameters:

            if postkey[:9] == 'FieldName':
                a,b,c = postkey.partition('_')
                #if request.form.get(a+b+c):
                if requestparameters[a+b+c]:
                    self.fieldindex.append(c)
        
        # Collect all the 'Field*' fields

        return True




    #def _createnew_db(self,ringname):




