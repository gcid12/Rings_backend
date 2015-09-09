import time
from flask import request

class timethis:
    def __init__(self, function):
        self.function = function


    def __call__(self, *args, **kw):

        ts = time.time()
        result = self.function(*args, **kw)
        te = time.time()
        
        
        print 'TIMETHIS: %r,%r,%2.2f sec' % \
              (request.method,request.url, te-ts)

        #print 'TIMETHIS: %r,%r,%r,%r,%r,%2.2f sec' % \
              #(request.method,request.url,self.function.__name__, args, kw, te-ts)

        #print '%r (%r, %r) %2.2f sec' % \
        #     ("xxx", args, kw, te-ts)

        return result