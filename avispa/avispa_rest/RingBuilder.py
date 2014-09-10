#RingBuilder.py
import json
import collections

class RingBuilder:
    
    def JSONRingGenerator(self,request):


        out = collections.OrderedDict()
        out['rings'] = []
        out['fields'] = []
        out['items'] = []

        ringprotocol = ['RingName','RingDescription','RingVersion','RingURI','RingBuild']
        ringprotocol_mandatory = ['RingName']
        ringprotocol_defaults = {'RingVersion':'0.1.0','RingBuild':'1'}


        fieldprotocol = ['FieldName', 'FieldLabel', 'FieldSemantic', 'FieldType', 'FieldSource',\
                           'FieldWidget','FieldOrder', 'FieldCardinality', 'FieldMultilingual',\
                           'FieldRequired', 'FieldDefault', 'FieldHint', 'FieldLayer']
        fieldprotocol_mandatory = ['FieldName']
        fieldprotocol_defaults = {'FieldType':'TEXT','FieldWidget':'text','FieldCardinality':'single',\
                                  'FieldMultilingual':False, 'FieldRequired':False, 'FieldLayer':3 }




        ringsbuffer = collections.OrderedDict()
        fieldsbuffer = collections.OrderedDict()
        itemsbuffer = collections.OrderedDict()

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):

            ringname = request.form.get('RingName') # I dont like this here

            # Collect all the 'Ring*' fields
            for val in ringprotocol:
                if request.form.get(val):
                    ringsbuffer[val] = request.form[val]
                    print(val)
                elif val in ringprotocol_mandatory:
                    print('Field in Ring Protocol missing : '+val)
                else:
                    if val in ringprotocol_defaults:
                        ringsbuffer[val] = ringprotocol_defaults[val]
                    else:
                        ringsbuffer[val] = ''
                    
                               

            # Look for 'Field*' sent via POST. Even if they are non-sequential
            fieldindex=[]
            for postkey in request.form:

                if postkey[:9] == 'FieldName':
                    a,b,c = postkey.partition('_')
                    fieldindex.append(c)
            
            # Collect all the 'Field*' fields
            print(fieldindex)
            i = 0
            for n in fieldindex:
                i = i + 1

                for val in fieldprotocol:
                    
                    if i not in fieldsbuffer.keys(): # Just once every field
                        fieldsbuffer[i] = collections.OrderedDict()

                    if request.form.get(val+'_'+str(i)):
                        fieldsbuffer[i][val] = request.form[val+'_'+str(i)]
                        print(val+'_'+str(i))
                    elif val in fieldprotocol_mandatory:
                        #raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))
                        print('Field in Ring Protocol missing : '+val+'_'+i)
                    else:
                        if val in fieldprotocol_defaults:
                            fieldsbuffer[i][val] = fieldprotocol_defaults[val]
                        else:
                            fieldsbuffer[i][val] = ''






            out['rings'].append(ringsbuffer)

           # print(ringsbuffer)
            #print(fieldsbuffer)

                        
            for fieldkey in fieldsbuffer: #Prepare them to be shown in Ring Format 

                tempdict = collections.OrderedDict()
                tempdict['RingName'] = ringname
                tempdict.update(fieldsbuffer[fieldkey])
                out['fields'].append(tempdict)


            print(out)
            print
            

            jsonrs = json.dumps(out)

            print jsonrs

           
            return 'hello'

        else:

            return 'There is not enough information to create a Ring'
