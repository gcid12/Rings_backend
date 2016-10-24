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
        
        self.rs_status = ''
        self.officialsizes = {'r100':100,'r240':240,'r320':320,'r500':500,'r640':640,'r800':800,'r1024':1024}
        self.thumbnailsizes = {'t75':75,'t150':150}
        self.allowed_formats = set(['txt','pdf','png','jpg','JPG','jpeg','gif'])

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})


    #DRIVER FUNCTION
    def do_upload(self,request,*args):

        response = {}
        image_sizes = []

        #Validate request
        if not self._request_complete(request):
            response['status']=self.rs_status
            return response

        #Pull file from request
        f = self._pull_file_from_request(request)

        #Check its name
        if not self._filename_extension_check(f.filename):
            response['status']=self.rs_status
            return response

        #Load the image blob
        print(f)
        f.seek(0)       
        image_binary = f.read()
        
        #Load the image
        with Image(blob=image_binary) as img:

            #Prepare image components       
            imgid = self._generate_imgid()
            filename = imgid+'.jpg'

            #Image analysis
            longside, shortside, orientation = self._img_orientation(img.width,img.height)

            #Constrain original if needed
            if longside > 2000:
                img = self._img_resize(img,2000,orientation)

            path = '%s/%s'%(self.handle,'o')
            self._s3_save(img,path,filename)
            m = self._generate_metadata(img.width,img.height,'o')
            image_sizes.append(m)

            #Save scaled down versions and thumbnail
            #Plan of action
            regular_wo,thumb_wo = self._image_workorder(longside,shortside)

            #Scaled down versions
            for wo in regular_wo:
                with img.clone() as i:
                    ii = self._img_resize(i,regular_wo[wo],orientation)
                    path = '%s/%s'%(self.handle,wo)
                    self._file_save(i,path,filename)
                    m = self._generate_metadata(ii.width,ii.height,wo)
                    image_sizes.append(m)



            #Thumbnail versions
            for wo in thumb_wo:
                with img.clone() as i:
                    ii = self._img_resize(i,thumb_wo[wo],orientation)
                    iii = self._img_thumbcrop(ii,orientation)
                    path = '%s/%s'%(self.handle,wo)
                    self._file_save(i,path,filename)
                    m = self._generate_metadata(iii.width,iii.height,wo)
                    image_sizes.append(m)


        response['status']=self.rs_status
        response['imgid']=imgid
        response['imgsizes']=image_sizes

        return response

    def do_copy(self,from_handle,to_handle,imgid):

        pass

        return response

    def _generate_metadata(self,width,height,sizename):

        multiplied={}
        multiplied['mime-type']='image/jpeg'
        multiplied['extension']='jpg'
        multiplied['width']=width
        multiplied['height']=height
        multiplied['sizename']=sizename
        multiplied['unit']='pixel'
        #self.lggr.debug(multiplied)

        return multiplied

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

    def _filename_extension_check(self,filename):

        #TO-DO This a very soft check. Please implement Real Format Check
  
        if not '.' in filename and filename.rsplit('.',1)[1] in self.allowed_formats:       
            self.lggr.error('Error: This file format is not allowed: '+str(filename))
            flash(u'This file format is not allowed: '+str(filename),'ER')
            self.rs_status='415'
            return False

        return True


    def _pull_file_from_request(self,request):

        try:
            f = request.files['file']
        except:
            self.lggr.debug("Unexpected error:"+str(sys.exc_info()[0]))
            flash(u'Unexpected error:'+str(sys.exc_info()[0]),'ER')
            self.rs_status='500'
            raise

        return f
        

    def _pull_file_from_s3(self,handle,imgid):

        pass

        #1. Subtract image from S3

        #2. Put it in self.f

    def _generate_imgid(self):
 
        return str(random.randrange(1000000000,9999999999))


    def _image_workorder(self,longside,shortside):

        regular_wo = {}
        thumb_wo = {}

        for r in self.officialsizes:
            if longside>=self.officialsizes[r]:
                regular_wo[r] = self.officialsizes[r]

        for t in self.thumbnailsizes:
            if shortside>=self.thumbnailsizes[t]:
                thumb_wo[t] = self.thumbnailsizes[t]

        return (regular_wo,thumb_wo)


    

    def _img_orientation(self,width,height):
        
        if width > height:
            
            longside = width
            shortside = height
            orientation = "landscape"

        if width < height:

            longside = height
            shortside = width
            orientation = "portrait"
            
        if width == height:
            
            longside = height
            shortside = width
            orientation = "square"

        return longside, shortside, orientation


    def _img_resize(self,img,mainside,orientation):

        if orientation=='portrait':
            img.transform(resize='x'+str(mainside)) #Height based
            #img.resize(height=int(mainside))
        elif orientation=='landscape':
            img.transform(resize=str(mainside)) #Width based
            #img.resize(width=int(mainside))
            #img.transform(resize=str(mainside)) 
        elif orientation=='square':
            img.transform(resize=str(mainside)) #Width based
            #img.resize(width=int(mainside))

        return img


    def _img_thumbcrop(self,img,orientation):
        offset = abs(img.width-img.height)/2  #This centers the crop
        if orientation=='portrait':
            img.crop(0,offset,width=img.width,height=img.width) 
        if orientation=='landscape':
            img.crop(offset,0,width=img.height,height=img.height)

        return img

    #DEPRECATED
    def _file_save(self,file,path,filename):
      
        if STORE_MODE == 'LOCAL':
            self.lggr.info("Storing image in LOCAL: %s/%s"%(path,filename))
            file.save(filename=('%s/%s/%s'%(IMAGE_FOLDER_NAME,path,filename)))          
        elif STORE_MODE == 'S3':
            self.lggr.info("Storing image in S3: %s/%s"%(path,filename))
            self._s3_save(file,path,filename)

    def _local_save(self,file,path,filename):
        self.lggr.info("Storing image in LOCAL: %s/%s"%(path,filename))
        file.save(filename=('%s/%s/%s'%(IMAGE_FOLDER_NAME,path,filename)))

    def _s3_save(self,file,path,filename):

        conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(IMAGE_BUCKET_NAME)       
        #k = Key(bucket)
        k = boto.s3.key.Key(bucket)
        k.key = '%s/%s'%(path,filename)
        print(k)
        print(k.key)
        print(file)

        fl = cStringIO.StringIO()
        file.save(fl)

        #print fl
        fl.seek(0)


        
        k.set_contents_from_file(fl)
        k.set_acl('public-read')
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



