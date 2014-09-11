# Import flask dependencies
from flask import Blueprint, render_template, request
from AvispaRestFunc import AvispaRestFunc


avispa_rest = Blueprint('avispa_rest', __name__, url_prefix='')
#It is very important to leave url_prefix empty as all the segments will be dynamic
ARF = AvispaRestFunc()


def route_dispatcher(depth,handle,ring=None,idx=None):

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
    requestx = 'axioma'
    data = {}
    data = getattr(ARF, m.lower())(request,handle,ring,idx)
    data['handle']=handle
    data['ring']=ring
    data['idx']=idx


    if request.headers.get('Accept'):
        accept = request.headers.get('Accept')
        if accept.lower() == 'application/json':
            return 'Display JSON version'
    else:
        return render_template(data['template'], data=data)

# Set the route and accepted methods
@avispa_rest.route('/')
def index():

    data = {}
    data['handle']='x' #you have to grab this from the session user
    return render_template("avispa_rest/intro.html", data=data)

@avispa_rest.route('/tools/', methods=['GET','POST'])
def intro():

    return render_template("avispa_rest/tools.html")

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


@avispa_rest.route('/<handle>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def route_a(handle):

    return route_dispatcher('_a',handle)
    

@avispa_rest.route('/<handle>/<ring>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def route_a_b(handle,ring):

    return route_dispatcher('_a_b',handle,ring)


@avispa_rest.route('/<handle>/<ring>/<idx>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def route_a_b_c(handle,ring,idx):

    return route_dispatcher('_a_b_c',handle,ring,idx)









