from flask import Blueprint,request,redirect,url_for
from flask.ext.login import current_user, login_required
from env_config import  URL_SCHEME
from dispatchers import rings_dispatcher,tool_dispatcher,patch_dispatcher,\
                        index_dispatcher,collection_dispatcher,home_dispatcher,\
                        history_dispatcher,people_dispatcher,teams_dispatcher,\
                        labels_dispatcher

avispa_rest = Blueprint('avispa_rest', __name__, url_prefix='')

# Set the route and accepted methods
@avispa_rest.route('/')
@login_required
def index():

    data = {}
    data['handle']='x' #you have to grab this from the session user

    return redirect(url_for('avispa_rest.home',
                                     handle=current_user.id,
                                     _external=True,
                                     _scheme=URL_SCHEME))


@avispa_rest.route('/<handle>/_history', methods=['GET'])
#This is to get the activity for a given user
def history_h(handle):

    result = history_dispatcher(handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/<handle>/<ring>/_history', methods=['GET'])
#This is to get the activity for a given user
def history_h_r(handle,ring):

    result = history_dispatcher(handle,ring=ring)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result



@avispa_rest.route('/_tools/install', methods=['GET'])
#This is needed because in a Vanilla install there are no users so /_tools/install would redirect me to /_login
def first_install():

    #result = rings_dispatcher('_a_b','_tools','install')
    result = tool_dispatcher('install')
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_tools/<tool>', methods=['GET','POST'])
def tool(tool):

    result = tool_dispatcher(tool)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_patch/<patchnumber>', methods=['GET'])
def patch(patchnumber):

    result = patch_dispatcher(patchnumber)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/<handle>/_home', methods=['GET'])
@login_required
def home(handle):

    result = home_dispatcher(handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result



@avispa_rest.route('/_api/<handle>/_index', methods=['GET'])
@login_required
def index_a(handle):

    result = index_dispatcher(handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_api/<handle>/<ring>/_index', methods=['GET'])
@login_required
def index_a_b(handle,ring):

    result = index_dispatcher(handle,ring)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_api/<handle>/<ring>/<idx>/_index', methods=['GET'])
@login_required
def index_a_b_c(handle,ring,idx):

    result = index_dispatcher(handle,ring,idx)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_api/<handle>/_unindex', methods=['GET'])
@login_required
def unindex_a(handle):

    result = index_dispatcher(handle,unindex=True)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_api/<handle>/<ring>/_unindex', methods=['GET'])
@login_required
def unindex_a_b(handle,ring):

    result = index_dispatcher(handle,ring,unindex=True)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_api/<handle>/<ring>/<idx>/_unindex', methods=['GET'])
@login_required
def unindex_a_b_c(handle,ring,idx):

    result = index_dispatcher(handle,ring,idx,unindex=True)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result



@avispa_rest.route('/<handle>/<ring>/_labels', methods=['GET','POST','PUT','DELETE'])
@login_required
def labels_a_l(handle):

    result = labels_dispatcher(handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result



@avispa_rest.route('/<handle>/_people', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def people_a_p(handle):

    result = people_dispatcher('_a_p',handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/<handle>/_people/<person>', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def people_a_p_q(handle,person):
    
    result = people_dispatcher('_a_p_q',handle,person)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result
    


@avispa_rest.route('/<handle>/_teams', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def teams_a_m(handle):

    result = teams_dispatcher('_a_m',handle)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/<handle>/_teams/<team>', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def teams_a_m_n(handle,team):

    result = teams_dispatcher('_a_m_n',handle,team=team)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/<handle>/_teams/<team>/_people', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def teams_a_m_n_p(handle,team):

    result = teams_dispatcher('_a_m_n_p',handle,team=team)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/<handle>/_teams/<team>/_people/<member>', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def teams_a_m_n_p_q(handle,team,member):

    result = teams_dispatcher('_a_m_n_p_q',handle,team=team,member=member)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/<handle>/_teams/<team>/_rings', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def teams_a_m_n_r(handle,team):

    result = teams_dispatcher('_a_m_n_r',handle,team=team)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/<handle>/_teams/<team>/_rings/<ring>', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def teams_a_m_n_r_b(handle,team,ring):

    result = teams_dispatcher('_a_m_n_r_b',handle,team,ring=ring)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result



@avispa_rest.route('/<handle>/_teams/<team>/_settings', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
@login_required
def teams_a_m_n_settings(handle,team):

    result = teams_dispatcher('_a_m_n_settings',handle,team)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/<handle>/_teams/<team>/_invite', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
@login_required
def teams_a_m_n_invite(handle,team):

    result = teams_dispatcher('_a_m_n_invite',handle,team)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


#API

@avispa_rest.route('/_api/<handle>/_collections', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def api_collections_route_a_x(handle):

    result = collection_dispatcher('_a_x',handle,api=True)
 
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

#API
@avispa_rest.route('/_api/<handle>/_collections/<collection>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def api_collections_route_a_x_y(handle,collection):

    if ('rq' not in request.args) and ('method' not in request.args): 
        result = rings_dispatcher('_a',handle,api=True,collection=collection)       
    elif request.method == 'POST':
        if 'method' in request.args:
            if request.args.get('method').lower()=='put':
                result = collection_dispatcher('_a_x_y',handle,api=True,collection=collection) 
            elif request.args.get('method').lower()=='post':
                result = rings_dispatcher('_a',handle,api=True,collection=collection)
        else:
            result = rings_dispatcher('_a',handle,api=True,collection=collection)

    elif 'rq' in request.args:
        if request.args.get('rq').lower() == 'put':
            result = collection_dispatcher('_a_x_y',handle,api=True,collection=collection)
        if request.args.get('rq').lower() == 'post':
            result = rings_dispatcher('_a',handle,api=True,collection=collection)


    else:
        #Every collection specific GET
        result = collection_dispatcher('_a_x_y',handle,api=True,collection=collection)
 
    if 'redirect' in result:
        return redirect(result['redirect'])    
    else:
        return result


@avispa_rest.route('/<handle>/_collections/<collection>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def collections_route_a_x_y(handle,collection):
    '''
    Administrative functions only. No data
    '''

    if ('rq' not in request.args) and ('method' not in request.args): 

        #result = rings_dispatcher('_a',handle,collection=collection) 
        #We are assuming that not having a collection specific page is ok?
        return redirect(url_for('avispa_rest.home',
                                     handle=handle,
                                     _external=True,
                                     _scheme=URL_SCHEME))  

    elif request.method == 'POST':
        if 'method' in request.args:
            if request.args.get('method').lower()=='put':
                # Put the Collection metadata
                result = collection_dispatcher('_a_x_y',handle,collection) 
            elif request.args.get('method').lower()=='post':
                # Post the Ring
                result = rings_dispatcher('_a',handle,collection=collection)
        else:
            # Post the ring
            result = rings_dispatcher('_a',handle,collection=collection)

    elif 'rq' in request.args:
        if request.args.get('rq').lower() == 'put':
            # Show the form to Edit the Collection metadata
            result = collection_dispatcher('_a_x_y',handle,collection)
        if request.args.get('rq').lower() == 'post':
            # Get the Ring Modeler
            result = rings_dispatcher('_a',handle,collection=collection)

    else:
        #Every collection specific GET
        result = collection_dispatcher('_a_x_y',handle,collection)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


#API
@avispa_rest.route('/_api/<handle>', methods=['GET','POST'])
def api_route_a(handle):

    result = rings_dispatcher('_a',handle,api=True)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

#API
@avispa_rest.route('/_api/<handle>/<ring>', methods=['GET','POST'])
def api_route_a_b(handle,ring):

    result = rings_dispatcher('_a_b',handle,ring,api=True)
 
    #if 'redirect' in result:
     #   return redirect(result['redirect'])        
    #else:
     #   return result

    return result

#API
@avispa_rest.route('/_api/<handle>/<ring>/<idx>', methods=['GET','POST'])
def api_route_a_b_c(handle,ring,idx):

    result = rings_dispatcher('_a_b_c',handle,ring,idx,api=True)

    return result


@avispa_rest.route('/<handle>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def route_a(handle):

    if request.method == 'GET':
        if ('rq' not in request.args) and ('method' not in request.args):         
            return redirect(url_for('avispa_rest.home',
                                     handle=handle,
                                     _external=True,
                                     _scheme=URL_SCHEME))

    if 'collection' in request.args:
        collection = request.args.get('collection')
    else:
        collection = False

    result = rings_dispatcher('_a',handle,collection=collection)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result
    
@avispa_rest.route('/<handle>/<ring>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def route_a_b(handle,ring):

    if 'collection' in request.args:
        collection = request.args.get('collection')
    else:
        collection = False

    result = rings_dispatcher('_a_b',handle,ring,collection=collection)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result



@avispa_rest.route('/<handle>/<ring>/<idx>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def route_a_b_c(handle,ring,idx):

    if 'collection' in request.args:
        collection = request.args.get('collection')
    else:
        collection = False

    result = rings_dispatcher('_a_b_c',handle,ring,idx,collection=collection)

    if 'redirect' in result:
        return redirect(result['redirect'])
    else:
        return result




    


