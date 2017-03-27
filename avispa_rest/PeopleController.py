# PeopleCollection.py
import logging
from flask import redirect,flash,url_for

from MainModel import MainModel
from PeopleModel import PeopleModel
from TeamsModel import TeamsModel
from AvispaLogging import AvispaLoggerAdapter
from env_config import URL_SCHEME


class PeopleController:

    def __init__(self,tid=None,ip=None):
        
        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})
               
        self.MAM = MainModel(tid=tid,ip=ip)
        self.PEM = PeopleModel(tid=tid,ip=ip)
        self.TEM = TeamsModel(tid=tid,ip=ip)
        
    # GET/a
    def get_a_p(self,handle,person,*args,**kargs):

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
                    person['memberships'] = self.TEM.get_a_m_all_p_q(handle,person['handle'])
                

            
            d['template'] = 'avispa_rest/get_a_p.html'
        else:
            #This is a regular user
         
            #d['redirect'] = '/'+handle+'/_home'
            d['redirect'] = url_for('avispa_rest.home',
                                     handle=handle,
                                     _external=True,
                                     _scheme=URL_SCHEME) 
     
        return d


        # POST/a
    def post_a_p(self,handle,person,rqform=None,*args,**kargs):

        #We need to recover from request as it doesn't come via URL
        person = rqform.get('newperson')

        #Check if the user exists or not
        if self.MAM.user_exists(person):

            result = self.PEM.post_a_p(handle,person)
                
            if result:
                self.lggr.debug('Awesome , you just added %s to the organization'%person)
                #msg = 'Item put with id: '+idx
                flash('Awesome , you just added %s to the organization'%person,'UI')

            else:
                self.lggr.error('Awesome , you just added %s to the organization'%person)
                flash('There was an error adding %s to the organization.'%s,'ER')

        else:
            self.lggr.debug('%s is not a MyRing user. Please create it first.'%person)
            flash('%s is not a MyRing user. Please create it first.'%person,'ER')

  
        #redirect = '/'+handle+'/_people'
        redirect = url_for('avispa_rest.people_a_p',
                                     handle=handle,
                                     _external=True,
                                     _scheme=URL_SCHEME) 

        d = {'redirect': redirect, 'status':200}
        return d


        #DELETE /a/b
    def delete_a_p_q(self,handle,person,*args,**kargs):
        #Will delete an existing person
        self.lggr.debug('Trying to delete the following person: %s'%person)

        #Check if the user exists or not
        if self.MAM.user_exists(person):

            result = self.PEM.delete_a_p_q(handle,person)
                
            if result:
                self.lggr.debug('You just deleted %s from the organization'%person)
                flash('You just deleted %s from the organization'%person,'UI')

            else:
                self.lggr.error('There was an error deleting %s from the organization.'%person)
                flash('There was an error deleting %s from the organization.'%person,'ER')

        else:
            self.lggr.debug('%s is not a MyRing user.'%person)
            flash('%s is not a MyRing user.'%person,'ER')


        
        #redirect = '/'+handle+'/_people'
        redirect = url_for('avispa_rest.people_a_p',
                                     handle=handle,
                                     _external=True,
                                     _scheme=URL_SCHEME) 

        d = {'redirect': redirect, 'status':200}
        return d




 