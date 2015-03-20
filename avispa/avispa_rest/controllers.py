# Import flask dependencies
import urlparse, time, datetime, collections
from flask import Blueprint, render_template, request, redirect
from AvispaRestFunc import AvispaRestFunc
from AvispaCollectionsRestFunc import AvispaCollectionsRestFunc
from AvispaRolesRestFunc import AvispaRolesRestFunc
from AvispaPeopleRestFunc import AvispaPeopleRestFunc
from AvispaTeamsRestFunc import AvispaTeamsRestFunc
from MyRingTool import MyRingTool
from MyRingPatch import MyRingPatch
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from default_config import IMAGE_STORE
from env_config import IMAGE_STORE
from MainModel import MainModel




avispa_rest = Blueprint('avispa_rest', __name__, url_prefix='')
#It is very important to leave url_prefix empty as all the segments will be dynamic


def route_dispatcher(depth,handle,ring=None,idx=None,api=False,collection=None):

    
    ARF = AvispaRestFunc()



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

    MAM = MainModel()
    authorization_result = MAM.user_is_authorized(current_user.id,m,depth,handle,ring=ring,idx=idx,api=api)
    if not authorization_result['authorized']:
        return render_template('avispa_rest/error_401.html', data=data),401

    data['user_authorizations'] = authorization_result['user_authorizations']

     
    data.update(getattr(ARF, m.lower())(request,handle,ring,idx,api=api,collection=collection))
 

    cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    data['cu_actualname'] = cu_user_doc['name']
    data['cu_profilepic'] = cu_user_doc['profilepic']
    data['cu_location'] = cu_user_doc['location']

    if current_user.id == handle:
        data['handle_actualname'] = cu_user_doc['name']
        data['handle_profilepic'] = cu_user_doc['profilepic']
        data['handle_location'] = cu_user_doc['location']

    else:
        handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
        if handle_user_doc:
            data['handle_actualname'] = handle_user_doc['name']
            data['handle_profilepic'] = handle_user_doc['profilepic']
            data['handle_location'] = handle_user_doc['location']

    if collection:       
        data['collection'] = collection

    if request.args.get("raw"):
        data['raw'] = True 


    data['handle']=handle
    data['ring']=ring
    data['idx']=idx
    data['current_user']=current_user

    o = urlparse.urlparse(request.url)
    data['host_url'] = urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
    data['api_url'] = urlparse.urlunparse((o.scheme, o.netloc, '_api'+o.path, o.params, o.query, o.fragment))

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

def tool_dispatcher(tool):
    
    MRT = MyRingTool()

    data = getattr(MRT, tool.lower())(request)
    print('Tool executed:',data)

    data['handle']=current_user.id
    data['current_user']=current_user
    o = urlparse.urlparse(request.url)
    data['host_url']=urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))

    t = time.time()
    data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))

    if 'redirect' in data:
        return data                 
    else:
        return render_template(data['template'], data=data)


def patch_dispatcher(patchnumber):


    MRP = MyRingPatch()
    patch = str(patchnumber)
    data = getattr(MRP, patch.lower())(request)
    
    if 'redirect' in data:
        return data              
    else:    
        return render_template(data['template'], data=data)


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


    MAM = MainModel()
    authorization_result = MAM.user_is_authorized(current_user.id,m,depth,handle,collection=collection)
    if not authorization_result['authorized']:
        return render_template('avispa_rest/error_401.html', data=data),401
    data['user_authorizations'] = authorization_result['user_authorizations']

    data.update(getattr(ACF, m.lower())(request,handle,collection,idx,api=api))

    MAM = MainModel()
    cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    if cu_user_doc:
        #data['cu_actualname'] = cu_user_doc['name']
        data['cu_profilepic'] = cu_user_doc['profilepic']
        #data['cu_location'] = cu_user_doc['location']

    #Thisi is the data from the handle we are visiting
    if current_user.id == handle:
        data['handle_actualname'] = cu_user_doc['name']
        data['handle_profilepic'] = cu_user_doc['profilepic']
        data['handle_location'] = cu_user_doc['location']

    else:
        handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
        if handle_user_doc:
            data['handle_actualname'] = handle_user_doc['name']
            data['handle_profilepic'] = handle_user_doc['profilepic']
            data['handle_location'] = handle_user_doc['location']


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


def home_dispatcher(handle):

    MAM = MainModel()
    data = {}

    if MAM.user_exists(handle):

        method= 'GET_a_home'
        depth = '_a'
        authorization_result = MAM.user_is_authorized(current_user.id,method,depth,handle)
        if not authorization_result['authorized']:
            return render_template('avispa_rest/error_401.html', data=data),401

        data['user_authorizations'] = authorization_result['user_authorizations']

    
        ACF = AvispaCollectionsRestFunc()
        m = 'get_a_x'
           
        collectionsd = getattr(ACF, m.lower())(request,handle,None,None)  

        #ARF = AvispaRestFunc()
        #m = 'get_a'
        #rings = getattr(ARF, m.lower())(request,handle,None,None)




        data['handle'] = handle
        #data['rings'] = rings
        data['collections'] = collectionsd

        
        # Daily Activity Graph steps
        #0. Create the general count dictionary (with 365 slots)
        #1. Retrieve all rings for this handle. Use view myringusers:ring/count
        ringcounts = MAM.select_user_doc_view('rings/count',current_user.id)
        if ringcounts:
            data['ring_counts'] = ringcounts
            data['total_items'] = 0
            for c in ringcounts:
                data['total_items'] += ringcounts[c]


        #2. Rerieve all the rings of all organizations where this user has something to do
        #3. For each of the rings found:
        

        h_new = collections.OrderedDict()
        h_update = collections.OrderedDict()
        h_generic = collections.OrderedDict()

        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        needle = today
        for d in range(93):
            
            #print('NEEDLE:',needle)
            h_new[str(needle)] = 0
            h_update[str(needle)] = 0
            h_generic[str(needle)] = 0
            needle = needle - one_day

        #print('h_new:',h_new)

            
        for ringx in ringcounts:
            ringdb = current_user.id+'_'+ringx
            ring_dac = MAM.select_ring_doc_view(ringdb,'ring/dailyactivity',current_user.id,5000)
            for item_dac in ring_dac:
                for n in item_dac['new']:
                    if n == str(today):
                        print('NEW TODAY:',item_dac['new'][n])

                    if n in h_generic:
                        h_generic[n] += item_dac['new'][n]

                    
                    if n in h_new:
                        h_new[n] += item_dac['new'][n]
                    else:
                        h_new[n] = item_dac['new'][n]
                    

                for n in item_dac['update']:
                    if n == str(today):
                        print('UPDATED TODAY:',item_dac['update'][n])

                    if n in h_generic:
                        h_generic[n] += item_dac['update'][n]
                    
                    
                    if n in h_update:
                        h_update[n] += item_dac['update'][n]
                    else:
                        h_update[n] = item_dac['update'][n]
                    




        data['dac_totals_date'] = h_generic
        totals_list = [ h_generic.get(k, 0) for k in h_generic]
        for tl in totals_list:
            if tl==0:
                del tl

        data['dac_totals'] = totals_list[::-1]



        #data['dac_totals_date'] = { k: h_new.get(k, 0) + h_update.get(k, 0) for k in h_new | h_update }
        #data['dac_totals'] = [ h_new.get(k, 0) + h_update.get(k, 0) for k in h_new | h_update ]

        #data['dac_new'] = h_new
        #data['dac_update'] = h_update


        #3a: Load its database
        #3b: Call its dailyactivity view with key=handle
        #3c: If something is found iterate through each one of the rows looking for the last 365 days
        #3d: add "New" and "Update "counts to the general count for that specific day
        


        # END DAILYGRAPH
        


        #This is to be used by the user bar
        cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
        if cu_user_doc:

            #data['cu_actualname'] = cu_user_doc['name']
            data['cu_profilepic'] = cu_user_doc['profilepic']
            #data['cu_location'] = cu_user_doc['location']
            #data['cu_handle'] = current_user.id

        #Thisi is the data from the handle we are visiting
        if current_user.id == handle:
            data['handle_actualname'] = cu_user_doc['name']
            data['handle_profilepic'] = cu_user_doc['profilepic']
            data['handle_location'] = cu_user_doc['location']

        else:
            handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
            if handle_user_doc:
                data['handle_actualname'] = handle_user_doc['name']
                data['handle_profilepic'] = handle_user_doc['profilepic']
                data['handle_location'] = handle_user_doc['location']
    

        
        peopleteams = MAM.is_org(handle) 
        if peopleteams: 
            #This is an organization         
            data['people'] = peopleteams['people'] 
            data['peoplethumbnails'] = {}
            for person in peopleteams['people']:
                #get the profilepic for this person
                person_user_doc = MAM.select_user_doc_view('auth/userbasic',person['handle'])
                if person_user_doc:
                    data['peoplethumbnails'][person['handle']] = person_user_doc['profilepic']

            data['teammembership'] = {}
            allteams = {}
            for teamd in peopleteams['teams']:
                teamd['count']=len(teamd['members'])
                for member in teamd['members']:
                    if current_user.id == member['handle']:
                        if teamd['teamname'] == 'owner':
                            data['teammembership'][teamd['teamname']] = 'org_owner'
                        else:
                            if len(teamd['roles']) >= 1:
                                data['teammembership'][teamd['teamname']] = teamd['roles'][-1]['role']
                
                allteams[teamd['teamname']] = 'org_owner'

            if 'owner' in data['teammembership']:
                data['teammembership'] = allteams


            data['teams'] = peopleteams['teams']

            data['template'] = 'avispa_rest/orghome.html'
        else:
            #This is a regular user
         
            data['organizations'] = MAM.user_orgs(handle)
            data['template'] = 'avispa_rest/userhome.html'
     
        return render_template(data['template'], data=data)

    else:
        data['redirect'] = '/'+current_user.id+'/_home'
        return data

def role_dispatcher(depth,handle,ring=None,idx=None,collection=None,api=False):

    ARR = AvispaRolesRestFunc()


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

    data = getattr(ARR, m.lower())(request,depth,handle,ring,idx,collection,api=api)

    data['handle']=handle
    data['ring']=ring
    data['idx']=idx
    data['collection']=collection
    data['current_user']=current_user

    data['depth_a'] = ['get_a','post_a','put_a','delete_a']
    data['depth_a_b'] = ['get_a_b','post_a_b','put_a_b','delete_a_b']
    data['depth_a_b_c'] = ['get_a_b_c','post_a_b_c','put_a_b_c','delete_a_b_c']
    

    t = time.time()
    data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))

    

    if 'error_status' in data.keys():
        status = int(data['error_status'])
    else:
        status = 200

    if 'redirect' in data:
        return data             
    elif request.headers.get('Accept') and request.headers.get('Accept').lower() == 'application/json':     
        return render_template(data['template'], data=data), status     
    else:
        return render_template(data['template'], data=data)

    

def people_dispatcher(depth,handle,person=None):

    APR = AvispaPeopleRestFunc()
    MAM = MainModel()
    data = {}

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


    #depth = '_a_p'
    authorization_result = MAM.user_is_authorized(current_user.id,m.lower(),depth,handle)
    if not authorization_result['authorized']:
        return render_template('avispa_rest/error_401.html', data=data),401
    data['user_authorizations'] = authorization_result['user_authorizations']
    
    
    data.update(getattr(APR, m.lower())(request,handle,person))

    
    data['handle'] = handle

    #This is to be used by the user bar
    cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    if cu_user_doc:

        #data['cu_actualname'] = cu_user_doc['name']
        data['cu_profilepic'] = cu_user_doc['profilepic']
        #data['cu_location'] = cu_user_doc['location']
        #data['cu_handle'] = current_user.id

    #Thisi is the data from the handle we are visiting
    if current_user.id == handle:
        data['handle_actualname'] = cu_user_doc['name']
        data['handle_profilepic'] = cu_user_doc['profilepic']
        data['handle_location'] = cu_user_doc['location']

    else:
        handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
        if handle_user_doc:
            data['handle_actualname'] = handle_user_doc['name']
            data['handle_profilepic'] = handle_user_doc['profilepic']
            data['handle_location'] = handle_user_doc['location']


    if 'redirect' in data:
        return data                 
    else:
        return render_template(data['template'], data=data)


def teams_dispatcher(depth,handle,team=None):

    ATR = AvispaTeamsRestFunc()
    MAM = MainModel()
    data = {}

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

    #depth = '_a_n'
    authorization_result = MAM.user_is_authorized(current_user.id,m.lower(),depth,handle,team=team)
    if not authorization_result['authorized']:
        return render_template('avispa_rest/error_401.html', data=data),401
    data['user_authorizations'] = authorization_result['user_authorizations']


    try:
        data.update(getattr(ATR, m.lower())(request,handle,team))
    except(AttributeError):
        data['template'] = 'avispa_rest/error_404.html'

    data['handle'] = handle


        #This is to be used by the user bar
    cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
    if cu_user_doc:

        #data['cu_actualname'] = cu_user_doc['name']
        data['cu_profilepic'] = cu_user_doc['profilepic']
        #data['cu_location'] = cu_user_doc['location']
        #data['cu_handle'] = current_user.id

    #Thisi is the data from the handle we are visiting
    if current_user.id == handle:
        data['handle_actualname'] = cu_user_doc['name']
        data['handle_profilepic'] = cu_user_doc['profilepic']
        data['handle_location'] = cu_user_doc['location']

    else:
        handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
        if handle_user_doc:
            data['handle_actualname'] = handle_user_doc['name']
            data['handle_profilepic'] = handle_user_doc['profilepic']
            data['handle_location'] = handle_user_doc['location']


    if 'redirect' in data:
        return data                 
    else:
        return render_template(data['template'], data=data)
    


# Set the route and accepted methods
@avispa_rest.route('/')
@login_required
def index():

    data = {}
    data['handle']='x' #you have to grab this from the session user
    #return render_template("avispa_rest/intro.html", data=data)
    return redirect('/'+current_user.id+'/_home')


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
#This is needed because in a Vanilla install there are no users so /_tools/install would redirect me to /_login
def first_install():

    #result = route_dispatcher('_a_b','_tools','install')
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
#The home of user <handle>
def home(handle):

    result = home_dispatcher(handle)
 
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

    result = teams_dispatcher('_a_m_n',handle,team)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/<handle>/_teams/<team>/_settings', methods=['GET','POST','PUT','PATCH','DELETE'])
#The home of user <handle>
def teams_a_m_n_settings(handle,team):

    result = teams_dispatcher('_a_m_n_settings',handle,team)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result




@avispa_rest.route('/_roles/<handle>', methods=['GET'])
@login_required
def roles_a(handle):
    
    result = role_dispatcher('_a',handle)

    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_roles/<handle>/<ring>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def roles_a_b(handle,ring):
    
    result = role_dispatcher('_a_b',handle,ring)

    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result
    

@avispa_rest.route('/_roles/<handle>/<ring>/<idx>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def roles_a_b_c(handle,ring,idx):
    
    result = role_dispatcher('_a_b_c',handle,ring,idx)

    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/_roles/<handle>/_collection', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def roles_a_x(handle,collection):
    
    result = role_dispatcher('_a_x',handle)

    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/_roles/<handle>/_collection/<collection>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def roles_a_x_y(handle,collection):
    
    result = role_dispatcher('_a_x_y',handle,collection)
    
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

    if ('rq' not in request.args) and ('method' not in request.args): 
        print('FLAGx1')
        result = route_dispatcher('_a',handle,collection=collection)       
    elif request.method == 'POST':
        if 'method' in request.args:
            if request.args.get('method').lower()=='put':
                print('FLAGx2')
                result = collection_dispatcher('_a_x_y',handle,collection) 
            elif request.args.get('method').lower()=='post':
                print('FLAGx3')
                result = route_dispatcher('_a',handle,collection=collection)
        else:
            print('FLAGx4')
            result = route_dispatcher('_a',handle,collection=collection)

    elif 'rq' in request.args:
        if request.args.get('rq').lower() == 'put':
            print('FLAGx5')
            result = collection_dispatcher('_a_x_y',handle,collection)
        if request.args.get('rq').lower() == 'post':
            print('FLAGx6')
            result = route_dispatcher('_a',handle,collection=collection)


    else:
        print('FLAGx7')
        #Every collection specific GET
        result = collection_dispatcher('_a_x_y',handle,collection)
 
    if 'redirect' in result:
        #pass
        return redirect(result['redirect'])        
    else:
        return result

@avispa_rest.route('/<handle>/_collections/<collection>/<ring>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def collections_route_a_x_y_b(handle,collection,ring):

    result = route_dispatcher('_a_b',handle,ring,collection=collection)

    if 'redirect' in result:
        return redirect(result['redirect'])
    else:
        return result

@avispa_rest.route('/<handle>/_collections/<collection>/<ring>/<idx>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def collections_route_a_x_y_b_c(handle,collection,ring,idx):

    result = route_dispatcher('_a_b_c',handle,ring,idx,collection=collection)

    if 'redirect' in result:
        return redirect(result['redirect'])
    else:
        return result


@avispa_rest.route('/<handle>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
@login_required
def route_a(handle):

    if request.method == 'GET':
        if ('rq' not in request.args) and ('method' not in request.args):         
            return redirect('/'+handle+'/_home')

    #if handle != current_user.id:
     #   return redirect('/_logout') 

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

    










