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
            print(data['user']+' exists already')
            return True

        else:
            auser = MyRingUser(email= data['email'],firstname= data['firstname'],lastname=data['lastname'], passhash= data['passhash'])
            auser._id = data['user']
            auser.store(self.db)
            print(data['user'] +' created')
            return False


    def get_a(self,handle):

        data=[]

        try:
            db = self.couch['myring_users']         
            doc = db[handle]
            rings = doc['rings']

            

            for ring in rings:
                db_ringname=str(handle)+'_'+str(ring)
                print(db_ringname)
                db = self.couch[db_ringname]
                RingDescription = db['blueprint']['rings'][0]['RingDescription']
                r = {'ringname':ring,'ringdescription':RingDescription}
                data.append(r)

        except:
            print('No rings for this user')

        return data



    def ring_set_db(self,handle,ringname,ringversion):

            
        db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)

        #try:
        if True:
            
            self.couch.create(db_ringname) 
            self.user_add_ring(handle,ringname,ringversion)
            return True    

        #except:  
        else:         
            return False

    def user_add_ring(self,handle,ringname,ringversion):


        db = self.couch[self.user_database]
        auser =  MyRingUser.load(db, handle)

        auser.rings.append(ringname=str(ringname),version=str(ringversion),added=datetime.now())

        #auser.guid = str(ringname)+'_'+str(ringversion)

        auser.store(db)

        #db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        #db = self.couch['myring_users']
        #doc = db[handle]
        #doc['guid']='9712qwerty'
        #rings = doc['rings']

        return True
            

    def ring_set_blueprint(self,handle,ringname,ringversion,out,ringprotocol,fieldprotocol):


        db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        db = self.couch[db_ringname]
        numfields = len(out['fields'])
        RingClass = self._create_ring_class(numfields,ringprotocol,fieldprotocol)  #This is a dynamically created class
        ring =  RingClass.load(db, 'blueprint')

        # Creates Ring Blueprint if it doesn't exist. Uses current one if it exists.
        if ring:
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
                    print(r+' did not change')
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
                    if out['fields'][i][f] == ring.fields[i][f]:  # Checks if old and new are the same
                        print(f+'_'+str(i+1)+' did not change')
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

        
        ring.store(db)

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

