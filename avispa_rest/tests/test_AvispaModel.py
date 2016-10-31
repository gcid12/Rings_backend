# Unit Testing for AvispaModel.py

from avispa_rest.AvispaModel import AvispaModel
import unittest

class TC(unittest.TestCase):

    def setUp(self):

        self.AVM = AvispaModel() 

        self.handle = 'testhandle'

        self.ring = {}
        self.ring['ringname'] = 'testring'
        self.ring['version'] = '0-1-1'
        self.ring['count'] = 66
        self.ring['origin'] = 'testorigin'
        self.ring['rings'] = []

        self.schema = {}
        self.schema['fields'] = []
        self.schema['rings'] = []
        self.schema['rings'].append({'RingDescription':'test description','RingLabel':'test label'})

        self.schemas = {}  #Creating a two member list of schemas
        self.schemas['ring1'] = self.schema
        self.schemas['ring2'] = self.schema
     
   
    def tearDown(self):
        pass

    def test__ring_data_from_user_doc__output_check(self):

        r = self.AVM.ring_data_from_user_doc(self.handle,self.ring)
        self.assertEqual(r['ringversionh'],'0.1.1')

    def test__ring_data_from_user_doc__output_length(self):

        r = self.AVM.ring_data_from_user_doc(self.handle,self.ring)
        self.assertEqual(len(r),5)

    def test__ring_data_from_schema__output_check(self):

        r = self.AVM.ring_data_from_schema(self.schema)
        self.assertEqual(r['ringdescription'],'test description')

    def test__ring_data_from_schema__output_length(self):

        r = self.AVM.ring_data_from_schema(self.schema)
        self.assertEqual(len(r),4)



if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(TC)
    unittest.TextTestRunner(verbosity=2).run(suite)