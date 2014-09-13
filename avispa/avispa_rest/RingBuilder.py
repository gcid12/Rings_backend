#RingBuilder.py
import json
import collections

class RingBuilder:

    def __init__(self):

        self.out = collections.OrderedDict()
 

        self.ringprotocol = ['RingName','RingDescription','RingVersion','RingURI','RingBuild']
        self.ringprotocol_mandatory = ['RingName']
        self.ringprotocol_defaults = {'RingVersion':'0.1.0','RingBuild':'1'}


        self.fieldprotocol = ['FieldName', 'FieldLabel', 'FieldSemantic', 'FieldType', 'FieldSource',\
                           'FieldWidget','FieldOrder', 'FieldCardinality', 'FieldMultilingual',\
                           'FieldRequired', 'FieldDefault', 'FieldHint', 'FieldLayer']
        self.fieldprotocol_mandatory = ['FieldName']
        self.fieldprotocol_defaults = {'FieldType':'TEXT','FieldWidget':'text','FieldCardinality':'single',\
                                  'FieldMultilingual':False, 'FieldRequired':False, 'FieldLayer':3 }



    
    def JSONRingGenerator(self,request):

        

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):

            self.ringname = request.form.get('RingName') # I dont like this here
            
            #GENERATE RING BLOCK                         
            self.out['rings'] = self._generate_ring_block(request)     
            #GENERATE FIELD BLOCK
            self.out['fields'] = self._generate_field_block(request)
            

            print(self.out)
            jsonrs = json.dumps(self.out)
            print jsonrs
           
            #return 'Ring '+self.ringname+' Created'
            return jsonrs

        else:

            return 'There is not enough information to create a Ring'



    def _generate_ring_block(self, request):

        ringsbuffer = collections.OrderedDict()
        

        # Collect all the 'Ring*' fields
        for val in self.ringprotocol:
            if request.form.get(val):
                ringsbuffer[val] = request.form[val]
                print(val)
            elif val in self.ringprotocol_mandatory:
                raise Exception('Field in Ring Protocol missing : '+val)
                #print('Field in Ring Protocol missing : '+val)
            else:
                if val in self.ringprotocol_defaults:
                    ringsbuffer[val] = self.ringprotocol_defaults[val]
                else:
                    ringsbuffer[val] = ''

        ringblock = []
        ringblock.append(ringsbuffer)

        return ringblock

    
    def _generate_field_block(self,request):

        fieldsbuffer = collections.OrderedDict()
                       

        # Look for 'Field*' sent via POST. Even if they are non-sequential
        fieldindex=[]
        for postkey in request.form:

            if postkey[:9] == 'FieldName':
                a,b,c = postkey.partition('_')
                if request.form.get(a+b+c):
                    fieldindex.append(c)
        
        # Collect all the 'Field*' fields
        print(fieldindex)
        i = 0
        for n in fieldindex:
            
            i = i + 1

            for val in self.fieldprotocol:
                
                if i not in fieldsbuffer.keys(): # Just once every field
                    fieldsbuffer[i] = collections.OrderedDict()

                if request.form.get(val+'_'+str(i)):
                    fieldsbuffer[i][val] = request.form[val+'_'+str(i)]
                    print(val+'_'+str(i))
                elif val in self.fieldprotocol_mandatory:
                    raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))

                    #print('Field in Ring Protocol missing : '+val+'_'+str(i))
                    #break
                else:
                    if val in self.fieldprotocol_defaults:
                        fieldsbuffer[i][val] = self.fieldprotocol_defaults[val]
                    else:
                        fieldsbuffer[i][val] = ''

        fieldblock = []

        for fieldkey in fieldsbuffer: #Prepare them to be shown in Ring Format 

            tempdict = collections.OrderedDict()
            tempdict['RingName'] = self.ringname
            tempdict.update(fieldsbuffer[fieldkey])
            fieldblock.append(tempdict)


        return fieldblock
