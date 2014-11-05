# Unit Testing for AvispaModel.py

from AvispaModel import AvispaModel
import unittest

class AvispaModelTestCase(unittest.TestCase):

    def setUp(self):
        self.AM = AvispaModel() 
        self.user_db = 'myring_users_test_1'

        self.user = {}
        self.user['user'] = 'testuser'
        self.user['email'] = 'testuser@test.com'
        self.user['lastname'] = 'testlastname'
        self.user['firstname'] = 'testfirstname'
        self.user['passhash'] = 'testhash'
        self.user['guid'] = 'testguid'
        self.user['salt'] = 'testsalt'

        self.preblueprint = {}
        self.preblueprint['ringname'] = 'testring'
        self.preblueprint['ringversion'] = '1.2.3'

        self.handle = self.user['user']

        self.ringdbname = self.user['user']+'_'+self.preblueprint['ringname']+'_'+self.preblueprint['ringversion'].replace('.','-')

        self.mockblueprint = {
            'fields': [{
                'FieldLabel': None, 
                'FieldOrder': None, 
                'FieldDefault': None, 
                'FieldSource': None, 
                'FieldLayer': 3, 
                'FieldRequired': None, 
                'FieldWidget': u'text', 
                'FieldHint': None, 
                'FieldMultilingual': None, 
                'FieldName': u'name1', 
                'FieldType': u'TEXT', 
                'FieldCardinality': u'Single', 
                'FieldSemantic': None
                }], 
            'added': '2014-11-05T13:02:57Z',
            'rings': [{
                'RingVersion': u'1.2.3', 
                'RingDescription': u'description1', 
                'RingName': u'testring', 
                'RingURI': u'http://ring.apiring.org/test1', 
                'RingBuild': u'100'
                }]
            }

      
    def tearDown(self):
        self.AM.delete_db(self.user_db)
        


    def test_create_then_select_a_db(self):
        #TEST
        resultcreate = self.AM.create_db(self.user_db)
        resultselect = self.AM.select_db(self.user_db)
        self.assertTrue(resultselect)

    def test_new_admin_user_db(self):
        #TEST
        result = self.AM.admin_user_db_create(self.user_db)
        self.assertTrue(result)

    def test_duplicate_admin_user_db(self):
        #SETUP
        self.AM.admin_user_db_create(self.user_db)
        #TEST
        result = self.AM.admin_user_db_create(self.user_db)
        self.assertFalse(result)

    def test_new_admin_user(self):
        #SETUP
        self.AM.admin_user_db_create(self.user_db)
        #TEST
        result = self.AM.admin_user_create(self.user,self.user_db)
        self.assertTrue(result)

    def test_duplicate_admin_user(self):
        #SETUP
        self.AM.admin_user_db_create(self.user_db)
        self.AM.admin_user_create(self.user,self.user_db)
        #TEST
        result = self.AM.admin_user_create(self.user,self.user_db)
        self.assertFalse(result)

    def test_create_new_user(self):
        #SETUP
        self.AM.admin_user_db_create(self.user_db)
        #TEST
        result = self.AM.create_user(self.user_db,self.user)
        self.assertTrue(result)

    def test_select_existing_user_in_existing_db(self):
        #SETUP
        self.AM.admin_user_db_create(self.user_db)
        self.AM.create_user(self.user_db,self.user)
        #TEST
        result = self.AM.select_user(self.user_db,self.user['user'])
        self.assertEqual(result['email'],self.user['email'])

    def test_select_non_existing_user_in_existing_db(self):
        #SETUP
        self.AM.admin_user_db_create(self.user_db)
        #TEST
        result = self.AM.select_user(self.user_db,self.user['user'])
        self.assertEqual(result,None)

    def test_delete_existing_user_in_existing_db(self):
        #SETUP
        self.AM.admin_user_db_create(self.user_db)
        self.AM.create_user(self.user_db,self.user)
        self.AM.select_user(self.user_db,self.user['user'])
        #TEST
        result = self.AM.delete_user(self.user_db,self.user['user'])
        self.assertTrue(result)


    
    def test_get_rings_from_empty_ring_list(self):
        #SETUP
        print('Function admin_user_db_create starts')
        self.AM.admin_user_db_create(self.user_db)
        print('Function create_user starts')
        self.AM.create_user(self.user_db,self.user)
        #TEST
        print('Function user_get_rings starts')
        result = self.AM.user_get_rings(self.handle,self.user_db)
        self.assertFalse(result)


    def test_add_ring_to_user_ring_list(self):
        #SETUP
        print('Function admin_user_db_create starts')
        self.AM.admin_user_db_create(self.user_db)
        print('Function create_user starts')
        self.AM.create_user(self.user_db,self.user)
        print('Function user_add_ring starts')
        self.AM.user_add_ring(self.user['user'],self.preblueprint['ringname'],self.preblueprint['ringversion'],self.user_db)
        #TEST
        result = self.AM.select_user(self.user_db,self.user['user'])
        if result['rings'][0]['ringname']:
            self.assertEqual(result['rings'][0]['ringname'],self.preblueprint['ringname'])
    
    

    def test_get_rings_from_ring_list(self):
        #SETUP
        print('Function admin_user_db_create starts')
        self.AM.admin_user_db_create(self.user_db)
        print('Function create_user starts')
        self.AM.create_user(self.user_db,self.user)
        print('Function user_add_ring starts')
        self.AM.user_add_ring(self.user['user'],self.preblueprint['ringname'],self.preblueprint['ringversion'],self.user_db) 
        print('Function create_db starts')
        self.AM.create_db(self.ringdbname)
        print('Function select_db starts')
        self.AM.select_db(self.ringdbname)
        print('Function create_doc starts')
        self.AM.create_doc(self.ringdbname,'blueprint',self.mockblueprint)

        #TEST
        print('Function user_get_rings starts')
        result = self.AM.user_get_rings(self.handle,self.user_db)
        self.assertEqual(result[0]['ringname'],self.preblueprint['ringname']+'_'+self.preblueprint['ringversion'])
        
        #TEARDOWN
        #self.AM.delete_db(self.ringdbname)




    #def test_admin_user_create_new(self):

        #self.AM.admin_user_create()



if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(AvispaModelTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)