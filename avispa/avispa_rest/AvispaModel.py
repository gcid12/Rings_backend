# AvispaModel.py

from datetime import datetime 
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, Mapping 
from AvispaCouchDB import AvispaCouchDB
from MyRingUser import MyRingUser

class AvispaModel:


    def __init__(self):

        ACD = AvispaCouchDB()
        self.couch=ACD._instantiate_couchdb_as_admin()
        self.user_database = 'myring_users'


    def admin_user_db_create(self,*args):

        print('flag1')


        try:

            print('flag2')           
            self.db = self.couch[self.user_database]
            print(self.user_database+' exists already')
            return True

        except:  

            print('flag3')         
            self.db = self.couch.create(self.user_database)
            print(self.user_database+'did not exist. Will create')
            return False




    def admin_user_create(self,data):

        self.db = self.couch[self.user_database]

        

        auser =  MyRingUser.load(self.db, data['user'])

        if auser:
            auser =  MyRingUser.load(self.db, data['user'])  # WTF!!! REPEATING THIS?
            print(data['user']+' exists already')
            return True

        else:
            auser = MyRingUser(email= data['email'],firstname= data['firstname'],lastname=data['lastname'], passhash= data['passhash'])
            auser._id = data['user']
            auser.store(self.db)
            print(data['user'] +' created')
            return False

#_createnew_db
    def post_a(self,ringname):

            
        ringname=str(ringname)

        try:
            self.db = self.couch[ringname]
            return False
        except:
            print('it did not exist. Will create')
            self.db = self.couch.create(ringname)
            return True

    def put_a_b(self,out,ringprotocol,fieldprotocol):


        numfields = len(out['fields'])
        RingClass = self._create_ring_class(numfields,ringprotocol,fieldprotocol)  #This is a dynamically created class
        ring =  RingClass.load(self.db, 'blueprint')

        # Creates Ring Blueprint if it doesn't exist. Uses current one if it exists.

        if ring:
            ring =  RingClass.load(self.db, 'blueprint')
            action = 'edit'

        else:       
            ring = RingClass()
            ring._id= 'blueprint'

            action = 'new'


        # Creates or updates Ring parameters

        args_r = {}
        for r in ringprotocol:
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
            for f in fieldprotocol:

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

    def _create_ring_class(self,numfields,ringprotocol,fieldprotocol):

        args_r = {}
        args_f = {} 

        for r in ringprotocol:

            args_r[r] = TextField()

        for i in xrange(1,numfields):

            for f in fieldprotocol:

                args_f[f] =  TextField()


        ringclass = type('RingClass',
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

