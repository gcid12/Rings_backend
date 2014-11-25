#RingBuilder.py
import collections
import urllib2
import json
import urlparse

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
                                  'FieldMultilingual':False, 'FieldRequired':False, 'FieldLayer':3 }


        self.avispamodel = AvispaModel()


    
    def JSONRingGenerator(self,request,handle):

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):

            pinput = collections.OrderedDict()

            ringname = request.form.get('RingName').lower() # I dont like this here
            handle = handle.lower()
            ringversion = request.form.get('RingVersion').replace('.','-') # I dont like this here
            
            
            requestparameters = {}
            for p in request.form:
                requestparameters[p] = request.form.get(p)
                print(p+':'+request.form.get(p))
 
            # Generate rings block                         
            pinput['rings'] = self._generate_ring_block(requestparameters)
            # Generate fields block
            pinput['fields'] = self._generate_field_block(requestparameters)

            print(pinput)
            
            
            if self.avispamodel.ring_set_db(handle,ringname,ringversion):
                print('New Ring database created: '+ ringname)
            else:
                print('The Ring '+ ringname +' database already exists')

            if self.avispamodel.ring_set_blueprint(handle,
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
            print("ringurl:")
            print(request.form.get('ringurl'))

            o1 = urlparse.urlparse(request.url)
            host_url=urlparse.urlunparse((o1.scheme, o1.netloc, '', '', '', ''))

            o2 = urlparse.urlparse(request.form.get('ringurl'))
            ring_url=urlparse.urlunparse((o2.scheme, o2.netloc, '', '', '', ''))

            
            if host_url==ring_url:
                print('Cloning local ring')
                self.avispamodel.ring_get_blueprint_from_view(handle,ringname)
                #You are cloning a ring from your localhost
                pass
                #Verificar si el request viene localmente. 
                #obtener el Blueprint (del Ring indicado)
                #tranformarlo para la generacion de un nuevo ring

            else:
                pass
            #else
               #Un call comun y corriente  

                print('in')
                r = requests.get(request.form.get('ringurl'))
                #r = requests.get('http://localhost:8080/_api/blalab2/reactivoexamen_0-1-2')
                
                print(r.text)
                

                #transformar request para generacion de nuevo ring

               #crear nuevo ring


            #data = json.load(response)   
            #print data
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
            

            pinput['rings'] = self._generate_ring_block(request)
            # Generate fields block
            pinput['fields'] = self._generate_field_block(request)

            print(pinput)
            
            

            if self.avispamodel.ring_set_blueprint(handle,
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
            elif k in self.ringprotocols['mandatory']:
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
                if val+'_'+str(i) in requestparameters:

                    fieldsbuffer[i][val] = requestparameters[val+'_'+str(i)]
                    #print(val+'_'+str(i))
                elif val in self.fieldprotocols['mandatory']:
                    raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))

                else:
                    if val in self.fieldprotocols['defaults']:
                        #print(val+'_'+str(i))
                        #print(self.fieldprotocols['defaults'][val])
                        #print
                        fieldsbuffer[i][val] = self.fieldprotocols['defaults'][val]
                        #fieldsbuffer[i][val] = True
                    else:
                        #print(val+'_'+str(i))
                        #print('gone none')
                        #print
                        fieldsbuffer[i][val] = None

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




