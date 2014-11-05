# Unit Testing for AvispaCouchDB.py

from AvispaCouchDB import AvispaCouchDB
import unittest
import couchdb

class AvispaCouchDBTestCase(unittest.TestCase):

    def setUp(self):
        self.ACD = AvispaCouchDB()
        self.user_database = 'myring_users'
        
           

    def tearDown(self):
        pass


    def test_instantiate_couchdb_as_admin(self):
        '''
        Test passes if it connects with Admin Credentials
        '''

        self.couch=self.ACD._instantiate_couchdb_as_admin()
        self.db = self.couch[self.user_database]

    def test_instantiate_without_credentials(self):
        '''
        Test passes if it connects without credentials
        '''

        self.couch=self.ACD._instantiate_couchdb_as_user()
        self.db = self.couch[self.user_database]

    def test_instantiate_with_wrong_credentials(self):
        '''
        Test passes if unauthorized exception is raised with wrong credentials
        '''

        self.couch=self.ACD._instantiate_couchdb_as_user(u'admin',u'happy1233')
        
        try:
            self.db = self.couch[self.user_database]
            raise #should fail if it doesnt raise unauthorized exception
        except(couchdb.Unauthorized):
            pass #Test passes if Unauthorized exception is raised




if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(AvispaCouchDBTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
