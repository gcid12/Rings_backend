# MyRingTool.py

import uuid
import random
import bcrypt
import json


from flask import flash, current_app

from MainModel import MainModel
from AvispaModel import AvispaModel

from auth.AuthModel import AuthModel

from AvispaUpload import AvispaUpload
from MyRingSchema import MyRingSchema
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)



class MyRingTool:

    def __init__(self):

        self.AVM = AvispaModel() 
        self.MAM = MainModel() 
        self.ATM = AuthModel()  
        self.user_database = 'myring_users'  

    def checkuno(self,request,*args):
        self.MAM.create_db('python-test39')    

    def install(self,request,*args):

        data = {}
        data['username'] = 'admin'
        data['email'] = 'admin@domain.com'
        data['lastname'] = 'admin last name'
        data['firstname'] = 'admin last name'
        data['passhash'] = 'adminpass'
        data['guid'] = 'adminguid'
        data['salt'] = 'adminsalt'


        #user = 'admin' #This is just the first user that is installed on a vanilla MyRing
        msg = ''
  
        if self.ATM.admin_user_db_create():
            msg += 'MyRing DB just Installed. '

        else:   
            msg += ' MyRing DB already exists. '
            if self.ATM.admin_user_create(data):
                msg += data['username'] + ' just Created. '
            else:
                msg += data['username'] + ' already existed. '

        # You need to create the image uploads folder as well. 


    	d = {'message': 'using install tool:'+msg , 'template':'avispa_rest/index.html'}
        return d


    def create_user(self,request,*args):

        

        if 'rs' in request.args:


            data = {}

            if request.form.get('username'):
                data['username'] = request.form.get('username')
            else:
                data['username'] = 'defaultusername'

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
                if request.form.get('passw') == request.form.get('passwrepeat'):
                    data['salt'] = self.generate_salt()
                    data['passhash'] = self.get_hashed_password(request.form.get('passw'),data['salt'])
                else:
                    print(request.form.get('passw'))
                    print(request.form.get('passwrepeat'))
                    raise ValueError('Both passwords need to be exactly the same')
            else:
                #implement hash here!
                raise ValueError('You need a password!')      

            data['guid'] = hex(uuid.getnode())


            msg = ''

            if self.ATM.admin_user_create(data):
                msg += ' just Created. '

                AUD = AvispaUpload(data['username'])
                AUD.create_user_imagefolder()
                
            else:
                msg += ' user already existed. '
                

            d = {'message': 'using install tool:'+msg , 'template':'avispa_rest/index.html'}


        else:  # Show form to formulate request

            d = {'message': 'Create_user tool RQ ', 'template':'avispa_rest/tools/create_user_rq.html'}

        return d

    def generate_salt(self):
        return bcrypt.gensalt(10) 
        # The integer is the number the dictates the 'slowness'
        #Slow is desirable because if a malicious party gets their hands on the table containing hashed passwords, 
        #then it is much more difficult to de-encrypt them. 

    def get_hashed_password(self,plain_text_password,salt):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password, salt)

    def check_password(self,plain_text_password, hashed_password):
        # Check hased password. Useing bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password, hashed_password)


    def dropzonedemo(self,request,*args):

        d = {'message': 'using dropzone tool', 'template':'avispa_rest/tools/dropzonedemo.html'}

        return d

    def wanddemo(self,request,*args):

        from wand.image import Image 
        from wand.display import display

        image_folder = ''

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


        UPLOAD_FOLDER = ''

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


        UPLOAD_FOLDER = ''
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

        #Check if the handle exists and the token is correct
        handle = request.args.get('handle')

        AUD = AvispaUpload(handle)

        blob = AUD.blob_from_request(request)
        response = AUD.do_upload(blob)
        response['handle'] = handle
        response['imgbase']= '/_images/{handle}/{sizename}/{imgid}_{sizename}.{extension}'

        print 'DATA:', repr(response)
        json_string = json.dumps(response)
        print 'JSON:', json_string

        
        
        if 'imgid' in response.keys():
            print(response)
            d = {'data_string':json_string, 
                 'imgid': response['imgid'], 
                 'imgsizes': response['imgsizes'] ,
                 'imgbase': response['imgsizes'] , 
                 'template':'avispa_rest/tools/uploadresponsejson.html'} 
            
        elif 'status' in response.keys():
            d = {'status':response['status'],
                 'template':'avispa_rest/tools/uploadresponsejson.html'}

        else:
            d = {'status':'500',
                 'template':'avispa_rest/tools/uploadresponsejson.html'}


        return d


    def delete_via_aud(self,request,*args):

        
        #Here is where you call the Avispa Uploader to delete an image in the image store

        #The document already unlinked this image. No references to it exist. It should be
        #queued for deletion or deleted instantly 

        #Not safe to implement until we secure the API

        # NOT IMPLEMENTED YET. 

        out = {'success':True,'message':'Queued for deletion'}
        d = {'template':'base_json.html','json_out':json.dumps(out)}

        return d


    def sync_couchdb_views(self,request,*args):
        '''
        Usage => http://127.0.0.1:8080/tool/sync_couchdb_views?dbringname=volatour_services_0-1-0
        '''

        db_ringname =  request.args.get('dbringname')

        self.AVM.ring_set_db_views(db_ringname)

        flash(u'Views synced to ring :'+db_ringname,'UI')
        rq='Loading the Views into CouchDB via python'

        d = {'rq': rq,'template':'avispa_rest/tools/flashresponsejson.html'}

        return d

    def run_view(self,request,*args):

        handle = 'volatour'
        ringname = 'services_0-1-0'
        startkey = '3468686347'
        resultsperpage = 3
        self.AVM.get_a_b(handle,ringname,resultsperpage,startkey)

        flash(u'ok')
        rq='run_view'

        d = {'rq': rq,'template':'avispa_rest/tools/flashresponsejson.html'}

        return d

    def update_gerardo(self,request,*args):

        self.ATM.userdb_set_db_views()

        flash(u'DB Views updated')

        rq = ''

        d = {'rq': rq,'template':'avispa_rest/tools/flashresponsejson.html'}

        return d

    def test_urllib2(self,request,*args):

        import requests

        print('in')
        r = requests.get('http://localhost:8080/_api/blalab2/reactivoexamen_0-1-2')
        #r = requests.get('http://yahoo.com')
        
        print('out')
        print(r)

        rq = r
        d = {'rq': r,'template':'avispa_rest/tools/flashresponsejson.html'}
        return d

    def test_request1(self,request,*args):

        import urlparse
        import requests

        o1 = urlparse.urlparse(request.url)
        host_url=urlparse.urlunparse((o1.scheme, o1.netloc, '', '', '', ''))
        print(host_url)

        ringurl = 'http://127.0.0.1:8080/_api/blalab/reactivoexamen_0-1-2?schema'
        o2 = urlparse.urlparse(ringurl)
        print('o2:')
        print(o2)
        #o2 = urlparse.urlparse(request.form.get('ringurl'))
        ring_url=urlparse.urlunparse((o2.scheme, o2.netloc, '', '', '', ''))
        print(ring_url)
        
        if host_url==ring_url:
            print('Cloning local ring')
            pathparts=o2.path.split('/')
            handle = pathparts[2]
            ringname = pathparts[3]
            schema = self.AVM.ring_get_schema_from_view(handle,ringname)
            print('Cloning local ring2')
            print(schema)
            #You are cloning a ring from your localhost
            rq = 'Cloning local ring'
            #Verificar si el request viene localmente. 
            #obtener el Schema (del Ring indicado)
            #tranformarlo para la generacion de un nuevo ring

        else:
            
        #else
           #Un call comun y corriente  

            print('Cloning non local ring')
            r = requests.get(request.form.get('ringurl'))
            #r = requests.get('http://localhost:8080/_api/blalab2/reactivoexamen_0-1-2')
            
            print(r.text)
            rq= r.text

        
        d = {'rq': rq,'template':'avispa_rest/tools/flashresponsejson.html'}
        return d


    def analyze_schema(self,request,*args):

        ring = MyRingSchema()

        print(MyRingSchema.fields['FieldName'])

        d = {'rq': 'ok','template':'avispa_rest/tools/flashresponsejson.html'}
        return d


    def analyze_url(self,request,*args):

        from urlparse import urlparse, urlunparse


        o2 = urlparse('http://127.0.0.1:8080/vito/juicio_0-1-0?schema222=23')
        print 'scheme  :', o2.scheme
        print 'netloc  :', o2.netloc
        print 'path    :', o2.path
        print 'params  :', o2.params
        print 'query   :', o2.query
        print 'fragment:', o2.fragment
        print 'username:', o2.username
        print 'password:', o2.password
        print 'hostname:', o2.hostname, '(netloc in lower case)'
        print 'port    :', o2.port

        pathparts = o2.path.split('/')
        print(pathparts)
        if pathparts[1]!='_api':
            corrected_path = '/_api'+o2.path
        else:
            corrected_path = o2.path

        corrected_query = 'schema'

        ring_url=urlunparse((o2.scheme, o2.netloc, corrected_path, '', corrected_query, ''))
        print('ring_url:')
        print(ring_url)


        d = {'rq': ring_url,'template':'avispa_rest/tools/flashresponsejson.html'}
        return d



    def template(self,request,*args):
        template = request.args.get('t')
        
        d = {'rq': current_user,'template':'avispa_rest/'+template+'.html'}
        return d





            





















