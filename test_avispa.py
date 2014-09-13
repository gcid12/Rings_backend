#test_RingBuilder.py

import os
from avispa import avispa
import unittest

class RingBuilderTestCase(unittest.TestCase):


    def setUp(self):
        self.app = avispa.test_client()

    def tearDown(self):
        pass

    def test_get_root(self):
        rv = self.app.get('/')
        assert 'Avispa' in rv.data

    def test_get_a(self):
        rv = self.app.get('/moma/')
        assert 'Showing 3 rings' in rv.data

    def test_post_a(self):
        rv = self.app.post('/moma/',
                            data={"RingName":"Tigers4Adoption",
                                  "RingVersion":2,
                                  "FieldName_1":"Name",
                                  "FieldLabel_1":"Name of the tiger"})

        print('This is RV')
        print(rv)
        print

        #assert '"RingName":"Tigers4Adoption"' in rv.data
        self.assertEquals(rv, dict(success=True))



if __name__ == '__main__':
    unittest.main()