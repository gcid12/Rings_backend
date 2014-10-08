# AvispaModel.py

from datetime import datetime 
import random
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, Mapping 
from AvispaCouchDB import AvispaCouchDB
from MyRingUser import MyRingUser
from MyRingBlueprint import MyRingBlueprint
from CouchViewSync import CouchViewSync

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
            auser = MyRingUser(email= data['email'],firstname= data['firstname'],lastname=data['lastname'], passhash= data['passhash'], guid= data['guid'], salt= data['salt'])
            auser._id = data['user']
            auser.store(self.db)
            print(data['user'] +' created')
            return False


    def user_get_rings(self,handle):

        data=[]

        try:
            db = self.couch['myring_users']         
            doc = db[handle]
            rings = doc['rings']

            

            for ring in rings:
                ringname = str(ring['ringname'])+'_'+str(ring['version']) 
                count = ring['count']
                
                db = self.couch[str(handle)+'_'+ringname]
                RingDescription = db['blueprint']['rings'][0]['RingDescription']
                r = {'ringname':ringname,'ringdescription':RingDescription,'count':count}
                data.append(r)

        except:
            print('No rings for this user')

        return data



    def ring_set_db(self,handle,ringname,ringversion):
           
        db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        db_ringname = db_ringname.replace(" ","")

        try:     
            
            self.couch.create(db_ringname) #Creates this ring database
            self.ring_set_db_views(db_ringname) #Sets all the CouchDB Views needed for this new ring
            self.user_add_ring(handle,ringname,ringversion) #Adds the ring to the user's list
            return True    

        except:          
            return False

    def ring_set_db_views(self,db_ringname):

        db = self.couch[db_ringname]

        CVS = CouchViewSync()
        return CVS.set_db_views(db)



    def user_add_ring(self,handle,ringname,ringversion):

        db = self.couch[self.user_database]
        doc =  MyRingUser.load(db, handle)
        doc.rings.append(ringname=str(ringname),version=str(ringversion),added=datetime.now(),count=0)
        doc.store(db)


        return True

    def ring_get_blueprint(self,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        print(db_ringname)
        db = self.couch[db_ringname]
        blueprint = MyRingBlueprint.load(db,'blueprint')

        return blueprint



    def ring_set_blueprint(self,handle,ringname,ringversion,pinput,ringprotocol,fieldprotocol):


        db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        db = self.couch[db_ringname]
        numfields = len(pinput['fields'])
        ring = MyRingBlueprint.load(db,'blueprint')

        # Creates Ring Blueprint if it doesn't exist. Uses current one if it exists.
        if ring:
            action = 'edit'
        else:       
            ring = MyRingBlueprint()
            #ring = RingClass()
            ring._id= 'blueprint'

            action = 'new'


        # Creates or updates Ring parameters

        args_r = {}
        for r in ringprotocol:
            if(action == 'new'):
                if pinput['rings'][0][r]:
                    args_r[r] = pinput['rings'][0][r]
            
            elif(action == 'edit'):
                if pinput['rings'][0][r] == ring.rings[0][r]:
                    print(r+' did not change')
                    pass
                else:
                    print(r+' changed. Old: "'+ str(ring.rings[0][r]) +'" ('+ str(type(ring.rings[0][r])) +')'+\
                            '  New: "'+ str(pinput['rings'][0][r]) + '" ('+ str(type(pinput['rings'][0][r])) +')' )
                    args_r[r] = pinput['rings'][0][r]

                  

        
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
                    if pinput['fields'][i][f]:
                        args_f[f] = pinput['fields'][i][f]

                elif(action == 'edit'):
                    if pinput['fields'][i][f] == ring.fields[i][f]:  # Checks if old and new are the same
                        print(f+'_'+str(i+1)+' did not change')
                        pass
                    else:
                        
                        print(f+'_'+str(i+1)+' changed. Old: "'+ str(ring.fields[i][f]) +'" ('+ str(type(ring.fields[i][f])) +')'+\
                            '  New: "'+ str(pinput['fields'][i][f]) + '" ('+ str(type(pinput['fields'][i][f])) +')' )
                        
                        args_f[f] = pinput['fields'][i][f]


            

            if(action == 'new'):
                ring.fields.append(**args_f)
                
            elif(action == 'edit'):
                for y in args_f:
                    ring.fields[i][y] = args_f[y]

            args_f={}

        
        ring.store(db)

        return 'ok'

    def _blueprint_create_class(self,numfields,ringprotocol,fieldprotocol):
        '''
        This function is deprecated. Now we just instantiate MyRingBlueprint class
        '''

        args_r = {}
        args_f = {} 

        for r in ringprotocol:

            args_r[r] = TextField()

        for i in xrange(1,numfields):

            for f in fieldprotocol:

                args_f[f] =  TextField()


        blueprintclass = type('BlueprintClass',
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

        return blueprintclass

    def ring_create_class(self,blueprint):

        args_i = {}
        fields = blueprint['fields']
        for field in fields:
            args_i[field['FieldName']] = TextField()
 

        RingClass = type('RingClass',
                         (Document,),
                         {
                            '_id' : TextField(),
                            'added' : DateTimeField(default=datetime.now),
                            'items': ListField(DictField(Mapping.build(
                                                    **args_i
                                                )))
                                               }) 

        return RingClass


    def post_a_b(self,request,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        blueprint = self.ring_get_blueprint(handle,ringname)
        
        values = {}
        fields = blueprint['fields']
        for field in fields:
            values[field['FieldName']] = request.form.get(field['FieldName'])


        RingClass = self.ring_create_class(blueprint)
        item = RingClass()         
        item._id= str(random.randrange(1000000000,9999999999))
        item.items.append(**values)
        
        if item.store(db):
        
            self.increase_item_count(handle,ringname)

            return item._id

        return False

    def increase_item_count(self,handle,ringname):

        self.db = self.couch[self.user_database]
        user =  MyRingUser.load(self.db, handle)

        if user:

            for ring in user['rings']:
                if ring['ringname']+'_'+ring['version'] == ringname:
                    ring['count'] += 1
                    print('Item Count increased')

            if user.store(self.db):
                
                return True
            else:
                print('Could not increase item count')
                return False

    def get_a_b(self,handle,ringname,limit=25,lastkey=None):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]
        batch = 500  #This is not the number of results per page. 
         # https://pythonhosted.org/CouchDB/client.html#couchdb.client.Database.iterview

        options = {}
        if lastkey:
            limit +=1
            options['startkey']=lastkey  #Where the last page left

        options['limit']=limit #Number of results per page
        
        
        #options['key']='4393588627'
        
        #options['startkey_docid']='4393588627'
        #options['endkey']='4393588626'
        #options['endkey_docid']=4


        result = db.iterview('avispa/get_a_b',batch,**options)



        #print (result)
        items = []
        i = 0

        for row in result:

            i += 1
            if lastkey and i==1:
                #continue  #skipping the lastkey
                print('length:')
                print(len(items))
                continue
                #pass

            item = {}
            item[u'id'] = row['id']
            item.update(row['value'])
            #item['id']=row['id']
            #item['values']=row['value']
            items.append(item)
            #print(item)

        #print(items)

        return items





    def get_a_b_c(self,request,handle,ringname,idx):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        blueprint = self.ring_get_blueprint(handle,ringname)
        RingClass = self.ring_create_class(blueprint)

        item = RingClass.load(db,idx)

        return item



    def couchdb_pager(db, view_name='_all_docs',
                  startkey=None, startkey_docid=None,
                  endkey=None, endkey_docid=None, bulk=5000):

        '''
        import couchdb
        couch = couchdb.Server()
        db = couch['mydatabase']

        # This is dangerous.
        for doc in db:
            pass

        # This is always safe.
        for doc in couchdb_pager(db):
            pass

        '''
        # Request one extra row to resume the listing there later.
        options = {'limit': bulk + 1}
        if startkey:
            options['startkey'] = startkey
            if startkey_docid:
                options['startkey_docid'] = startkey_docid
        if endkey:
            options['endkey'] = endkey
            if endkey_docid:
                options['endkey_docid'] = endkey_docid
        done = False
        while not done:
            view = db.view(view_name, **options)
            rows = []
            # If we got a short result (< limit + 1), we know we are done.
            if len(view) <= bulk:
                done = True
                rows = view.rows
            else:
                # Otherwise, continue at the new start position.
                rows = view.rows[:-1]
                last = view.rows[-1]
                options['startkey'] = last.key
                options['startkey_docid'] = last.id

            for row in rows:
                yield row.id








        










