# Import flask dependencies
import urlparse, time, datetime
from flask import Blueprint, render_template, request, redirect
from AvispaRestFunc import AvispaRestFunc
from AvispaCollectionsRestFunc import AvispaCollectionsRestFunc
from MyRingTool import MyRingTool
from MyRingPatch import MyRingPatch
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from default_config import IMAGE_STORE
from env_config import IMAGE_STORE




avispa_rest = Blueprint('avispa_rest', __name__, url_prefix='')
#It is very important to leave url_prefix empty as all the segments will be dynamic


def route_dispatcher(depth,handle,ring=None,idx=None,api=False):

    
    ARF = AvispaRestFunc()

    #Will have to move _tools and _patch this to its own FlaskBlueprint
    MRT = MyRingTool()
    MRP = MyRingPatch()
    


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



    if handle=='_tools':  #not a ring! System specific tools
        tool = ring
        data = getattr(MRT, tool.lower())(request)
        print('flagA:')
        print(data)
    elif handle=='_patch':
        tool = ring
        data = getattr(MRP, tool.lower())(request)
        print('flagA:')
        print(data)


    else:
        data = getattr(ARF, m.lower())(request,handle,ring,idx,api=api)

    if 'collection' in request.args:
        data['collection'] = request.args.get('collection')

    data['handle']=handle
    data['ring']=ring
    data['idx']=idx
    data['current_user']=current_user

    o = urlparse.urlparse(request.url)
    data['host_url']=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

    t = time.time()
    data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))

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


def collection_dispatcher(depth,handle,collection=None,idx=None,api=False):

    ACF = AvispaCollectionsRestFunc()


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

    #method = request.method
    m = method+depth
    data = {}

    data = getattr(ACF, m.lower())(request,handle,collection,idx,api=api)

    data['handle']=handle
    data['collection']=collection
    data['idx']=idx
    data['current_user']=current_user

    o = urlparse.urlparse(request.url)
    data['host_url']=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

    t = time.time()
    data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))

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


def dashboard_dispatcher(handle,dashboard_widgets):

    if 'collection_list' in dashboard_widgets:
        ACF = AvispaCollectionsRestFunc()
        m = 'get_a_x'
        collections = getattr(ACF, m.lower())(request,handle,None,None)
        

    if 'ring_list' in dashboard_widgets:
        ARF = AvispaRestFunc()
        m = 'get_a'
        rings = getattr(ARF, m.lower())(request,handle,None,None)
        


    data = {'message': 'Using get_a for handle '+handle ,
            'template':'avispa_rest/userhome.html',
            'handle': handle,
            'rings': rings,
            'collections': collections }
    
    return render_template(data['template'], data=data)

    
    


# Set the route and accepted methods
@avispa_rest.route('/')
@login_required
def index():

    data = {}
    data['handle']='x' #you have to grab this from the session user
    return render_template("avispa_rest/intro.html", data=data)


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

@avispa_rest.route('/_tools/install', methods=['GET'])
#This is needed because in a Vanilla install there are no users so /<handle>/<ring> would redirect me to /_login
def first_install():


    result = route_dispatcher('_a_b','_tools','install')
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/<handle>/_home', methods=['GET'])
#This is needed because in a Vanilla install there are no users so /<handle>/<ring> would redirect me to /_login
def home(handle):

    dashboard_widgets = []
    dashboard_widgets.append('production_timeline')
    dashboard_widgets.append('collection_list')
    dashboard_widgets.append('ring_list')

    result = dashboard_dispatcher(handle,dashboard_widgets)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result



@avispa_rest.route('/_api/<handle>', methods=['GET'])
def api_route_a(handle):

    result = route_dispatcher('_a',handle,api=True)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/_api/<handle>/<ring>', methods=['GET'])
def api_route_a_b(handle,ring):

    result = route_dispatcher('_a_b',handle,ring,api=True)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/_api/<handle>/<ring>/<idx>', methods=['GET'])
def api_route_a_b_c(handle,ring,idx):

    result = route_dispatcher('_a_b_c',handle,ring,idx,api=True)

    if 'redirect' in result:
        return redirect(result['redirect'])
    else:
        return result

@avispa_rest.route('/<handle>/_collections', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def collections_route_a_x(handle):

    result = collection_dispatcher('_a_x',handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/<handle>/_collections/<collection>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def collections_route_a_x_y(handle,collection):

    result = collection_dispatcher('_a_x_y',handle,collection)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/<handle>/_collections/<collection>/<ring>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def collections_route_a_x_y_b(handle,collection,idx):

    result = collection_dispatcher('_a_x_y_b',handle,collection,idx)

    if 'redirect' in result:
        return redirect(result['redirect'])
    else:
        return result

@avispa_rest.route('/<handle>/_collections/<collection>/<ring>/<idx>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def collections_route_a_x_y_b_c(handle,collection,idx):

    result = collection_dispatcher('_a_x_y_b_c',handle,collection,idx)

    if 'redirect' in result:
        return redirect(result['redirect'])
    else:
        return result


@avispa_rest.route('/<handle>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def route_a(handle):

    print("get_a:Login")
    print(handle)
    print(current_user.id)

    if handle != current_user.id:
        return redirect('/_logout') 

    result = route_dispatcher('_a',handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result
    

@avispa_rest.route('/<handle>/<ring>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def route_a_b(handle,ring):

    result = route_dispatcher('_a_b',handle,ring)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result
        


@avispa_rest.route('/<handle>/<ring>/<idx>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def route_a_b_c(handle,ring,idx):

    result = route_dispatcher('_a_b_c',handle,ring,idx)

    if 'redirect' in result:
        return redirect(result['redirect'])
    else:
        return result

    










