# Unit Testing for AvispaModel.py

from AvispaModel import AvispaModel
import unittest

class AvispaModelTestCase(unittest.TestCase):

    def setUp(self):

        self.AVM = AvispaModel() 
        self.ring = {}
        self.ring['ringname'] = 'testring'
        self.ring['version'] = '0-1-1'
        self.ring['count'] = 66
        self.ring['origin'] = 'testorigin'

        self.handle = 'testhandle'
   
    def tearDown(self):
        pass

    def test__ring_data_from_user_doc(self):

        r = self.AVM.ring_data_from_user_doc(self.handle,self.ring)
        self.assertEqual(r['ringversionh'],'0.1.1')

    def test__ring_data_from_user_doc_is_dict(self):

        r = self.AVM.ring_data_from_user_doc(self.handle,self.ring)
        self.assertEqual(type(r),dict)



if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(AvispaModelTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)