# Unit Testing for AvispaModel.py

from avispa.avispa_rest.AvispaModel import AvispaModel
from MainModel import MainModel
from auth.AuthModel import AuthModel
import unittest

class AllModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.AVM = AvispaModel() 
        self.MAM = MainModel() 
        self.ATM = AuthModel() 
        self.user_db = 'myring_users_test_1'

        self.user = {}
        self.user['username'] = 'testuser'
        self.user['email'] = 'testuser@test.com'
        self.user['lastname'] = 'testlastname'
        self.user['firstname'] = 'testfirstname'
        self.user['passhash'] = 'testhash'
        self.user['guid'] = 'testguid'
        self.user['salt'] = 'testsalt'

        self.preblueprint = {}
        self.preblueprint['ringname'] = 'testring'
        self.preblueprint['ringversion'] = '1.2.3'

        self.handle = self.user['username']

        self.ringdbname = self.user['username']+'_'+self.preblueprint['ringname']+'_'+self.preblueprint['ringversion'].replace('.','-')

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
        self.MAM.delete_db(self.user_db)
        

    #MAIN
    def test_create_then_select_a_db(self):
        #TEST
        resultcreate = self.MAM.create_db(self.user_db)
        resultselect = self.MAM.select_db(self.user_db)
        self.assertTrue(resultselect)

    #AUTH
    def test_new_admin_user_db(self):
        #TEST
        result = self.ATM.admin_user_db_create(self.user_db)
        self.assertTrue(result)

    #AUTH
    def test_duplicate_admin_user_db(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        #TEST
        result = self.ATM.admin_user_db_create(self.user_db)
        self.assertFalse(result)

    #AUTH
    def test_new_admin_user(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        #TEST
        result = self.ATM.admin_user_create(self.user,self.user_db)
        self.assertTrue(result)

    #AUTH
    def test_duplicate_admin_user(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        self.ATM.admin_user_create(self.user,self.user_db)
        #TEST
        result = self.ATM.admin_user_create(self.user,self.user_db)
        self.assertFalse(result)

    #AUTH
    def test_create_new_user(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        #TEST
        result = self.MAM.create_user(self.user,self.user_db)
        self.assertTrue(result)

    #AUTH
    def test_select_existing_user_in_existing_db(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        self.MAM.create_user(self.user,self.user_db)
        #TEST
        result = self.MAM.select_user(self.user_db,self.user['username'])
        self.assertEqual(result['email'],self.user['email'])

    #AUTH
    def test_select_non_existing_user_in_existing_db(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        #TEST
        result = self.MAM.select_user(self.user_db,self.user['username'])
        self.assertEqual(result,None)

    #AUTH
    def test_delete_existing_user_in_existing_db(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        self.MAM.create_user(self.user,self.user_db)
        self.MAM.select_user(self.user_db,self.user['username'])
        #TEST
        result = self.MAM.delete_user(self.user_db,self.user['username'])
        self.assertTrue(result)


    #AVISPA
    def test_get_rings_from_empty_ring_list(self):
        #SETUP
        print('Function admin_user_db_create starts')
        self.ATM.admin_user_db_create(self.user_db)
        print('Function create_user starts')
        self.MAM.create_user(self.user,self.user_db)
        #TEST
        print('Function user_get_rings starts')
        result = self.AVM.user_get_rings(self.handle,self.user_db)
        self.assertEqual(0,len(result))

    #AVISPA
    def test_add_ring_to_user_ring_list(self):
        #SETUP
        print('Function admin_user_db_create starts')
        self.ATM.admin_user_db_create(self.user_db)
        print('Function create_user starts')
        self.MAM.create_user(self.user,self.user_db)
        print('Function user_add_ring starts')
        self.AVM.user_add_ring(self.user['username'],self.preblueprint['ringname'],self.preblueprint['ringversion'],self.user_db)
        #TEST
        result = self.MAM.select_user(self.user_db,self.user['username'])
        if result['rings'][0]['ringname']:
            self.assertEqual(result['rings'][0]['ringname'],self.preblueprint['ringname'])
    
    
    #AVISPA
    def test_get_rings_from_ring_list(self):
        #SETUP
        print('Function admin_user_db_create starts')
        self.ATM.admin_user_db_create(self.user_db)
        print('Function create_user starts')
        self.MAM.create_user(self.user,self.user_db)
        print('Function user_add_ring starts')
        self.AVM.user_add_ring(self.user['username'],self.preblueprint['ringname'],self.preblueprint['ringversion'],self.user_db) 
        print('Function create_db starts')
        self.MAM.create_db(self.ringdbname)
        print('Function select_db starts')
        self.MAM.select_db(self.ringdbname)
        print('Function create_doc starts')
        self.MAM.create_doc(self.ringdbname,'blueprint',self.mockblueprint)

        #TEST
        print('Function user_get_rings starts')
        result = self.AVM.user_get_rings(self.handle,self.user_db)
        self.assertEqual(result[0]['ringname'],self.preblueprint['ringname']+'_'+self.preblueprint['ringversion'])
        
        #TEARDOWN
        self.MAM.delete_db(self.ringdbname)
    
    #AUTH
    def test_user_database_views(self):
        #SETUP
        print('Function admin_user_db_create starts')
        self.ATM.admin_user_db_create(self.user_db)
        print('Function create_user starts')
        self.MAM.create_user(self.user,self.user_db)
        print('Function userdb_get_user_by_email')
        result =self.ATM.userdb_get_user_by_email(self.user['email'],self.user_db)
        print(result['key'])
        print(result['value'])
        self.assertEqual(result['key'],self.user['email'])





    #def test_admin_user_create_new(self):

        #self.AM.admin_user_create()



if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(AllModelsTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)