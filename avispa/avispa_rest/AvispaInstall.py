# AvispaInstall.py
from AvispaCouchDB import AvispaCouchDB
from AvispaUser import AvispaUser

class AvispaInstall:

    def __init__(self):

        ACD = AvispaCouchDB()
        self.couch=ACD._instantiate_couchdb_as_admin()

    def avispa_db_install(self,*args):

        user_database = 'myring_users'

        try:           
            self.db = self.couch[user_database]
            print(user_database+' exists already')
            return True

        except:           
            self.db = self.couch.create(user_database)
            print(user_database+'did not exist. Will create')
            return False

    def avispa_user_create(self,user):

        auser =  AvispaUser.load(self.db, user)

        if auser:
            auser =  AvispaUser.load(self.db, user)  # WTF!!! REPEATING THIS?
            print(user+' exists already')
            action = True

        else:       
            auser = AvispaUser(username= 'Fidencio', guid='sdsd3e3dr3')
            #auser._id = user
            auser._id = 'xserto'
            auser.store(self.db)
            print(user +' created')
            action = False



