from AvispaModel import AvispaModel
from MainModel import MainModel
from flask.ext.login import current_user
from AvispaLabelsModel import AvispaLabelsModel

class AvispaTeamsRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()
        self.MAM = MainModel()
        self.ATM = AvispaLabelsModel()

    def get_a_l(self,request,handle,ring,*args):
        #Shows list of labels for this ring
    	pass

    def put_a_l(self,request,handle,ring,*args):
    	# Changes the labels list
    	pass

    def post_a_l(self,request,handle,ring,*args):
    	# Create the labels list for the first time
    	pass