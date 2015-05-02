# AvispaUpload.py
import os
import sys
import errno
import random
import werkzeug 
from werkzeug import secure_filename
from flask import flash
from wand.image import Image 
from wand.display import display

from default_config import IMAGE_STORE
from env_config import IMAGE_STORE


class AvispaUpload:

    def __init__(self,handle):

        self.IMAGE_FOLDER = IMAGE_STORE+'/'+handle
        self.filename = ''
        self.rs_status = ''
        self.image_sizes = []

        self.officialsizes = {'r100':100,'r240':240,'r320':320,'r500':500,'r640':640,'r800':800,'r1024':1024}
        self.thumbnailsizes = {'t75':75,'t150':150}

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
            print('Error: You can only use upload via POST')
            flash(u'You can only use upload via POST','ER')
            self.rs_status='405'
            return False

        if not request.files['file']:
            print('Error: There are no files in the request')
            flash(u'There are no files in the request','ER')
            self.rs_status='400'
            return False

        return True

    def _request_allowed(self,request):

        file = request.files['file']
        if not self.__allowed_file(file.filename):
            print('Error: This file is not allowed: '+str(file.filename))
            flash(u'This file is not allowed: '+str(file.filename),'ER')
            self.rs_status='415'
            return False

        return True


    def _upload_file(self,request):

        file = request.files['file']
        #filename = secure_filename(file.filename)
        self.imgid = str(random.randrange(1000000000,9999999999))
        filename = self.imgid+'_o.jpg'
        originalversionpath = self.IMAGE_FOLDER + '/o/'


        try:     
            file.save(os.path.join(originalversionpath, filename))
            print('File uploaded successfully here:' + os.path.join(self.IMAGE_FOLDER, filename))
            self.uploaded_file = os.path.join(self.IMAGE_FOLDER, filename)
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            flash(u'Unexpected error:'+str(sys.exc_info()[0]),'ER')
            self.rs_status='500'
            raise


    def _multi_size(self):

        with Image(filename=self.IMAGE_FOLDER+'/o/'+self.imgid+'_o.jpg') as img:

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
            print(multiplied)
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
            

        

        try:     
            img.save(filename=self.IMAGE_FOLDER+'/'+sizename+'/'+self.imgid+'_'+sizename+'.jpg')
            print('File multiplied successfully here:' + self.IMAGE_FOLDER+'/'+sizename+'/'+self.imgid+'_'+sizename+'.jpg')
            multiplied={}
            multiplied['mime-type']='image/jpeg'
            multiplied['extension']='jpg'
            multiplied['width']=img.width
            multiplied['height']=img.height
            multiplied['sizename']=sizename
            multiplied['unit']='pixel'
            print(multiplied)
            self.image_sizes.append(multiplied)
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            flash(u'Unexpected error:'+str(sys.exc_info()[0]),'ER')
            self.rs_status='500'
            raise


        


    def __allowed_file(self,filename):

        ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','JPG','jpeg','gif'])

        return '.' in filename and \
                filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS



    def x_create_user_imagefolder(self): #DONT USE HERE! #Moved to AuthModel.py

        
        self.safe_create_dir(self.IMAGE_FOLDER+'/o') #Original folder

        for r in self.officialsizes:
            self.safe_create_dir(self.IMAGE_FOLDER+'/'+r)  # Scale-down version folders


        for t in self.thumbnailsizes:
            self.safe_create_dir(self.IMAGE_FOLDER+'/'+t)  # Thumbnail folders

        return True

    

    def x_safe_create_dir(self,path): #DONT USE HERE! #Moved to AuthModel.py
        print(path)
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        print('flag1')
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



