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

    return render_template("avispa_rest/index.html", route='index')

@avispa_rest.route('/<user>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def method_a(user):

    return route_dispatcher('_a',user)
    

@avispa_rest.route('/<user>/<ring>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def method_a_b(user,ring):

    return route_dispatcher('_a_b',user,ring)

@avispa_rest.route('/<user>/<ring>/<idx>/', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def method_a_b_c(user,ring,idx):

    return route_dispatcher('_a_b_c',user,ring,idx)









