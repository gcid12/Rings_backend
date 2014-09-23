#RingBuilder.py
import collections
from datetime import datetime 
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, Mapping 

from AvispaCouchDB import AvispaCouchDB

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


        ACD = AvispaCouchDB()
        self.couch=ACD._instantiate_couchdb_as_admin()


    
    def JSONRingGenerator(self,request):

                
        if request.form.get('RingName') and request.form.get('FieldName_1'):


            self.ringname = request.form.get('RingName') # I dont like this here
            
            # Generate rings block                         
            self.out['rings'] = self._generate_ring_block(request)

            # Generate fields block
            self.out['fields'] = self._generate_field_block(request)
            
            
            if self._createnew_db(self.ringname.lower()):
                print('New Ring database created: '+ self.ringname.lower())
            else:
                print('The Ring '+ self.ringname.lower() +' database already exists, overwriting')

            result = self._save_ring_schema_in_db(self.out)

            #print(result)
           
            return result

        else:

            return 'There is not enough information to create a Ring'



    def _generate_ring_block(self, request):

        ringsbuffer = collections.OrderedDict()

        
        # Collect all the 'Ring*' fields coming via the RQ
        for k in self.ringprotocol:
            if request.form.get(k):
                ringsbuffer[k] = request.form[k]
                #print(k)
            elif k in self.ringprotocol_mandatory:
                raise Exception('Field in Ring Protocol missing : '+k)
                #print('Field in Ring Protocol missing : '+k)
            else:
                if k in self.ringprotocol_defaults:
                    ringsbuffer[k] = self.ringprotocol_defaults[k]
                else:
                    ringsbuffer[k] = ''

        ringblock = []
        ringblock.append(ringsbuffer)

        return ringblock
        

    
    def _generate_field_block(self,request):

        fieldsbuffer = collections.OrderedDict()

        self._generate_fieldindex(request)
            

        i = 0
        for n in self.fieldindex:
            
            i = i + 1

            for val in self.fieldprotocol:
                
                if i not in fieldsbuffer.keys(): 
                    # Just first for every field. Creates Dictionary that will hold it
                    fieldsbuffer[i] = collections.OrderedDict()

                if request.form.get(val+'_'+str(i)):
                    fieldsbuffer[i][val] = request.form[val+'_'+str(i)]
                    #print(val+'_'+str(i))
                elif val in self.fieldprotocol_mandatory:
                    raise Exception('Field in Ring Protocol missing : '+val+'_'+str(i))


                else:
                    if val in self.fieldprotocol_defaults:
                        fieldsbuffer[i][val] = self.fieldprotocol_defaults[val]
                    else:
                        fieldsbuffer[i][val] = None

        fieldblock = []

        for fieldkey in fieldsbuffer: #Prepare them to be shown in Ring Format 

            tempdict = collections.OrderedDict()
            tempdict['RingName'] = self.ringname
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




    def _createnew_db(self,ringname):

        
        ringname=str(ringname)

        try:
            self.db = self.couch[ringname]
            return False
        except:
            print('it did not exist. Will create')
            self.db = self.couch.create(ringname)
            return True



        

        


    def _save_ring_schema_in_db(self,out):


        numfields = len(out['fields'])
        RingClass = self._create_ring_class(numfields)
        ring =  RingClass.load(self.db, 'blueprint')

        # Creates Ring Blueprint if it doesn't exist. Uses current one if it exists.

        if ring:
            ring =  RingClass.load(self.db, 'blueprint')
            action = 'edit'

        else:       
            ring = RingClass()
            ring._id = 'blueprint'
            action = 'new'


        # Creates or updates Ring parameters

        args_r = {}
        for r in self.ringprotocol:
            if(action == 'new'):
                if out['rings'][0][r]:
                    args_r[r] = out['rings'][0][r]
            
            elif(action == 'edit'):
                if out['rings'][0][r] == ring.rings[0][r]:
                    #print(r+' did not change')
                    pass
                else:
                    print(r+' changed. Old: "'+ str(ring.rings[0][r]) +'" ('+ str(type(ring.rings[0][r])) +')'+\
                            '  New: "'+ str(out['rings'][0][r]) + '" ('+ str(type(out['rings'][0][r])) +')' )
                    args_r[r] = out['rings'][0][r]

                  

        
        if(action == 'new'):
            ring.rings.append(**args_r)
        
        elif(action == 'edit'):
            for x in args_r:
                ring.rings[0][x] = args_r[x]
            

        # Creates or updates Field parameters

        args_f = {}


        for i in xrange(0,numfields):
            for f in self.fieldprotocol:

                if(action == 'new'):
                    if out['fields'][i][f]:
                        args_f[f] = out['fields'][i][f]

                elif(action == 'edit'):
                    if out['fields'][i][f] == ring.fields[i][f]:
                        #print(f+'_'+str(i+1)+' did not change')
                        pass
                    else:
                        
                        print(f+'_'+str(i+1)+' changed. Old: "'+ str(ring.fields[i][f]) +'" ('+ str(type(ring.fields[i][f])) +')'+\
                            '  New: "'+ str(out['fields'][i][f]) + '" ('+ str(type(out['fields'][i][f])) +')' )
                        
                        args_f[f] = out['fields'][i][f]


            

            if(action == 'new'):
                ring.fields.append(**args_f)
                
            elif(action == 'edit'):
                for y in args_f:
                    ring.fields[i][y] = args_f[y]

            args_f={}

        
        ring.store(self.db)

        return 'ok'


    def _create_ring_class(self,numfields):

        args_r = {}
        args_f = {} 

        for r in self.ringprotocol:

            args_r[r] = TextField()

        for i in xrange(1,numfields):

            for f in self.fieldprotocol:

                args_f[f] =  TextField()


        ringclass = type('Person',
                         (Document,),
                         {
                            '_id' : TextField(),

                            'rings': ListField(DictField(Mapping.build(
                                                    **args_r
                                                ))),
                            'fields':ListField(DictField(Mapping.build(
                                                    **args_f
                                                )))
                                               })

        return ringclass




    









    




