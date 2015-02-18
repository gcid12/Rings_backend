# AvispaCollectionsRestFunc.py
from flask import redirect, flash
from AvispaModel import AvispaModel
from MainModel import MainModel
from flask.ext.login import current_user
from AvispaTeamsModel import AvispaTeamsModel


class AvispaTeamsRestFunc:

    def __init__(self):
        self.AVM = AvispaModel()
        self.MAM = MainModel()
        self.ATM = AvispaTeamsModel()
        
        

    # GET/a
    def get_a_m(self,request,handle,team,*args):

        d = {}

        print('flag232x')

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams: 
            #This is an organization         
            
            d['teamlistlen'] = len(peopleteams['teams'])
            d['teammembership'] = {}
            d['nonteammembership'] = {}
            
            for teamd in peopleteams['teams']:
                #get the profilepic for this person
                for member in teamd['members']:

                    print('flag666x')

                    person_user_doc = self.MAM.select_user_doc_view('auth/userbasic',member['handle'])
                    if person_user_doc:
                        member['thumbnail'] = person_user_doc['profilepic']

                    if current_user.id == member['handle']:
                        d['teammembership'][teamd['teamname']] = teamd['roles'][-1]['role']
                    else:
                        d['nonteammembership'][teamd['teamname']] = teamd['roles'][-1]['role']







            
           
                    #d['peoplethumbnails'][person['handle']] = person_user_doc['profilepic']

            d['teamlist'] = peopleteams['teams']            
            d['template'] = 'avispa_rest/get_a_m.html'
        else:
            #This is a regular user
         
            d['redirect'] = '/'+handle+'/_home'
     
        return d


        # POST/a
    def post_a_m(self,request,handle,team,*args):
        '''
        Creates a new team
        '''
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

                    if teamd['roles']:

                        if teamd['roles'][-1]['role'] == 'team_admin':
                            teamauth = 'RWX'
                        elif teamd['roles'][-1]['role'] == 'team_writer':
                            teamauth = 'RW'
                        elif teamd['roles'][-1]['role'] == 'team_reader':
                            teamauth = 'R'
                        else:
                                teamauth = ''

                        teamd['teamauth'] = teamauth


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

    def put_a_m_n(self,request,handle,team,*args):

        #This function should be refactored into multiple functions that obey RESTFUL:
        # post_a_m_n_members , delete_a_m_n_members , post_a_m_n_rings, delete_a_m_n_rings

        d = {}

        if 'newmember' in request.form: 
            member = request.form.get('newmember')
            if self.ATM.post_a_m_n_members(handle,team,member):
                print(member + ' has been added to the team.')
                flash(member + ' has been added to the team.')
            else:
                print(member + ' is already part of this team.')
                flash(member + ' is already part of this team.')

        if 'delmember' in request.args: 
            member = request.args.get('delmember')
            if self.ATM.delete_a_m_n_members(handle,team,member):
                print(member + ' has been deleted from the team.')
                flash(member + ' has been deleted from the team.')
            else:
                print('There was an issue deleting: ' + member + '.')
                flash('There was an issue deleting: ' + member + '.')
            
        if 'newring' in request.form:
            ring = request.form.get('newring')
            if self.ATM.post_a_m_n_rings(handle,team,ring):
                print(ring + ' has been added to the team.')
                flash(ring + ' has been added to the team.')
            else:
                print(ring + ' already  exists in this team.')
                flash(ring + ' already  exists in this team.')           

        if 'delring' in request.args:
            ring = request.args.get('delring')
            if self.ATM.delete_a_m_n_rings(handle,team,ring):
                print(ring + ' has been deleted from the team.')
                flash(ring + ' has been deleted from the team.')
            else:
                print('There was an issue deleting: ' + ring + '.')
                flash('There was an issue deleting: ' + ring + '.')
            
            
        d['redirect'] = '/'+handle+'/_teams/'+team

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

    def get_a_m_n_settings(self,request,handle,team,*args):

        redirect = '/'+handle+'/_teams/'+team        

        d = {'redirect': redirect, 'status':200}
        return d


    def put_rq_a_m_n_settings(self,request,handle,team,*args):
        
        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams:   
            
            d['people'] = peopleteams['people']        
            
            for teamd in peopleteams['teams']:
                #get the profilepic for this person

                if teamd['teamname'] == team :

                    if teamd['roles']:
                        if teamd['roles'][-1]['role'] == 'team_admin':
                            teamauth = 'RWX'
                        elif teamd['roles'][-1]['role'] == 'team_writer':
                            teamauth = 'RW'
                        elif teamd['roles'][-1]['role'] == 'team_reader':
                            teamauth = 'R'
                        else:
                                teamauth = ''

                        teamd['teamauth'] = teamauth

                    d['team'] = teamd
                    break

                      
            d['template'] = 'avispa_rest/put_rq_a_m_n_settings.html'
        else:
            #This is a regular user
         
            d['redirect'] = '/'+handle+'/_home'
     
        return d




    def put_a_m_n_settings(self,request,handle,team,*args):
        d = {}
        p = {}     

        if ('description' in request.form) or ('teamauth' in request.form): 
            print('xx')
            p['description'] = request.form.get('description')
            p['teamauth'] = request.form.get('teamauth')
            if self.ATM.put_a_m_n_settings(handle,team,p):
                print(team + ' has been updated.')
                flash(team + ' has been updated.')
            else:
                print(' There was a problem updating '+team+'.')
                flash(' There was a problem updating '+team+'.')  

        d['redirect'] = '/'+handle+'/_teams/'+team

        return d 



 