#RingBuilder.py
import collections

from AvispaModel import AvispaModel


class RingBuilder:

    def __init__(self):

        self.out = collections.OrderedDict()


        self.ringprotocols = {}

        self.ringprotocols['ringprotocol'] = ['RingName','RingDescription','RingVersion','RingURI','RingBuild']
        self.ringprotocols['mandatory'] = ['RingName']
        self.ringprotocols['defaults'] = {'RingVersion':'0.1.0','RingBuild':'1'}

        self.fieldprotocols = {}

        self.fieldprotocols['fieldprotocol'] = ['FieldName', 'FieldLabel', 'FieldSemantic', 'FieldType', 'FieldSource',\
                           'FieldWidget','FieldOrder', 'FieldCardinality', 'FieldMultilingual',\
                           'FieldRequired', 'FieldDefault', 'FieldHint', 'FieldLayer']
        self.fieldprotocols['mandatory'] = ['FieldName']
        self.fieldprotocols['defaults'] = {'FieldType':'TEXT','FieldWidget':'text','FieldCardinality':'single',\
                                  'FieldMultilingual':False, 'FieldRequired':False, 'FieldLayer':3 }


        self.avispamodel = AvispaModel()


    
    def JSONRingGenerator(self,request,handle):

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):


            ringname = request.form.get('RingName').lower() # I dont like this here
            handle = handle.lower()
            ringversion = request.form.get('RingVersion').replace('.','-') # I dont like this here
            
            # Generate rings block                         
            self.out['rings'] = self._generate_ring_block(request)
            # Generate fields block
            self.out['fields'] = self._generate_field_block(request)
            
            
            if self.avispamodel.ring_set_db(handle,ringname,ringversion):
                print('New Ring database created: '+ ringname)
            else:
                print('The Ring '+ ringname +' database already exists')

            if self.avispamodel.ring_set_blueprint(handle,
                                        ringname,
                                        ringversion,
                                        self.out,
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



    def _generate_ring_block(self, request):

        ringsbuffer = collections.OrderedDict()

        
        # Collect all the 'Ring*' fields coming via the RQ
        for k in self.ringprotocols['ringprotocol']:
            if request.form.get(k):
                ringsbuffer[k] = request.form[k]
                #print(k)
            elif k in self.ringprotocols['mandatory']:
                raise Exception('Field in Ring Protocol missing : '+k)
                #print('Field in Ring Protocol missing : '+k)
            else:
                if k in self.ringprotocols['defaults']:
                    ringsbuffer[k] = self.ringprotocols['defaults'][k]
                else:
                    ringsbuffer[k] = ''

        ringblock = []
        ringblock.append(ringsbuffer)

        return ringblock
        

    
    def _generate_field_block(self,request):

        fieldsbuffer = collections.OrderedDict()

        self._generate_fieldindex(request)

        ringname = request.form.get('RingName')
            

        i = 0
        for n in self.fieldindex:
            
            i = i + 1

            for val in self.fieldprotocols['fieldprotocol']:
                
                if i not in fieldsbuffer.keys(): 
                    # Just first for every field. Creates Dictionary that will hold it
                    fieldsbuffer[i] = collections.OrderedDict()

                if request.form.get(val+'_'+str(i)):
                    fieldsbuffer[i][val] = request.form[val+'_'+str(i)]
                    #print(val+'_'+str(i))
                elif val in self.fieldprotocols['mandatory']:
                    raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))


                else:
                    if val in self.fieldprotocols['defaults']:
                        fieldsbuffer[i][val] = self.fieldprotocols['defaults'][val]
                    else:
                        fieldsbuffer[i][val] = None

        fieldblock = []

        for fieldkey in fieldsbuffer: #Prepare them to be shown in Ring Format 

            tempdict = collections.OrderedDict()
            tempdict['RingName'] = ringname
            tempdict.update(fieldsbuffer[fieldkey])
            fieldblock.append(tempdict)


        return fieldblock


    def _generate_fieldindex(self, request):

        # Look for 'Field*' sent via POST. Even if they are non-sequential

        self.fieldindex=[]
        for postkey in request.form:

            if postkey[:9] == 'FieldName':
                a,b,c = postkey.partition('_')
                if request.form.get(a+b+c):
                    self.fieldindex.append(c)
        
        # Collect all the 'Field*' fields

        return True




    #def _createnew_db(self,ringname):




