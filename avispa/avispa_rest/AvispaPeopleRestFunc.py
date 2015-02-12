# AvispaCollectionsRestFunc.py
from flask import redirect, flash
from AvispaModel import AvispaModel
from MainModel import MainModel
from AvispaPeopleModel import AvispaPeopleModel


class AvispaPeopleRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()
        self.MAM = MainModel()
        self.APM = AvispaPeopleModel()
        

    # GET/a
    def get_a_p(self,request,handle,person,*args):

        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams: 
            #This is an organization         
            d['peoplelist'] = peopleteams['people'] 
            d['peoplelistlen'] = len(peopleteams['people'])
            
            for person in peopleteams['people']:
                #get the profilepic for this person
                person_user_doc = self.MAM.select_user_doc_view('auth/userbasic',person['handle'])
                if person_user_doc:
                    person['thumbnail'] = person_user_doc['profilepic']

                    #d['peoplethumbnails'][person['handle']] = person_user_doc['profilepic']

            
            d['template'] = 'avispa_rest/get_a_p.html'
        else:
            #This is a regular user
         
            d['redirect'] = '/'+handle+'/_home'
     
        return d


        # POST/a
    def post_a_p(self,request,handle,person,*args):

        #We need to recover from request as it doesn't come via URL
        person = request.form.get('newperson')

        #Check if the user exists or not
        if self.MAM.user_exists(person):

            result = self.APM.post_a_p(handle,person)
                
            if result:
                print('Awesome , you just added '+ person +' to the organization')
                #msg = 'Item put with id: '+idx
                flash('Awesome , you just added '+ person +' to the organization')

            else:
                flash('There was an error adding '+ person +' to the organization.')

        else:
            flash(person+' is not a MyRing user. Please create it first.')


        
        redirect = '/'+handle+'/_people'
        d = {'redirect': redirect, 'status':200}
        return d


        #DELETE /a/b
    def delete_a_p_q(self,request,handle,person,*args):
        #Will delete an existing person
        print('Trying to delete the following person: '+person)

        #Check if the user exists or not
        if self.MAM.user_exists(person):

            result = self.APM.delete_a_p_q(handle,person)
                
            if result:
                print('You just deleted '+ person +' from the organization')
                #msg = 'Item put with id: '+idx
                flash('You just deleted '+ person +' from the organization')

            else:
                flash('There was an error deleting '+ person +' from the organization.')

        else:
            flash(person+' is not a MyRing user.')


        
        redirect = '/'+handle+'/_people'
        d = {'redirect': redirect, 'status':200}
        return d




 