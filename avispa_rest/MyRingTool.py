# MyRingTool.py

import uuid
import random
import bcrypt
import json

from flask import flash, current_app
from MainModel import MainModel
from TypesModel import TypesModel
from auth.AuthModel import AuthModel
from Upload import Upload
from MyRingSchema import MyRingSchema
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)


class MyRingTool:

    def __init__(self):

        self.TYM = TypesModel() 
        self.MAM = MainModel() 
        self.ATM = AuthModel()  
        self.user_database = 'myring_users'  

    #BOOTSTRAP INSTALLATION
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


    #IMAGE SERVER
    def assert_rq_method(self,request,method):

        if not request.method == method:

            self.lggr.error('Error: You can only use upload via POST')
            flash(u'You can only use upload via POST','ER')
            self.rs_status='405'
            return False

        if not request.files['file']:
            self.lggr.error('Error: There are no files in the request')
            flash(u'There are no files in the request','ER')
            self.rs_status='400'
            return False

        return True
    
    #IMAGE SERVER
    def pull_file_from_request(self,request):

        try:
            f = request.files['file']
        except:
            self.lggr.debug("Unexpected error:"+str(sys.exc_info()[0]))
            flash(u'Unexpected error:'+str(sys.exc_info()[0]),'ER')
            self.rs_status='500'
            raise

        return f
    
    #IMAGE SERVER UPLOAD DRIVER
    def upload_via_aud(self,request,*args):

        #Check if the handle exists and the token is correct
        handle = request.args.get('handle')

        #Validate that method is POST
        if not self.assert_rq_method(request,'POST'):
            response['status']=self.rs_status
            return response

        f = self.pull_file_from_request(request)

        UPL = Upload(handle)

        if not UPL.check_extension(f.filename):
            return False

        blob = UPL.blob_from_file(f)

        response = UPL.do_upload(blob)
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

    #IMAGE SERVER DELETE DRIVER
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

        self.TYM.ring_set_db_views(db_ringname)

        flash(u'Views synced to ring :'+db_ringname,'UI')
        rq='Loading the Views into CouchDB via python'

        d = {'rq': rq,'template':'avispa_rest/tools/flashresponsejson.html'}

        return d

    def run_view(self,request,*args):

        handle = 'volatour'
        ringname = 'services_0-1-0'
        startkey = '3468686347'
        resultsperpage = 3
        self.TYM.get_a_b(handle,ringname,resultsperpage,startkey)

        flash(u'ok')
        rq='run_view'

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
            schema = self.TYM.ring_get_schema_from_view(handle,ringname)
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
