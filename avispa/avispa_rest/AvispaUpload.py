# AvispaUpload.py
import os
import sys
import random
from werkzeug import secure_filename
from wand.image import Image 
from wand.display import display

class AvispaUpload:

    def __init__(self):

        self.UPLOAD_FOLDER = '/Users/ricardocid/Code/avispapics/'
        self.filename = ''

    def do_upload(self,request,*args):

        if not self._request_complete(request):
            return False

        if not self._request_allowed(request):
            return False         

        if self._upload_file(request):
            self._multi_size()
        else:
            return False
  
        return True

    def _request_complete(self,request):

        if not request.method == 'POST':
            print('Error: You can only use upload via POST')
            return False

        if not request.files['file']:
            print('Error: There are no files in the request')
            return False

        return True

    def _request_allowed(self,request):

        file = request.files['file']
        if not self.__allowed_file(file.filename):
            print('Error: This file is not allowed')
            return False

        return True


    def _upload_file(self,request):

        file = request.files['file']
        #filename = secure_filename(file.filename)
        self.imgid = str(random.randrange(1000,9999))
        filename = self.imgid+'_o.jpg'


        try:     
            file.save(os.path.join(self.UPLOAD_FOLDER, filename))
            print('File uploaded successfully here:' + os.path.join(self.UPLOAD_FOLDER, filename))
            self.uploaded_file = os.path.join(self.UPLOAD_FOLDER, filename)
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


    def _multi_size(self):

        with Image(filename=self.UPLOAD_FOLDER+self.imgid+'_o.jpg') as img:

            #newname = str(random.randrange(1000,9999))

            #print(img.size)
            for r in 1,2,3:
                with img.clone() as i:
                    i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
                    #i.rotate(90 * r)
                    i.save(filename=self.UPLOAD_FOLDER+self.imgid+'_{0}.jpg'.format(r))
                    #display(i)
                    print('File multiplied:'+self.UPLOAD_FOLDER+self.imgid+'_{0}.jpg'.format(r))
        
        return True

    def _rename(self,filename):

        filename.rsplit('.',1)[1]




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






    def __allowed_file(self,filename):

        ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','JPG','jpeg','gif'])

        return '.' in filename and \
                filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


