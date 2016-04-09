import time


class timethis:
    def __init__(self,function):

        self.function = function


    def __call__(self,*args,**kargs):

        #print "Inside __call__()"      

        ts = time.time()

        #print('args',args)
        #print('kargs',kargs)
        result = self.function(*args,**kargs)
        te = time.time()

        #print 'TIMETHIS: %r,%r,%2.2f sec' % \
              #(request.method,request.url, te-ts)

        #print 'TIMETHIS: %r,%r,%r,%r,%r,%2.2f sec' % \
            #(request.method,request.url,self.function.__name__, args, kargs, te-ts)


        print 'TIMETHIS: %r (%r, %r) %2.2f sec' % \
             (self.function.__name__, args, kargs, te-ts)

        return result

        