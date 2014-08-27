# Import flask dependencies
from flask import Blueprint, render_template, request
from AvispaRestFunc import AvispaRestFunc


avispa_rest = Blueprint('avispa_rest', __name__, url_prefix='')
#It is very important to leave url_prefix empty as all the segments will be dynamic
ARF = AvispaRestFunc()


def route_dispatcher(depth,user,ring=None,idx=None):

    m = request.method+depth
    r = getattr(ARF, m.lower())(user,ring,idx)


    accept = request.headers.get('Accept')

    if accept.lower() == 'application/json':
        return 'Display JSON version'
    else:
        return render_template(r['template'], results=r['message'])

# Set the route and accepted methods
@avispa_rest.route('/')
@avispa_rest.route('/index/', methods=['GET', 'POST'])
def index():

    return render_template("avispa_rest/index2.html", route='index')

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

@avispa_rest.route('/<user>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def method_a(user):

    return route_dispatcher('_a',user)
    

@avispa_rest.route('/<user>/<ring>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def method_a_b(user,ring):

    return route_dispatcher('_a_b',user,ring)

@avispa_rest.route('/<user>/<ring>/<idx>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def method_a_b_c(user,ring,idx):

    return route_dispatcher('_a_b_c',user,ring,idx)









