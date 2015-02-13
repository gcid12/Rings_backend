# AvispaCollectionsRestFunc.py
from flask import redirect, flash
from AvispaModel import AvispaModel
from MainModel import MainModel
from flask.ext.login import current_user


class AvispaTeamsRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()
        self.MAM = MainModel()
        
        

    # GET/a
    def get_a_m(self,request,handle,team,*args):

        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams: 
            #This is an organization         
            
            d['teamlistlen'] = len(peopleteams['teams'])
            
            for team in peopleteams['teams']:
                #get the profilepic for this person
                for member in team['members']:
                    person_user_doc = self.MAM.select_user_doc_view('auth/userbasic',member['handle'])
                    if person_user_doc:
                        member['thumbnail'] = person_user_doc['profilepic']

                    #d['peoplethumbnails'][person['handle']] = person_user_doc['profilepic']

            d['teamlist'] = peopleteams['teams']            
            d['template'] = 'avispa_rest/get_a_m.html'
        else:
            #This is a regular user
         
            d['redirect'] = '/'+handle+'/_home'
     
        return d


        # POST/a
    def post_a_m(self,request,handle,team,*args):

        #We need to recover from request as it doesn't come via URL
        team = request.form.get('newteam')

        #Check if the team exists or not
        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams: 
            #This is an organization                  
            for teamd in peopleteams['teams']:
                
                if teamd['teamname'] == team:
                    #This team exists in this handle!
                    flash('This team exists already. Use a different name')
                    redirect = '/'+handle+'/_teams' 
                    d = {'redirect': redirect, 'status':200}
                    return d 

            if self.MAM.add_team(handle,team,current_user.id):
                print('Awesome , you just created team '+ team +'.')
                #msg = 'Item put with id: '+idx
                flash('Awesome , you just created team '+ team +'.')
                redirect = '/'+handle+'/_teams'
            else:
                flash('There was an error adding team: '+ team +'.')
                redirect = '/'+handle+'/_teams'

        else:
            #This is not an organization 
            redirect = '/'+current_user.id        

        d = {'redirect': redirect, 'status':200}
        return d


    def get_a_m_n(self,request,handle,team,*args):

        d = {}

        rings = self.MAM.select_user_doc_view('rings/count',handle)
        d['rings'] = rings

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams:   
            
            d['people'] = peopleteams['people']        
            
            for teamd in peopleteams['teams']:
                #get the profilepic for this person

                if teamd['teamname'] == team :

                    for member in teamd['members']:
                        person_user_doc = self.MAM.select_user_doc_view('auth/userbasic',member['handle'])
                        if person_user_doc:
                            member['thumbnail'] = person_user_doc['profilepic']

                    d['team'] = teamd
                    break

                      
            d['template'] = 'avispa_rest/get_a_m_n.html'
        else:
            #This is a regular user
         
            d['redirect'] = '/'+handle+'/_home'
     
        return d



        #DELETE /a/b
    def delete_a_m_n(self,request,handle,team,*args):
        #Will delete an existing person
        print('Trying to delete the following team: '+team)

        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams: 
            #This is an organization  

            for teamd in peopleteams['teams']:
                
                if teamd['teamname'] == team:
                    
                    if self.MAM.delete_team(handle,team):
                        print('You just deleted team '+ team +'.')
                        #msg = 'Item put with id: '+idx
                        flash('You just deleted team '+ team +'.')
                        redirect = '/'+handle+'/_teams'
                    else:
                        flash('There was an error deleting team: '+ team +'.')
                        redirect = '/'+handle+'/_teams'

        else:
            #This is not an organization 
            redirect = '/'+current_user.id        

        d = {'redirect': redirect, 'status':200}
        return d



 