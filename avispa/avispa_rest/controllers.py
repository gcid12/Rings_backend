# Import flask dependencies
import urlparse
from flask import Blueprint, render_template, request, redirect
from AvispaRestFunc import AvispaRestFunc
from MyRingTool import MyRingTool
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from default_config import IMAGE_STORE
from env_config import IMAGE_STORE



avispa_rest = Blueprint('avispa_rest', __name__, url_prefix='')
#It is very important to leave url_prefix empty as all the segments will be dynamic


def route_dispatcher(depth,handle,ring=None,idx=None):

    ARF = AvispaRestFunc()
    MRT = MyRingTool()
    


    if 'q' in request.args:
        if request.args.get("q"):
            method = 'search'
        else:
            method = 'search_rq'
    elif request.args.get("rq"):
        method = request.args.get("rq")+'_rq'
    elif request.args.get("rs"):
        method = request.args.get("rq")+'_rs'
    elif request.args.get("method"):
        method = request.args.get("method")
    else:
        method = request.method

    m = method+depth
    data = {}



    if handle=='_tools':  #not a ring! Here goes all the system specific functionality
        tool = ring
        data = getattr(MRT, tool.lower())(request)
        print('flagA:')
        print(data)

    else:
        data = getattr(ARF, m.lower())(request,handle,ring,idx)

    data['handle']=handle
    data['ring']=ring
    data['idx']=idx
    data['current_user']=current_user

    o = urlparse.urlparse(request.url)
    data['host_url']=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

    print("host_url")
    print(data['host_url'])


    if 'error_status' in data.keys():
        status = int(data['error_status'])
    else:
        status = 200

    if 'redirect' in data:
        print('flag0')
        print(data)
        return data             
    elif request.headers.get('Accept') and request.headers.get('Accept').lower() == 'application/json': 
        print('flag1')
        print(data)      
        return render_template(data['template'], data=data), status     
    else:
        print('flag2')
        #print(data) 
        return render_template(data['template'], data=data)
        #return 'ok'




# Set the route and accepted methods
@avispa_rest.route('/')
@login_required
def index():

    data = {}
    data['handle']='x' #you have to grab this from the session user
    return render_template("avispa_rest/intro.html", data=data)

@avispa_rest.route('/tools/', methods=['GET','POST'])
@login_required
def intro():

    data = {}
    return render_template("avispa_rest/tools.html", data=data)

@avispa_rest.route('/_images/<depth1>/<depth2>/<filename>', methods=['GET', 'POST'])

def imageserver(filename,depth1,depth2):

    avispa_rest.static_folder=IMAGE_STORE+'/'+depth1+'/'+depth2
    return avispa_rest.send_static_file(filename)

@avispa_rest.route('/static/<filename>', methods=['GET', 'POST'])

def static(filename):

    avispa_rest.static_folder='static'
    return avispa_rest.send_static_file(filename)

@avispa_rest.route('/static/<depth1>/<filename>', methods=['GET', 'POST'])

def static2(filename,depth1):

    avispa_rest.static_folder='static/'+depth1
    return avispa_rest.send_static_file(filename)

@avispa_rest.route('/static/<depth1>/<depth2>/<filename>', methods=['GET', 'POST'])

def static3(filename,depth1,depth2):

    avispa_rest.static_folder='static/'+depth1+'/'+depth2
    return avispa_rest.send_static_file(filename)

@avispa_rest.route('/static/<depth1>/<depth2>/<depth3>/<filename>', methods=['GET', 'POST'])

def static4(filename,depth1,depth2,depth3):

    avispa_rest.static_folder='static/'+depth1+'/'+depth2+'/'+depth3
    return avispa_rest.send_static_file(filename)

@avispa_rest.route('/static/<depth1>/<depth2>/<depth3>/<depth4>/<filename>/', methods=['GET', 'POST'])

def static5(filename,depth1,depth2,depth3,depth4):

    avispa_rest.static_folder='static/'+depth1+'/'+depth2+'/'+depth3+'/'+depth4
    return avispa_rest.send_static_file(filename)


@avispa_rest.route('/<handle>', methods=['GET', 'POST','PUT','PATCH','DELETE'])

def route_a(handle):

    result = route_dispatcher('_a',handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result
    

@avispa_rest.route('/<handle>/<ring>', methods=['GET', 'POST','PUT','PATCH','DELETE'])

def route_a_b(handle,ring):

    result = route_dispatcher('_a_b',handle,ring)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result
        


@avispa_rest.route('/<handle>/<ring>/<idx>', methods=['GET', 'POST','PUT','PATCH','DELETE'])

def route_a_b_c(handle,ring,idx):

    result = route_dispatcher('_a_b_c',handle,ring,idx)

    if 'redirect' in result:
        return redirect(result['redirect'])
    else:
        return result

    










