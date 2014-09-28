# Get.py
from AvispaModel import AvispaModel

class Get:


    def __init__(self):

        self.avispamodel = AvispaModel()



    def get_a(self,handle):  #Is this extra step necessary? Why not AvispaRestFunc calls the model directly?

        return self.avispamodel.get_a(handle)




