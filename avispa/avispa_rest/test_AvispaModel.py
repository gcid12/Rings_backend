# Unit Testing for AvispaModel.py

from AvispaModel import AvispaModel
from MainModel import MainModel
from auth.AuthModel import AuthModel
import unittest

class TestAvispaModel(unittest.TestCase):

    def setUp(self):
        self.AVM = AvispaModel(test=True) 
        self.MAM = MainModel(test=True) 
        self.ATM = AuthModel(test=True) 
        self.user_db = 'myring_users_test_1'

        self.user = {}
        self.user['username'] = 'testuser'
        self.user['email'] = 'testuser@test.com'
        self.user['lastname'] = 'testlastname'
        self.user['firstname'] = 'testfirstname'
        self.user['passhash'] = 'testhash'
        self.user['guid'] = 'testguid'
        self.user['salt'] = 'testsalt'
        #self.user['onlogin'] = 'testhandle'

        self.preschema = {}
        self.preschema['ringname'] = 'testring'
        self.preschema['ringversion'] = '1.2.3'

        self.handle = self.user['username']

        self.ringdbname = self.user['username']+'_'+self.preschema['ringname']+'_'+self.preschema['ringversion'].replace('.','-')

        self.mockschema = {
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
        


    #AVISPA
    def test__user_get_rings__from_empty_ring_list(self):
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
    def test__user_get_rings__from_ring_list(self):
        #SETUP
        self.MAM.delete_db(self.ringdbname)
        print('Function admin_user_db_create starts')
        self.ATM.admin_user_db_create(self.user_db)
        print('Function create_user starts')
        self.MAM.create_user(self.user,self.user_db)
        print('Function user_add_ring starts')
        self.AVM.user_add_ring(self.user['username'],self.preschema['ringname'],self.preschema['ringversion'],self.user_db) 
        print('Function create_db starts')
        self.MAM.create_db(self.ringdbname)
        print('Function select_db starts')
        self.MAM.select_db(self.ringdbname)
        print('Function create_doc starts')
        self.MAM.create_doc(self.ringdbname,'schema',self.mockschema)

        #TEST
        print('Function user_get_rings starts')
        result = self.AVM.user_get_rings(self.handle,self.user_db)
        print('RESULT:::')
        print(result)
        self.assertEqual(result[0]['ringname'],self.preschema['ringname']+'_'+self.preschema['ringversion'])
        
        #TEARDOWN
        #self.MAM.delete_db(self.ringdbname)
        

    #MAIN
    def test__create_db__and__select_db(self):
        #TEST
        resultcreate = self.MAM.create_db(self.user_db)
        resultselect = self.MAM.select_db(self.user_db)
        self.assertTrue(resultselect)

    #MAIN
    def test__create_user__new(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        #TEST
        result = self.MAM.create_user(self.user,self.user_db)
        self.assertTrue(result)

    #MAIN
    def test__select_user__existing_user_in_existing_db(self):
        # Select existing user in existing DB
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        self.MAM.create_user(self.user,self.user_db)
        #TEST
        result = self.MAM.select_user(self.user_db,self.user['username'])
        self.assertEqual(result['email'],self.user['email'])

    #MAIN
    def test__select_user__non_existing_user_in_existing_db(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        #TEST
        result = self.MAM.select_user(self.user_db,self.user['username'])
        self.assertEqual(result,None)

    #MAIN
    def test__select_user__add_ring_to_user(self):
        #test_add_ring_to_user_ring_list
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        self.MAM.create_user(self.user,self.user_db)
        self.AVM.user_add_ring(self.user['username'],self.preschema['ringname'],self.preschema['ringversion'],self.user_db)
        #TEST
        result = self.MAM.select_user(self.user_db,self.user['username'])
        if result['rings'][0]['ringname']:
            self.assertEqual(result['rings'][0]['ringname'],self.preschema['ringname'])

    #MAIN
    def test__delete_user__existing_user_in_existing_db(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        self.MAM.create_user(self.user,self.user_db)
        self.MAM.select_user(self.user_db,self.user['username'])
        #TEST
        result = self.MAM.delete_user(self.user_db,self.user['username'])
        self.assertTrue(result)

    #AUTH
    def test__admin_user_db_create(self):
        #TEST
        result = self.ATM.admin_user_db_create(self.user_db)
        self.assertTrue(result)

    #AUTH
    def test__admin_user_db_create__duplicate(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        #TEST
        result = self.ATM.admin_user_db_create(self.user_db)
        self.assertFalse(result)

    #AUTH
    def test__admin_user_create(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        #TEST
        result = self.ATM.admin_user_create(self.user,self.user_db)
        self.assertTrue(result)

    #AUTH
    def test__admin_user_create__duplicate(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        self.ATM.admin_user_create(self.user,self.user_db)
        #TEST
        result = self.ATM.admin_user_create(self.user,self.user_db)
        self.assertFalse(result)
    
    #AUTH
    def test__userdb_get_user_by_email(self):
        #SETUP
        self.ATM.admin_user_db_create(self.user_db)
        self.MAM.create_user(self.user,self.user_db)
        #TEST
        result =self.ATM.userdb_get_user_by_email(self.user['email'],self.user_db)
        self.assertEqual(result['key'],self.user['email'])



if __name__ == '__main__':
    #unittest.main()

    #If you want to run only one test
    #python -m  unittest avispa.avispa_rest.test_AvispaModel.TestAvispaModel.test__userdb_get_user_by_email

    suite = unittest.TestLoader().loadTestsFromTestCase(TestAvispaModel)
    unittest.TextTestRunner(verbosity=2).run(suite)