#TeamsRestFunc.py
import urlparse, random
import logging
from flask import redirect, flash, url_for
from MainModel import MainModel
from flask.ext.login import current_user
from TeamsModel import TeamsModel
from flanker.addresslib import address
from datetime import datetime
from app import flask_bcrypt
from EmailModel import EmailModel
from AvispaLogging import AvispaLoggerAdapter
from env_config import URL_SCHEME


class TeamsCollection:

    def __init__(self,tid=None,ip=None):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})
        
        self.MAM = MainModel(tid=tid,ip=ip)
        self.TEM = TeamsModel(tid=tid,ip=ip)

    # GET/a
    def get_a_m(self,handle,team,*args,**kargs):

        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams: 
            #This is an organization         
            
            d['teamlistlen'] = len(peopleteams['teams'])
            d['teammembership'] = {}
            allteams = {}         
            for teamd in peopleteams['teams']:
                #get the profilepic for this person
                self.lggr.debug('teamname:%s'%teamd['teamname'])

                for member in teamd['members']:

                    self.lggr.debug('member:%s'%member['handle'])

                    person_user_doc = self.MAM.select_user_doc_view('auth/userbasic',member['handle'])
                    if person_user_doc:
                        member['thumbnail'] = person_user_doc['profilepic']

                    if current_user.id == member['handle']:
                        self.lggr.debug('%s is member'%member['handle']) 
                        if teamd['teamname'] == 'owner':
                            d['teammembership'][teamd['teamname']] = 'org_owner'
                        else:
                            if len(teamd['roles']) >= 1:
                                d['teammembership'][teamd['teamname']] = teamd['roles'][-1]['role']

                allteams[teamd['teamname']] = 'org_owner'

            if 'owner' in d['teammembership']:
                d['teammembership'] = allteams
       
            d['teamlist'] = peopleteams['teams']            
            d['template'] = 'avispa_rest/get_a_m.html'
        else:
            #This is a regular user
            #d['redirect'] = '/'+handle+'/_home'
            d['redirect'] = url_for('avispa_rest.home',
                                     handle=handle,
                                     _external=True,
                                     _scheme=URL_SCHEME)
     
        return d

        # POST/a
    def post_a_m(self,handle,team,rqform=None,*args,**kargs):
        '''
        Creates a new team
        '''
        #We need to recover from request as it doesn't come via URL
        team = rqform.get('newteam')

        #Check if the team exists or not
        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams: 

            redirect = url_for('avispa_rest.teams_a_m',
                                     handle=handle,
                                     _external=True,
                                     _scheme=URL_SCHEME)

            #This is an organization                  
            for teamd in peopleteams['teams']:
                
                if teamd['teamname'] == team:
                    #This team exists in this handle!
                    flash('This team exists already. Use a different name','ER')
                    #redirect = '/'+handle+'/_teams'

                    d = {'redirect': redirect, 'status':200}
                    return d 

            if self.MAM.add_team(handle,team,current_user.id):
                self.lggr.debug('Awesome , you just created team %s '%team)
                #msg = 'Item put with id: '+idx
                flash('Awesome , you just created team %s '%team,'UI')
                
            else:
                flash('There was an error adding team %s '%team,'UI') 

        else:
            #This is not an organization 
            #redirect = '/'+current_user.id 
            redirect = url_for('avispa_rest.home',
                                handle=handle,
                                _external=True,
                                _scheme=URL_SCHEME)       

        d = {'redirect': redirect, 'status':200}
        return d


    def get_a_m_n(self,handle,team,*args,**kargs):

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
            #d['redirect'] = '/'+handle+'/_home'
            d['redirect'] = url_for('avispa_rest.home',
                                handle=handle,
                                _external=True,
                                _scheme=URL_SCHEME)         
     
        return d

    def put_a_m_n(self,handle,team,rqform=None,rqargs=None,*args,**kargs):

        #This function should be refactored into multiple functions that obey RESTFUL:
        # post_a_m_n_members , delete_a_m_n_members , post_a_m_n_rings, delete_a_m_n_rings

        d = {}

        if 'newmember' in rqform: 
            member = rqform.get('newmember')
            if self.TEM.post_a_m_n_members(handle,team,member):
                self.lggr.debug('%s has been added to the team.'%member)
                flash('%s has been added to the team.'%member,'UI')
            else:
                self.lggr.debug('%s is already part of this team.'%member)
                flash('%s is already part of this team.'%member,'UI')

        if 'delmember' in rqargs: 
            member = rqargs.get('delmember')
            if self.TEM.delete_a_m_n_members(handle,team,member):
                self.lggr.debug('%s has been deleted from the team.'%member)
                flash('%s has been deleted from the team.'%member,'UI')
            else:
                self.lggr.error('There was an issue deleting: %s'%member)
                flash('There was an issue deleting: %s'%member,'UI')
            
        if 'newring' in rqform:
            ring = rqform.get('newring')
            if self.TEM.post_a_m_n_rings(handle,team,ring):
                self.lggr.debug('%s has been added to the team.'%ring)
                flash('%s has been added to the team.'%ring,'UI')
            else:
                self.lggr.error('%s already  exists in this team.'%ring)
                flash('%s already  exists in this team.'%ring,'UI')           

        if 'delring' in rqargs:
            ring = rqargs.get('delring')
            if self.TEM.delete_a_m_n_rings(handle,team,ring):
                self.lggr.debug('%s has been deleted from the team.'%ring)
                flash('%s has been deleted from the team.'%ring,'UI')
            else:
                self.lggr.error('There was an issue deleting: %s'%ring)
                flash('There was an issue deleting: %s'%ring,'UI')
                
        #d['redirect'] = '/'+handle+'/_teams/'+team
        d['redirect'] = url_for('avispa_rest.teams_a_m_n',
                                     handle=handle,
                                     team=team,
                                     _external=True,
                                     _scheme=URL_SCHEME)

        return d


        #DELETE /a/b
    def delete_a_m_n(self,handle,team,*args,**kargs):
        #Will delete an existing person
        self.lggr.debug('Trying to delete the following team: %s'%team)

        d = {}

        peopleteams = self.MAM.is_org(handle) 
        if peopleteams: 
            #This is an organization  

            for teamd in peopleteams['teams']:
                
                if teamd['teamname'] == team:
                    
                    if self.MAM.delete_team(handle,team):
                        self.lggr.debug('You just deleted team %s'%team)
                        flash('You just deleted team %s'%team,'UI')                      
                    else:
                        self.lggr.error('There was an error deleting team: %s'%team)
                        flash('There was an error deleting team: %s'%team,'ER')                       

                    redirect = url_for('avispa_rest.teams_a_m',
                                        handle=handle,
                                        _external=True,
                                        _scheme=URL_SCHEME)


        else:
            #This is not an organization 
            #redirect = '/'+current_user.id
            redirect = url_for('avispa_rest.home',
                                        handle=handle,
                                        _external=True,
                                        _scheme=URL_SCHEME)      

        d = {'redirect': redirect, 'status':200}
        return d

    def get_a_m_n_settings(self,handle,team,*args,**kargs):

        #redirect = '/'+handle+'/_teams/'+team 
        redirect = url_for('avispa_rest.teams_a_m_n',
                            handle=handle,
                            team=team,
                            _external=True,
                            _scheme=URL_SCHEME)


        d = {'redirect': redirect, 'status':200}
        return d


    def put_rq_a_m_n_settings(self,handle,team,*args,**kargs):
        
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
         
            #d['redirect'] = '/'+handle+'/_home'
            d['redirect'] = url_for('avispa_rest.home',
                                handle=handle,
                                _external=True,
                                _scheme=URL_SCHEME) 
     
        return d


    def put_a_m_n_settings(self,handle,team,rqform=None,*args,**kargs):
        d = {}
        p = {}     

        if ('description' in rqform) or ('teamauth' in rqform): 
            p['description'] = rqform.get('description')
            p['teamauth'] = rqform.get('teamauth')
            if self.TEM.put_a_m_n_settings(handle,team,p):
                self.lggr.debug('%s has been updated.'%team)
                flash('%s has been updated.'%team,'UI')
            else:
                self.lggr.error('There was a problem updating team %s'%team)
                flash('There was a problem updating team %s'%team,'ER')  

        #d['redirect'] = '/'+handle+'/_teams/'+team
        d['redirect'] = url_for('avispa_rest.teams_a_m_n',
                            handle=handle,
                            team=team,
                            _external=True,
                            _scheme=URL_SCHEME)

        return d 

    def get_a_m_n_invite(self,handle,team,*args,**kargs):

        #redirect = '/'+handle+'/_teams/'+team 
        redirect = url_for('avispa_rest.teams_a_m_n',
                            handle=handle,
                            team=team,
                            _external=True,
                            _scheme=URL_SCHEME)       

        d = {'redirect': redirect, 'status':200}
        return d


    def put_rq_a_m_n_invite(self,handle,team,*args,**kargs):
        
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




    def put_a_m_n_invite(self,handle,team,rqurl=None,rqform=None,*args,**kargs):
        d = {}

        self.EMM = EmailModel()
        collabraw = rqform.get('emails')
        valid_emails, invalid_emails = address.validate_list(collabraw, as_tuple=True)

        self.lggr.debug('valid_emails:%s'%valid_emails)
        self.lggr.debug('invalid_emails:%s'%invalid_emails)

        #2. If it is an email, send ring subscription url/token 

        o = urlparse.urlparse(rqurl)
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
                #d['redirect'] = '/'+handle+'/_teams/'+team
                d['redirect'] = url_for('avispa_rest.teams_a_m_n',
                                         handle=handle,
                                         team=team,
                                         _external=True,
                                         _scheme=URL_SCHEME)
                return d

            # teamd carries the team object
        #Try to convert invalid_emails (myringIDs) into valid_emails

        for invite_handle in invalid_emails:
            user_doc = self.MAM.select_user_doc_view('auth/userbyhandle',invite_handle)                   
            if user_doc:
                if user_doc['email'] not in valid_emails:
                    valid_emails.append(user_doc['email'])

        for email in valid_emails:

            email = str(email)
              
            invite={}
            invite['email'] = email
            invite['count'] = 1
            invite['team'] = team
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

            token = invite['token'] 
            to = email
            subject = handle+" has invited you to collaborate in the following team : "+team
            # https://avispa.myring.io/_register?h=cdmit&t=staff&k=11111&e=invi@tado.com
            content = "Click here to start working with this team: "+host_url+"/_register?h="+handle+"&t="+team+"&k="+token+"&e="+email
            self.lggr.debug('%s,%s,%s'%(to,subject,content))

            if self.EMM.send_one_email(to,subject,content):
                flash("Invitation email sent.",'UI') 
                self.MAM.append_to_user_field(handle,'invitations',invite) 
            else:
                flash("Invitation email failed.",'UI') 
        
              
        #d['redirect'] = '/'+handle+'/_teams/'+team
        d['redirect'] = url_for('avispa_rest.teams_a_m_n',
                                 handle=handle,
                                 team=team,
                                 _external=True,
                                 _scheme=URL_SCHEME)

        

        return d 




 