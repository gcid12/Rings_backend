# MyRingTool.py

from AvispaModel import AvispaModel

class MyRingTool:

    def __init__(self):

        self.avispamodel = AvispaModel()        

    def install(self,request,*args):

        data = {}
        data['user'] = 'admin'
        data['email'] = 'admin@domain.com'
        data['lastname'] = 'admin last name'
        data['firstname'] = 'admin last name'
        data['passhash'] = 'adminpass'


        #user = 'admin' #This is just the first user that is installed on a vanilla MyRing
        msg = ''
  
        if self.avispamodel.admin_user_db_create():
            msg += ' MyRing DB already exists. '
            if self.avispamodel.admin_user_create(data):
                msg += data['user'] + ' already existed. '
            else:
                msg += data['user'] + ' just Created. '

        else:
            msg += 'MyRing DB just Installed. '


    	d = {'message': 'using install tool:'+msg , 'template':'avispa_rest/index.html'}
        return d


    def create_user(self,request,*args):


        if 'rs' in request.args:


            data = {}

            if request.form.get('user'):
                data['user'] = request.form.get('user')
            else:
                data['user'] = 'defaultuser'

            if request.form.get('email'):
                data['email'] = request.form.get('email')
            else:
                data['email'] = 'defaultemail'

            if request.form.get('firstname'):
                data['firstname'] = request.form.get('firstname')
            else:
                data['firstname'] = 'defaultfirstname'

            if request.form.get('lastname'):
                data['lastname'] = request.form.get('lastname')
            else:
                data['lastname'] = 'defaultlastname'

            if request.form.get('passw'):
                #implement hash here!
                data['passhash'] = request.form.get('passw')
            else:
                #implement hash here!
                data['passhash'] = 'defaultpass'

            msg = ''

            if self.avispamodel.admin_user_create(data):
                msg += ' already existed. '
            else:
                msg += ' just Created. '

            d = {'message': 'using install tool:'+msg , 'template':'avispa_rest/index.html'}


        else:  # Show form to formulate request

            d = {'message': 'Create_user tool RQ ', 'template':'avispa_rest/tool_create_user_rq.html'}

        return d


    def dropzonedemo(self,request,*args):

        d = {'message': 'using dropzone tool', 'template':'avispa_rest/tools/dropzonedemo.html'}

        return d





