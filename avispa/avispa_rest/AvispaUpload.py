# AvispaUpload.py
import os
import sys
import errno
import random
import werkzeug 
import logging
import cStringIO



from werkzeug import secure_filename
from flask import flash, g
from wand.image import Image 
from wand.display import display

from env_config import IMAGE_FOLDER_NAME, STORE_MODE

if STORE_MODE == 'S3':
    import boto
    from boto.s3.key import Key
    from env_config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, IMAGE_BUCKET_NAME


from AvispaLogging import AvispaLoggerAdapter


class AvispaUpload:

    def __init__(self,handle):

        self.handle = handle
        self.filename = ''
        self.rs_status = ''
        self.image_sizes = []

        self.officialsizes = {'r100':100,'r240':240,'r320':320,'r500':500,'r640':640,'r800':800,'r1024':1024}
        self.thumbnailsizes = {'t75':75,'t150':150}

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})


    def do_upload(self,request,*args):

        response={}

        if not self._request_complete(request):
            response['status']=self.rs_status
            return response

        if not self._request_allowed(request):
            response['status']=self.rs_status
            return response

        if self._upload_file(request):
            self._multi_size()
            response['imgid']=self.imgid
            response['imgsizes']=self.image_sizes
        else:
            response['status']=self.rs_status

        return response
            
  
        

    def _request_complete(self,request):

        if not request.method == 'POST':

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

    def _request_allowed(self,request):

        file = request.files['file']
        if not self.__allowed_file(file.filename):
            self.lggr.error('Error: This file is not allowed: '+str(file.filename))
            flash(u'This file is not allowed: '+str(file.filename),'ER')
            self.rs_status='415'
            return False

        return True


    def _upload_file(self,request):

        self.f = request.files['file']
        path = '%s/%s'%(self.handle,'o')
        self.imgid = str(random.randrange(1000000000,9999999999)) 
        filename = self.imgid+'.jpg'
        
        self.lggr.debug('path:%s'%path)
        self.lggr.debug('filename:%s'%filename)

        try:
            # OLD : file.save(os.path.join(originalversionpath, filename)) 
            self._file_save(self.f,path,filename)
            self.lggr.debug('Original File uploaded successfully')
            
            return True
        except:
            self.lggr.debug("Unexpected error:"+str(sys.exc_info()[0]))
            flash(u'Unexpected error:'+str(sys.exc_info()[0]),'ER')
            self.rs_status='500'
            raise


    def _multi_size(self):

        #### REFACTOR TO CALL S3 or LOCAL depeding on config

        

        #f = request.files['file']
        print('FILE')
        print(self.f)
        self.f.seek(0)
        
        image_binary = self.f.read()

        #with open(self.f) as f:
         #   image_binary = f.read()

        print('IMAGE_BINARY:')
        print(image_binary)

        # OLD with Image(filename=self.IMAGE_FOLDER+'/o/'+self.imgid+'.jpg') as img:
        with Image(blob=image_binary) as img:

            orientation = self._img_orientation(img)
            if orientation == 'portrait' or orientation == 'square':
                longside = img.height
                shortside = img.width
            elif orientation == 'landscape':
                longside = img.width
                shortside = img.height

            for r in self.officialsizes:
                with img.clone() as i:
                    if longside>=self.officialsizes[r]:
                        self._img_resize_and_save(i,self.officialsizes[r],r,orientation,False)

            for t in self.thumbnailsizes:
                with img.clone() as j:
                    if shortside>=self.thumbnailsizes[t]:
                        self._img_resize_and_save(j,self.thumbnailsizes[t],t,orientation,True)

            multiplied={}
            multiplied['mime-type']='image/jpeg'
            multiplied['extension']='jpg'
            multiplied['width']=img.width
            multiplied['height']=img.height
            multiplied['sizename']='o'
            multiplied['unit']='pixel'
            self.lggr.debug(multiplied)
            self.image_sizes.append(multiplied)

        
        return True

    def _img_orientation(self,img):
        
        if img.width > img.height:
            return 'landscape'
        if img.width < img.height:
            return 'portrait'
        if img.width == img.height:
            return 'square'

    def _img_resize_and_save(self,img,mainside,sizename,orientation,thumbnail):

        if thumbnail:

            if orientation=='portrait':
                img.transform(resize=str(mainside))
            elif orientation=='landscape':
                img.transform(resize='x'+str(mainside))
            elif orientation=='square':
                img.transform(resize=str(mainside))


            offset = abs(img.width-img.height)/2  #This centers the crop
            if orientation=='portrait':
                img.crop(0,offset,width=img.width,height=img.width) 
            if orientation=='landscape':
                img.crop(offset,0,width=img.height,height=img.height)

        else:

            if orientation=='portrait':
                img.transform(resize='x'+str(mainside))
            elif orientation=='landscape':
                img.transform(resize=str(mainside))
            elif orientation=='square':
                img.transform(resize=str(mainside))
            

        path = '%s/%s'%(self.handle,sizename)
        filename = self.imgid+'_'+sizename+'.jpg'

        self.lggr.debug('path:%s'%path)
        self.lggr.debug('filename:%s'%filename)


        try:     
            #OLD VERSION: img.save(filename=self.IMAGE_FOLDER+'/'+sizename+'/'+self.imgid+'_'+sizename+'.jpg')  
            self._file_save(img,path,filename)
            self.lggr.debug('File multiplied successfully ')
            multiplied={}
            multiplied['mime-type']='image/jpeg'
            multiplied['extension']='jpg'
            multiplied['width']=img.width
            multiplied['height']=img.height
            multiplied['sizename']=sizename
            multiplied['unit']='pixel'
            self.lggr.debug(multiplied)
            self.image_sizes.append(multiplied)
            return True
        except:
            self.lggr.debug("Unexpected error:"+str(sys.exc_info()[0]))
            flash(u'Unexpected error:'+str(sys.exc_info()[0]),'ER')
            self.rs_status='500'
            raise

    def _file_save(self,file,path,filename):
      
        if STORE_MODE == 'LOCAL':
            self.lggr.info("Storing image in LOCAL: %s/%s"%(path,filename))
            file.save(filename=('%s/%s/%s'%(IMAGE_FOLDER_NAME,path,filename)))          
        elif STORE_MODE == 'S3':
            self.lggr.info("Storing image in S3: %s/%s"%(path,filename))
            self._s3_save(file,path,filename)

    def _s3_save(self,f,path,filename):

        conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(IMAGE_BUCKET_NAME)       
        #k = Key(bucket)
        k = boto.s3.key.Key(bucket)
        k.key = '%s/%s'%(path,filename)
        print(k)
        print(k.key)
        print(f)

        fl = cStringIO.StringIO()
        f.save(fl)

        #print fl
        fl.seek(0)


        
        k.set_contents_from_file(fl)
        #AttributeError: 'Image' object has no attribute 'tell'
        
        
        
        #b = fl.read()
        #print(b)
        #k.set_contents_from_string(b)
        '''
        File "/Users/ricardocid/Code/avispa/avispa/avispa_rest/AvispaUpload.py", line 257, in _s3_save
        k.set_contents_from_string(f.read())
        File "/usr/local/lib/python2.7/site-packages/boto/s3/key.py", line 1422, in set_contents_from_string
        string_data = string_data.encode("utf-8")
        AttributeError: 'NoneType' object has no attribute 'encode'
        '''
        
        return True

    def __allowed_file(self,filename):

        ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','JPG','jpeg','gif'])

        return '.' in filename and \
                filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS




    
    def check_upload_path(self,path):
        pass

    def check_filename(self):
        pass

    def set_max_filesize(self):
        pass

    def set_max_filename(self):
        pass

    def set_max_width(self):
        pass

    def set_max_height(self):
        pass

    def set_allowed_types(self,types):
        pass

    def set_image_properties(self):
        pass

    def set_xss_clean(self):
        pass

    def is_image(self):
        pass

    def is_allowed_filetype(self):
        pass

    def is_allowed_filesize(self):
        pass

    def is_allowed_dimensions(self):
        pass

    def validate_upload_path(self):
        pass

    def get_extension(self,filename):
        pass

    def clean_file_name(self,filename):
        pass

    def limit_filename_length(self,filename,length):
        pass

    def do_xss_clean(self):
        pass

    def set_error(self,msg):
        pass

    def display_errors(self):
        pass

    def mime_types(self,mime):
        pass

    def _prep_filename(self,filename):
        pass

    def _file_mime_type(self,file):
        pass



