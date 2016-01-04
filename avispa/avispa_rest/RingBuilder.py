#RingBuilder.py
import collections
import urllib2
import json
import urlparse
import requests
import logging
from couchdb.http import PreconditionFailed
from flask import flash, g 
from AvispaLogging import AvispaLoggerAdapter

from AvispaModel import AvispaModel


class RingBuilder:

    def __init__(self):

        


        self.ringprotocols = {}

        self.ringprotocols['ringprotocol'] = ['RingName','RingLabel','RingDescription','RingVersion','RingURI','RingBuild','RingParent']
        self.ringprotocols['mandatory'] = ['RingName']
        self.ringprotocols['defaults'] = {'RingVersion':'0.1.0','RingBuild':'1'}

        self.fieldprotocols = {}

        self.fieldprotocols['fieldprotocol'] = ['FieldName', 'FieldLabel', 'FieldSemantic', 'FieldType', 'FieldSource',\
                           'FieldWidget','FieldOrder', 'FieldCardinality', 'FieldMultilingual',\
                           'FieldRequired', 'FieldDefault', 'FieldHint', 'FieldLayer']
        self.fieldprotocols['mandatory'] = ['FieldName']
        self.fieldprotocols['defaults'] = {'FieldType':'STRING','FieldWidget':'text','FieldCardinality':'single',\
                                  'FieldMultilingual':'FALSE', 'FieldRequired':'FALSE', 'FieldLayer':'2', 'FieldOrder':'1' }


        self.AVM = AvispaModel()

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})


    
    def JSONRingGenerator(self,request,handle):

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):

            pinput = collections.OrderedDict()

            ringname = request.form.get('RingName').lower().replace(' ','') # I dont like this here

            handle = handle.lower()
            if request.form.get('RingVersion'):
                ringversion = request.form.get('RingVersion').replace('.','-') # I dont like this here
            else:
                ringversion = self.ringprotocols['defaults']['RingVersion'].replace('.','-')

            
            self.lggr.info('ringversion:'+str(ringversion))
            
            requestparameters = {}

            if request.form.get('RingParent'):
                requestparameters['RingParent'] = request.form.get('RingParent')
            else: 
                requestparameters['RingParent'] = ringname


            for p in request.form:
                if p == 'RingName':
                    requestparameters['RingName'] = ringname
                    requestparameters['RingLabel'] = ringname
                    self.lggr.info((p)+':'+ringname)

                else:
                    requestparameters[p] = request.form.get(p)
                    self.lggr.info((p)+':'+str(request.form.get(p)))
 
            # Generate rings block                         
            pinput['rings'] = self._generate_ring_block(requestparameters)
            # Generate fields block
            pinput['fields'] = self._generate_field_block(requestparameters,self.fieldprotocols['fieldprotocol'])

            self.lggr.info(pinput)
            
            #Check if a database with that name already exists

            try:
                self.AVM.ring_set_db(handle,ringname,ringversion)
                self.lggr.info('New Ring database created: '+ str(ringname))

            except(PreconditionFailed):
                self.lggr.info('The Ring '+ str(ringname) +' database already exists')
                flash('The Ring '+ ringname+' already exists','ER')
                return False



            if self.AVM.ring_set_schema(handle,
                                        ringname,
                                        ringversion,
                                        pinput,
                                        self.ringprotocols['ringprotocol'],
                                        self.fieldprotocols['fieldprotocol']):

                ringd = {'handle':handle,'ringname':ringname,'version':ringversion}
                self.lggr.info('Schema inserted/updated')
                return ringd
            else:
                self.lggr.info('Schema could not be inserted')
                return False

        elif request.form.get('ringurl') :
            #We are cloning a Ring!!!

            pinput = collections.OrderedDict()              
            
            o1 = urlparse.urlparse(request.url)
            host_url=urlparse.urlunparse((o1.scheme, o1.netloc, '', '', '', ''))
            self.lggr.info(host_url)

            

            o2 = urlparse.urlparse(request.form.get('ringurl'))

            pathparts = o2.path.split('/')
            self.lggr.info(pathparts)
            if pathparts[1]!='_api':
                corrected_path = '/_api'+o2.path
            else:
                corrected_path = o2.path

            corrected_query = 'schema'

            ring_url=urlparse.urlunparse((o2.scheme, o2.netloc, corrected_path, '', corrected_query, ''))
            host_ring_url=urlparse.urlunparse((o2.scheme, o2.netloc, '', '', '', ''))
            self.lggr.info(host_ring_url)

            
            if host_url==host_ring_url:
                #You are cloning a ring from your localhost
                #Although the result is like doing a put_a_b with no changes as system won't allow duplicates
                self.lggr.info('Cloning local ring')

                pathparts=corrected_path.split('/')
                origin_handle = pathparts[2] #BUG! This will set origin database as handle for new ring 
                handle = handle.lower()
                ringnameparts = pathparts[3].split('_')
                ringname = ringnameparts[0]
                ringdbname = ringname
                
                #original schema
                schema = self.AVM.ring_get_schema_from_view(origin_handle,ringdbname)
                self.lggr.debug(schema) 
                #Generate pinput from schema
                
                if schema['rings'][0]['RingVersion']:
                    ringversion = schema['rings'][0]['RingVersion'].replace('.','-')
                else:
                    ringversion = ''

                requestparameters = {}


                self.lggr.info('schema rings:')
                self.lggr.info(schema['rings'])

                
                for k in schema['rings'][0]:
                    requestparameters[k] = schema['rings'][0][k]


                if 'RingParent' not in requestparameters:
                    requestparameters['Ringparent'] = requestparameters['RingName']
                

                i = 0
                for n in schema['fields']:
                    
                    self.lggr.info(n)
                    i = i + 1
                    for k in n:   
                        requestparameters[k+'_'+str(i)] = n[k]

                self.lggr.info('requestparameters:'+str(requestparameters))

                # Generate rings block                         
                pinput['rings'] = self._generate_ring_block(requestparameters)
                # Generate fields block
                pinput['fields'] = self._generate_field_block(requestparameters,self.fieldprotocols['fieldprotocol'])

                

            else:
                # You are cloning a ring from another server 
                self.lggr.info('Cloning non local ring')

                try:
                    r = requests.get(ring_url)
                except(requests.exceptions.ConnectionError):
                    self.lggr.info('The connection was refused')
                    flash('The connection to the parent ring was refused. Check the URL in your browser.','ER')
                    return False
                #r = requests.get('http://localhost:8080/_api/blalab2/reactivoexamen_0-1-2')             
                
                self.lggr.info('Raw JSON schema:')
                self.lggr.info(r.text)
                schema = json.loads(r.text)
                
                #Generate pinput from r.text

                #x = '{"source": "/blalab/mecanismos_0-3-0", "items": [{"Descripcion": "Cigue\u00f1al de cuatro codos", "Referencia": "2.1 f", "Imagen": "", "Clasificacion": "Eslabon", "Subclasificacion": "Manivela", "_id": "1378154159"}], "rings": [{"RingVersion": "0.3.0", "RingDescription": "Descripcion de Mecanismos", "RingName": "Mecanismos", "RingURI": "http://ring.apiring.org/mecanismos", "RingBuild": "1"}], "fields": [{"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "1", "FieldRequired": false, "FieldWidget": "textarea", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Descripcion", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}, {"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "1", "FieldRequired": false, "FieldWidget": "images", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Imagen", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}, {"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "2", "FieldRequired": false, "FieldWidget": "text", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Clasificacion", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}, {"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "2", "FieldRequired": false, "FieldWidget": "text", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Subclasificacion", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}, {"FieldLabel": "None", "FieldOrder": "None", "FieldDefault": "None", "FieldSource": "None", "FieldLayer": "2", "FieldRequired": false, "FieldWidget": "text", "FieldHint": "None", "FieldMultilingual": false, "FieldName": "Referencia", "FieldType": "TEXT", "FieldCardinality": "Single", "FieldSemantic": "None"}]} '
                #schema = json.loads(x)
                self.lggr.info('schema:'+str(schema))


                handle = handle.lower()
                ringname = schema['rings'][0]['RingName'].lower().replace(' ','')
                ringversion = schema['rings'][0]['RingVersion'].replace('.','-')
                
                requestparameters = {}

                for k in schema['rings'][0]:
                    requestparameters[k] = schema['rings'][0][k]

                self.lggr.info('pre_requestparameters:'+str(requestparameters))

                if 'RingParent' not in requestparameters:
                    self.lggr.info('adding RingParent to requestparameters')
                    requestparameters['RingParent'] = requestparameters['RingName']

                '''
                if 'RingLabel' not in requestparameters:
                    requestparameters['RingLabel'] = request.form.get('RingName') 
                '''
                
                i = 0
                for n in schema['fields']:
                    
                    self.lggr.info(n)
                    i = i + 1
                    for k in n:   
                        requestparameters[k+'_'+str(i)] = n[k]

                self.lggr.info('requestparameters:'+str(requestparameters))


               

                    # Generate rings block                         
                pinput['rings'] = self._generate_ring_block(requestparameters)
                # Generate fields block
                pinput['fields'] = self._generate_field_block(requestparameters,self.fieldprotocols['fieldprotocol'])
 

            try: 
                self.AVM.ring_set_db(handle,ringname,ringversion)
                self.lggr.info('New Ring database created:'+str(handle)+'_'+str(ringname))
            except(PreconditionFailed):
                self.lggr.info('The Ring '+ str(ringname)+' database already exists')
                flash('The Ring '+ ringname+'_'+ringversion +' already exists','ER')
                return False

            try:
                self.AVM.ring_set_schema(handle,
                                        ringname,
                                        ringversion,
                                        pinput,
                                        self.ringprotocols['ringprotocol'],
                                        self.fieldprotocols['fieldprotocol'])

                
                ringd = {'handle':handle,'ringname':ringname,'version':ringversion}
                self.lggr.info('Schema inserted/updated')
                return ringd
            except(ValueError,KeyError):
                #Delete db you just created
                self.AVM.user_hard_delete_ring(handle,ringname,ringversion)
                self.lggr.info('Schema could not be inserted, Delete all trace.')
                return False
                

            
        else:

            self.lggr.info('There is not enough information to create a Ring')
            return False

    def put_a_b(self,request,handle,ring):
        #Same as JSONRingGenerator but to edit schema

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):

            pinput = collections.OrderedDict()

            ringname = request.form.get('RingName').lower() # I dont like this here
            handle = handle.lower()
            ringversion = request.form.get('RingVersion').replace('.','-') # I dont like this here

            
            
            # Generate rings block  

            requestparameters = {}

            if 'RingParent' not in request.form:
                requestparameters['RingParent'] = request.form.get('RingName')   

            if 'RingLabel' not in request.form:
                requestparameters['RingLabel'] = request.form.get('RingName')          
            
            for p in request.form:
                requestparameters[p] = request.form.get(p)
                self.lggr.info(str(p)+':'+str(request.form.get(p)))
            

            pinput['rings'] = self._generate_ring_block(requestparameters)
            # Generate fields block
            pinput['fields'] = self._generate_field_block(requestparameters,self.fieldprotocols['fieldprotocol'])

            self.lggr.info(pinput)
            
            
            if self.AVM.ring_set_schema(handle,
                                        ringname,
                                        ringversion,
                                        pinput,
                                        self.ringprotocols['ringprotocol'],
                                        self.fieldprotocols['fieldprotocol']):

                self.lggr.info('Schema inserted/updated')
                return True
            else:
                self.lggr.info('Schema could not be inserted')
                return False


        else:

            self.lggr.info('There is not enough information to create a Ring')
            return False



    def _generate_ring_block(self, requestparameters):

        ringsbuffer = collections.OrderedDict()

        
        # Collect all the 'Ring*' fields coming via the RQ
        for k in self.ringprotocols['ringprotocol']:
            self.lggr.info('generate_ring_block iteration:'+str(k))
            if k in requestparameters:
                self.lggr.debug('in')
            #if request.form.get(k):
                #ringsbuffer[k] = request.form[k]
                ringsbuffer[k] = requestparameters[k].strip()
                #self.lggr.info(k)
                

                if ringsbuffer[k]=='':

                    if k in self.ringprotocols['mandatory']:
                        raise Exception('Field in Ring Protocol missing : '+k)
                        #self.lggr.debug('Field in Ring Protocol missing : '+k)
                    else:
                        if k in self.ringprotocols['defaults']:
                            ringsbuffer[k] = self.ringprotocols['defaults'][k]
                        else:
                            ringsbuffer[k] = ''

        self.lggr.debug('ringsbuffer:'+str(ringsbuffer))

        ringblock = []
        ringblock.append(ringsbuffer)

        return ringblock

    
    def _generate_field_block(self,requestparameters,fieldprotocol):

        fieldsbuffer = collections.OrderedDict()

        self._generate_fieldindex(requestparameters)

        #ringname = request.form.get('RingName')
        ringname = requestparameters['RingName']
            

        i = 0
        for n in self.fieldindex:
            
            i = i + 1

            for val in fieldprotocol:
                
                if i not in fieldsbuffer.keys(): 
                    # Just first for every field. Creates Dictionary that will hold it
                    fieldsbuffer[i] = collections.OrderedDict()

                #if request.form.get(val+'_'+str(i)):
                #if requestparameters[val+'_'+str(i)]:
                self.lggr.debug(str(val)+'_'+str(i))
                self.lggr.debug('gfb1')
                #self.lggr.logger.debug('requestparameters')
                #self.lggr.logger.debug(requestparameters)
                if val+'_'+str(i) in requestparameters:

                    self.lggr.logger.debug('gfb2')
                    
                    if requestparameters[val+'_'+str(i)] and requestparameters[val+'_'+str(i)]!='None' :

                        self.lggr.logger.debug('gfb3')
                        self.lggr.logger.debug(requestparameters[val+'_'+str(i)])

                        fieldsbuffer[i][val] = requestparameters[val+'_'+str(i)]
                        #self.lggr.logger.debug(val+'_'+str(i))
                    else:
                        #The parameter exists but it is empty
                        self.lggr.logger.debug('gfb4')
                        self.lggr.logger.debug(val+'_'+str(i))
                        self.lggr.logger.debug('gone none')
                        #self.lggr.logger.debug
                        fieldsbuffer[i][val] = ''

                        if val in self.fieldprotocols['mandatory']:
                            raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))

                        if val in self.fieldprotocols['defaults']:
                            self.lggr.logger.debug("DEFAULTS:")
                            self.lggr.logger.debug(val+'_'+str(i))
                            self.lggr.logger.debug(self.fieldprotocols['defaults'][val])
                            #self.lggr.logger.debug
                            fieldsbuffer[i][val] = self.fieldprotocols['defaults'][val]
                            #fieldsbuffer[i][val] = True
                    

                else:
                    #The checkboxes or fields could not be in the request but still need to be introduced in the database
                    self.lggr.logger.debug('gfb5')
                
                    if val in self.fieldprotocols['mandatory']:
                        raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))

                    if val in self.fieldprotocols['defaults']:
                        self.lggr.logger.debug('gfb6')
                        self.lggr.logger.debug("DEFAULTS 2:")
                        self.lggr.logger.debug(val+'_'+str(i))
                        self.lggr.logger.debug(self.fieldprotocols['defaults'][val])
                        #self.lggr.logger.debug
                        fieldsbuffer[i][val] = self.fieldprotocols['defaults'][val]
                        self.lggr.logger.debug(fieldsbuffer[i][val])
                    else:
                        self.lggr.logger.debug('gfb7')
                        self.lggr.logger.debug("BLANK DEFAULTS:")
                        self.lggr.logger.debug(val+'_'+str(i))
                        fieldsbuffer[i][val] = ''
                        self.lggr.logger.debug(fieldsbuffer[i][val])

                
                
        self.lggr.logger.debug("fieldsbuffer:")
        self.lggr.logger.debug(fieldsbuffer)
         
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




