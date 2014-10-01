# AvispaUpload.py
import os
import sys
import random
from werkzeug import secure_filename
from flask import flash
from wand.image import Image 
from wand.display import display

class AvispaUpload:

    def __init__(self):

        self.UPLOAD_FOLDER = '/Users/ricardocid/Code/avispapics/'
        self.filename = ''
        self.rs_status = ''
        self.image_sizes = []

    def do_upload(self,request,*args):

        response={}

        if not self._request_complete(request):
            response['error_status']=self.rs_status
            return response

        if not self._request_allowed(request):
            response['error_status']=self.rs_status
            return response

        if self._upload_file(request):
            self._multi_size()
            response['imgid']=self.imgid
            response['imgsizes']=self.image_sizes
        else:
            response['error_status']=self.rs_status

        return response
            
  
        

    def _request_complete(self,request):

        if not request.method == 'POST':
            print('Error: You can only use upload via POST')
            flash(u'You can only use upload via POST','error')
            self.rs_status='405'
            return False

        if not request.files['file']:
            print('Error: There are no files in the request')
            flash(u'There are no files in the request','error')
            self.rs_status='400'
            return False

        return True

    def _request_allowed(self,request):

        file = request.files['file']
        if not self.__allowed_file(file.filename):
            print('Error: This file is not allowed: '+str(file.filename))
            flash(u'This file is not allowed: '+str(file.filename),'error')
            self.rs_status='415'
            return False

        return True


    def _upload_file(self,request):

        file = request.files['file']
        #filename = secure_filename(file.filename)
        self.imgid = str(random.randrange(1000,9999))
        filename = self.imgid+'_o.jpg'
        originalversionpath = self.UPLOAD_FOLDER + 'o/'


        try:     
            file.save(os.path.join(originalversionpath, filename))
            print('File uploaded successfully here:' + os.path.join(self.UPLOAD_FOLDER, filename))
            self.uploaded_file = os.path.join(self.UPLOAD_FOLDER, filename)
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            flash(u'Unexpected error:'+str(sys.exc_info()[0]),'error')
            self.rs_status='500'
            raise


    def _multi_size(self):

        with Image(filename=self.UPLOAD_FOLDER+'o/'+self.imgid+'_o.jpg') as img:

            orientation = self._img_orientation(img)
            if orientation == 'portrait' or orientation == 'square':
                longside = img.height
                shortside = img.width
            elif orientation == 'landscape':
                longside = img.width
                shortside = img.height

            officialsizes = {'r100':100,'r240':240,'r320':320,'r500':500,'r640':640,'r800':800,'r1024':1024}

            for r in officialsizes:
                with img.clone() as i:
                    if longside>=officialsizes[r]:
                        self._img_resize_and_save(i,officialsizes[r],r,orientation)

            multiplied={}
            multiplied['mimetype']='image/jpeg'
            multiplied['width']=str(img.width)
            multiplied['height']=str(img.height)
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

    def _img_resize_and_save(self,img,mainside,sizename,orientation):

        if(orientation=='portrait'):
            img.transform(resize='x'+str(mainside))
        elif(orientation=='landscape'):
            img.transform(resize=str(mainside))
        elif(orientation=='square'):
            img.transform(crop=str(mainside))

        

        try:     
            img.save(filename=self.UPLOAD_FOLDER+sizename+'/'+self.imgid+'_'+sizename+'.jpg')
            print('File multiplied successfully here:' + self.UPLOAD_FOLDER+sizename+'/'+self.imgid+'_'+sizename+'.jpg')
            multiplied={}
            multiplied['mimetype']='image/jpeg'
            multiplied['width']=str(img.width)
            multiplied['height']=str(img.height)
            multiplied['sizename']=sizename
            multiplied['unit']='pixel'
            print(multiplied)
            self.image_sizes.append(multiplied)
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            flash(u'Unexpected error:'+str(sys.exc_info()[0]),'error')
            self.rs_status='500'
            raise


        


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



