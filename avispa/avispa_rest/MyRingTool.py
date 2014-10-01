# MyRingTool.py

from flask import flash
from AvispaModel import AvispaModel
from AvispaUpload import AvispaUpload


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


        # You need to create the image uploads folder as well. 


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

    def wanddemo(self,request,*args):

        from wand.image import Image 
        from wand.display import display

        image_folder = '/Users/ricardocid/Code/avispa/imagestest/'

        with Image(filename=image_folder+'cover1b.png') as img:
            print(img.size)
            for r in 1,2,3:
                with img.clone() as i:
                    i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
                    i.rotate(90 * r)
                    i.save(filename=image_folder+'cover1b-{0}.png'.format(r))
                    display(i)


    def fileupload(self,request,*args):

        import os
        from werkzeug import secure_filename


        UPLOAD_FOLDER = '/Users/ricardocid/Code/avispapics/'

        if request.method == 'POST':
            file = request.files['file']
            if file and self.__allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                out = 'File uploaded successfully here:' + os.path.join(UPLOAD_FOLDER, filename)
            else:
                out = 'Format not allowed'
        else:
            out = 'Upload something'
        
        

        d = {'out': out , 'template':'avispa_rest/tools/uploadfiledemo.html'} 
        return d 


    def __allowed_file(self,filename):

        ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','JPG','jpeg','gif'])

        return '.' in filename and \
                filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


    def uploadmultiply(self,request,*args):

        import os
        from werkzeug import secure_filename
        from wand.image import Image 
        from wand.display import display


        UPLOAD_FOLDER = '/Users/ricardocid/Code/avispapics/'
        out = ''

        if request.method == 'POST':
            file = request.files['file']
            if file and self.__allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))

                print('File uploaded here:' + os.path.join(UPLOAD_FOLDER, filename))
         

                with Image(filename=os.path.join(UPLOAD_FOLDER, filename)) as img:
                    print(img.size)
                    for r in 1,2,3:
                        with img.clone() as i:
                            #i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
                            i.transform(resize=str(100 * r))
                            #i.rotate(90 * r)
                            i.save(filename=UPLOAD_FOLDER+filename+'{0}.jpg'.format(r))
                            #display(i)
                            print('File multiplied:'+UPLOAD_FOLDER+filename+'{0}.jpg'.format(r))



                out = 'File uploaded'


            else:
                out = 'Format not allowed'
        else:
            out = 'Upload something'

        d = {'out': out , 'template':'avispa_rest/tools/uploadfiledemo.html'} 
        return d 


    def upload_via_aud(self,request,*args):

        AUD = AvispaUpload()

        response = AUD.do_upload(request)
        imgbase = '/images/'
        
        if 'imgid' in response.keys():
            d = {'imgid': response['imgid'], 'imgbase': imgbase , 'template':'avispa_rest/tools/uploadresponsejson.html'} 
            
        elif 'error_status' in response.keys():
            d = {'error_status':response['error_status'],'template':'avispa_rest/tools/uploadresponsejson.html'}

        else:
            d = {'error_status':'500','template':'avispa_rest/tools/uploadresponsejson.html'}


        return d


    def delete_via_aud(self,request,*args):

        rq = 'DELETE image/'+request.args.get('id')
        flash(u'Succesfully deleted','message')

        d = {'rq': rq,'template':'avispa_rest/tools/flashresponsejson.html'}

        return d


















