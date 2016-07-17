# AvispaBadgesRestFunc.py
import logging
from flask import redirect, flash

from AvispaModel import AvispaModel
from MainModel import MainModel
from AvispaBadgesModel import AvispaBadgesModel
from AvispaLogging import AvispaLoggerAdapter


class AvispaBadgesRestFunc:

    def __init__(self,tid=None,ip=None):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})
        
        self.AVM = AvispaModel(tid=tid,ip=ip)
        self.MAM = MainModel(tid=tid,ip=ip)
        self.ATM = AvispaBadgesModel(tid=tid,ip=ip)

    def get_a_p(self,handle,badge,*args,**kargs):
        '''
          Get all badges for one handle
        '''
        result = self.APM.get_a_p(handle,person)

    def post_a_p(self,handle,badge,rqform=None,*args,**kargs):
        '''
          Create new badge for a handle
        '''
        result = self.APM.post_a_p(handle,person)

    def delete_a_p_q(self,handle,badge,*args,**kargs):
        '''
          Delete a badge from a handle
        '''
        result = self.APM.delete_a_p_q(handle,person)

