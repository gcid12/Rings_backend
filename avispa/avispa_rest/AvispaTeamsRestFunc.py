# AvispaCollectionsRestFunc.py
import urlparse, random
from flask import redirect, flash
from AvispaModel import AvispaModel
from MainModel import MainModel
from flask.ext.login import current_user
from AvispaTeamsModel import AvispaTeamsModel
from flanker.addresslib import address
from datetime import datetime
from app import flask_bcrypt
from EmailModel import EmailModel


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
            allteams = {}         
            for teamd in peopleteams['teams']:
                #get the profilepic for this person
                print('teamname:'+teamd['teamname'])

                for member in teamd['members']:

                    print('member:'+member['handle'])

                    

                    person_user_doc = self.MAM.select_user_doc_view('auth/userbasic',member['handle'])
                    if person_user_doc:
                        member['thumbnail'] = person_user_doc['profilepic']

                    if current_user.id == member['handle']:
                        print(member['handle']+' is member')
                        #print('T writing'+teamd['roles'][-1]['role'])
                        if teamd['teamname'] == 'owner':
                            d['teammembership'][teamd['teamname']] = 'org_owner'
                        else:
                            if len(teamd['roles']) >= 1:
                                d['teammembership'][teamd['teamname']] = teamd['roles'][-1]['role']


                allteams[teamd['teamname']] = 'org_owner'
                #print('allteams:',allteams)


            if 'owner' in d['teammembership']:
                d['teammembership'] = allteams



           
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
                    flash('This team exists already. Use a different name','ER')
                    redirect = '/'+handle+'/_teams' 
                    d = {'redirect': redirect, 'status':200}
                    return d 

            if self.MAM.add_team(handle,team,current_user.id):
                print('Awesome , you just created team '+ team +'.')
                #msg = 'Item put with id: '+idx
                flash('Awesome , you just created team '+ team +'.','UI')
                redirect = '/'+handle+'/_teams'
            else:
                flash('There was an error adding team: '+ team +'.','UI')
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
                flash(member + ' has been added to the team.','UI')
            else:
                print(member + ' is already part of this team.')
                flash(member + ' is already part of this team.','UI')

        if 'delmember' in request.args: 
            member = request.args.get('delmember')
            if self.ATM.delete_a_m_n_members(handle,team,member):
                print(member + ' has been deleted from the team.')
                flash(member + ' has been deleted from the team.','UI')
            else:
                print('There was an issue deleting: ' + member + '.')
                flash('There was an issue deleting: ' + member + '.','UI')
            
        if 'newring' in request.form:
            ring = request.form.get('newring')
            if self.ATM.post_a_m_n_rings(handle,team,ring):
                print(ring + ' has been added to the team.')
                flash(ring + ' has been added to the team.','UI')
            else:
                print(ring + ' already  exists in this team.')
                flash(ring + ' already  exists in this team.','UI')           

        if 'delring' in request.args:
            ring = request.args.get('delring')
            if self.ATM.delete_a_m_n_rings(handle,team,ring):
                print(ring + ' has been deleted from the team.')
                flash(ring + ' has been deleted from the team.','UI')
            else:
                print('There was an issue deleting: ' + ring + '.')
                flash('There was an issue deleting: ' + ring + '.','UI')
            
            
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
                        flash('You just deleted team '+ team +'.','UI')
                        redirect = '/'+handle+'/_teams'
                    else:
                        flash('There was an error deleting team: '+ team +'.','ER')
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
                flash(team + ' has been updated.','UI')
            else:
                print(' There was a problem updating '+team+'.')
                flash(' There was a problem updating '+team+'.','ER')  

        d['redirect'] = '/'+handle+'/_teams/'+team

        return d 

    def get_a_m_n_invite(self,request,handle,team,*args):

        redirect = '/'+handle+'/_teams/'+team        

        d = {'redirect': redirect, 'status':200}
        return d


    def put_rq_a_m_n_invite(self,request,handle,team,*args):
        
        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams:   
            
            d['people'] = peopleteams['people']        
            
            for teamd in peopleteams['teams']:
                #get the profilepic for this person

                if teamd['teamname'] == team :
                    d['team'] = teamd
                    break
                   
        d['template'] = 'avispa_rest/put_rq_a_m_n_invite.html'

        return d




    def put_a_m_n_invite(self,request,handle,team,*args):
        d = {}

        self.EMM = EmailModel()


        collabraw = request.form.get('emails')

        valid_emails, invalid_emails = address.validate_list(collabraw, as_tuple=True)

        print('valid_emails:',valid_emails)
        print('invalid_emails:',invalid_emails)

        #2. If it is an email, send ring subscription url/token 

        o = urlparse.urlparse(request.url)
        host_url=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

        #2a PENDING
        # Subtract team object from org document
        peopleteams = self.MAM.is_org(handle) 
        if peopleteams:   
              
            for teamd in peopleteams['teams']:
                teamfound = False
                
                if teamd['teamname'] == team :
                    # This team actually exists in this org. You can continue with the invitations
                    teamfound = True
                    break

            if not teamfound:
                # This team doesnt exist. No invitation can be sent
                d['redirect'] = '/'+handle+'/_teams/'+team
                return d

            # teamd carries the team object
        #Try to convert invalid_emails (myringIDs) into valid_emails

        print("flag1")

        for invite_handle in invalid_emails:
            user_doc = self.MAM.select_user_doc_view('auth/userbyhandle',invite_handle)                   
            if user_doc:
                if user_doc['email'] not in valid_emails:
                    valid_emails.append(user_doc['email'])

        for email in valid_emails:

            print("flag2")

            email = str(email)
            
            # Check if the invitations object even exists. If not create
            if not 'invitations' in teamd:
                teamd['invitations'] = []

            invite={}
            invite['email'] = email
            invite['count'] = 1
            invite['token'] = flask_bcrypt.generate_password_hash(email+str(random.randint(0,9999)))  
            invite['lasttime'] = str(datetime.now())
            invite['author'] = current_user.id
            
            

            user_doc = self.MAM.select_user_doc_view('auth/userbyemail',email)         

            if user_doc:
                #You are inviting an existing myRing user
                existinguser = True
                
            else:
                #You are inviting a soon to be myRing user
                existinguser = False

            print("flag3")

            #host_url = "https://avispa.myring.io"
                
            token = invite['token'] 
            to = email
            subject = handle+" has invited you to collaborate in the following team : "+team
            # https://avispa.myring.io/_register?h=cdmit&t=staff&k=11111&e=invi@tado.com
            content = "Click here to start working with this team: "+host_url+"/_register?h="+handle+"&t="+team+"&k="+token+"&e="+email
            print(to,subject,content)

            if self.EMM.send_one_email(to,subject,content):
                flash("Invitation email sent.",'UI') 
                self.MAM.append_to_user_field(handle,'invitations',invite) 
            else:
                flash("Invitation email failed.",'UI') 
        
              
        d['redirect'] = '/'+handle+'/_teams/'+team
        return d 



 