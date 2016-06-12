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
from env_config import TEMP_ACCESS_TOKEN

from AvispaModel import AvispaModel


class RingBuilder:

    def __init__(self,tid=None,ip=None):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})

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

    def generate_blocks(self,requestparameters,fieldprotocol):

        pinput = collections.OrderedDict()

        # Generate rings block                         
        pinput['rings'] = self._generate_ring_block(requestparameters)
        # Generate fields block
        pinput['fields'] = self._generate_field_block(requestparameters,fieldprotocol)

        self.lggr.info(pinput)

        return pinput

    def update_ring_schema(self,p):

        pinput = self.generate_blocks(p,self.fieldprotocols['fieldprotocol'])

        if self.AVM.ring_set_schema(p['handle'],
                                    p['RingName'],
                                    p['RingVersion'],
                                    pinput,
                                    self.ringprotocols['ringprotocol'],
                                    self.fieldprotocols['fieldprotocol']):

            ringd = {'handle':p['handle'],'ringname':p['RingName'],'version':p['RingVersion']}
            self.lggr.info('Schema inserted/updated')
            return ringd
        else:
            self.lggr.info('Schema could not be inserted')
            return False




    def create_ring_db(self,handle,ringname,ringversion):
        
        try:
            self.AVM.ring_set_db(handle,ringname,ringversion)
            self.lggr.info('New Ring database created: '+ str(ringname))
            return True

        except(PreconditionFailed):
            self.lggr.info('The Ring '+ str(ringname) +' database already exists')
            flash('The Ring '+ ringname+' already exists','ER')
            return False

    def subtract_request_parameters(self,rqform,handle,ring=None):

        p = {}

        p['handle'] = handle.lower()

        if ring:
            p['RingName'] = ring 
        elif 'RingName' in rqform:  
            p['RingName'] = rqform.get('RingName').lower().replace(' ','')
            #There should be also a nonaplhanumeric character strip here
        else:
            self.lggr.info('No name for the ring')
            return False
            

        if 'RingVersion' in rqform:
            p['RingVersion'] = rqform.get('RingVersion').replace('.','-') # I dont like this here
        else:
            p['RingVersion'] = self.ringprotocols['defaults']['RingVersion'].replace('.','-')

        if 'RingParent' in rqform:
            p['RingParent'] = rqform.get('RingParent')
        else:
            p['RingParent'] = p['RingName']
        
        if 'RingLabel' in rqform:
            p['RingLabel'] = rqform.get('RingLabel')
        else:
            p['RingLabel'] = p['RingName'] 

        for parameter in rqform:
            if parameter not in p:
                p[parameter] = rqform.get(parameter)
                self.lggr.info((parameter)+':'+str(rqform.get(parameter)))

        return p


    def post_a(self,rqurl,rqform,handle):

        p = self.subtract_request_parameters(rqform,handle)
             
        if p['RingName'] and ('FieldName_1' in p):
            # Minumum requirements ok, create a ring

            # 1. Create empty schema document
            if not self.create_ring_db(p['handle'],p['RingName'],p['RingVersion']):
                return False
 
            # 2. Add fields and extra parameters
            return self.update_ring_schema(p)

        elif 'ringurl' in rqform:
            # We are cloning a Ring

            pinput = collections.OrderedDict()              
            
            # ORIGIN
            # Base URL
            o1 = urlparse.urlparse(rqurl)
            host_url=urlparse.urlunparse((o1.scheme, o1.netloc, '', '', '', ''))
            self.lggr.debug(host_url)
            
            # TARGET 
            # Base URL
            o2 = urlparse.urlparse(rqform.get('ringurl'))
            host_ring_url=urlparse.urlunparse((o2.scheme, o2.netloc, '', '', '', ''))
            self.lggr.info(host_ring_url)

            pathparts = o2.path.split('/')
            self.lggr.info(pathparts)
            if pathparts[1]!='_api':
                corrected_path = '/_api'+o2.path
            else:
                corrected_path = o2.path
            corrected_query = 'schema=1'+'&access_token=%s'%TEMP_ACCESS_TOKEN
            ring_url=urlparse.urlunparse((o2.scheme, o2.netloc, corrected_path, '', corrected_query, ''))

            
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

    def put_a_b(self,rqform,handle,ring):
        # Update the ring schema

        p = self.subtract_request_parameters(rqform,handle,ring=ring)

                
        if p['RingName'] and ('FieldName_1' in p):

            return self.update_ring_schema(p)

        else:
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
                            raise Exception('Field listed as mandatory is missing : '+val+'_'+str(i))

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




