#test_RingBuilder.py

import os
from RingBuilder import RingBuilder
import unittest
from flask import request
import sys

sys.path.append('../../') #Sorry about this. Will add to PYTHONPATH later
from avispa import avispa


class RingBuilderTestCase(unittest.TestCase):

    def setUp(self):
        #self.app = avispa.test_cl
        pass
        

    def tearDown(self):
        pass

    def test_JSONRingGenerator_returns_something(self):


        requestx = request.Request()

        #request = avispa.test_request_context('/?next=blabla', method='POST' , form={'RingName':'Snake4Adoption','RingDescription':'This ring shows snakes','FieldName_1':'Name'})
        RB = RingBuilder()
        result = RB.JSONRingGenerator(requestx)
        return result

if __name__ == '__main__':
    unittest.main()