# Import flask dependencies
import urlparse, time, datetime, collections, json, csv, types, cStringIO
import logging
from AvispaLogging import AvispaLoggerAdapter

from flask import Blueprint,render_template,request,redirect,g,make_response,Response
from AvispaRestFunc import AvispaRestFunc
from AvispaCollectionsRestFunc import AvispaCollectionsRestFunc
from AvispaRolesRestFunc import AvispaRolesRestFunc
from AvispaPeopleRestFunc import AvispaPeopleRestFunc
from AvispaTeamsRestFunc import AvispaTeamsRestFunc
from MyRingTool import MyRingTool
from MyRingPatch import MyRingPatch
from ElasticSearchModel import ElasticSearchModel
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from default_config import IMAGE_FOLDER_NAME
from env_config import IMAGE_FOLDER_NAME, IMAGE_CDN_ROOT, TEMP_ACCESS_TOKEN,URL_SCHEME
from MainModel import MainModel


avispa_rest = Blueprint('avispa_rest', __name__, url_prefix='')

logger = logging.getLogger('Avispa')
#lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})
lggr = AvispaLoggerAdapter(logger, {'tid': '0','ip': '0'})
lggr.debug('Controller start')

#It is very important to leave url_prefix empty as all the segments will be dynamic

def setup_log_vars():
    MAM = MainModel()
    
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers.get('X-Forwarded-For')
    else:
        ip = request.remote_addr

    tid = MAM.random_hash_generator(36)

    return tid,ip

def setup_local_logger(tid,ip):
    return AvispaLoggerAdapter(logger, {'tid':tid,'ip':ip})
    

def route_dispatcher(depth,handle,ring=None,idx=None,api=False,collection=None):
      
    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    lggr.info('START route_dispatcher')

    MAM = MainModel(tid=tid,ip=ip)
    ARF = AvispaRestFunc(tid=tid,ip=ip)

    
    if request.args.get("rq"):
        method = request.args.get("rq")+'_rq'
    elif request.args.get("rs"):
        method = request.args.get("rq")+'_rs'
    elif request.args.get("method"):
        method = request.args.get("method")
    else:
        method = request.method

    data = {}

    m = method+depth
    data['method'] = m
    lggr.info('Route:%s',m)

    if api:

        

        lggr.debug('API call')       
        # PLEASE REMOVE TEMP_ACCESS_TOKEN with real OAuth access token  ASAP!
        lggr.debug('TEMP_ACCESS_TOKEN:'+str(TEMP_ACCESS_TOKEN))       
        # Load Balancer is not letting the headers pass. Will have to use args
        #lggr.info('Header:'+str(request.headers.get('access_token')))
        lggr.info('Arg:'+str(request.args.get('access_token')))

        if hasattr(current_user,'id'):
            user_handle = current_user.id

        elif request.args.get('access_token') == TEMP_ACCESS_TOKEN:
            lggr.info('TEMP_ACCESS_TOKEN matches!')
            user_handle = '_api_anonymous' #Please change this to the actual username that is using this token
        
        else:
            lggr.info('END route_dispatcher')
            return render_template('avispa_rest/error_401.html', data=data),401
 
        authorization_result = MAM.user_is_authorized(user_handle,m,depth,handle,ring=ring,idx=idx,api=api)

    if not api:

        lggr.info('Not an API call')
  
        authorization_result = MAM.user_is_authorized(current_user.id,m,depth,handle,ring=ring,idx=idx,api=api)
        
        if not authorization_result['authorized']:
            lggr.info('END route_dispatcher')
            return render_template('avispa_rest/error_401.html', data=data),401

        data['user_authorizations'] = authorization_result['user_authorizations']

        cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
        data['cu_actualname'] = cu_user_doc['name']
        data['cu_profilepic'] = cu_user_doc['profilepic']
        data['cu_location'] = cu_user_doc['location']


        if current_user.id == handle:
            data['handle_actualname'] = cu_user_doc['name']
            data['handle_profilepic'] = cu_user_doc['profilepic']
            data['handle_location'] = cu_user_doc['location']
            data['is_org'] = False

        else:
            handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
            if handle_user_doc:
                data['handle_actualname'] = handle_user_doc['name']
                data['handle_profilepic'] = handle_user_doc['profilepic']
                data['handle_location'] = handle_user_doc['location']
                if 'is_org' in handle_user_doc:
                    if handle_user_doc['is_org']:
                        data['is_org'] = True
                    else:
                        data['is_org'] = False

        
        if collection:       
            data['collection'] = collection
        else:
            data['collection'] = ''
        lggr.debug('COLLECTION: %s'%data['collection'])

        

        if request.args.get("raw"):
            data['raw'] = True 


        data['handle']=handle
        data['ring']=ring
        data['idx']=idx
        data['current_user']=current_user

        o = urlparse.urlparse(request.url)
        data['host_url'] = urlparse.urlunparse((URL_SCHEME, o.netloc, '', '', '', ''))
        data['api_url'] = urlparse.urlunparse((URL_SCHEME, o.netloc, '_api'+o.path, o.params, o.query, o.fragment))
        

        #search_path = '/'.join(o.path.split('/')[:-1])
        if collection:
            search_path = "/%s/_collections/%s/%s"%(handle,collection,ring)
        else:
            search_path = "/%s/%s"%(handle,ring)            

        data['search_url'] = urlparse.urlunparse(('', '', search_path,'', '', ''))


        data['image_cdn_root'] = IMAGE_CDN_ROOT

        t = time.time()
        data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))


    lggr.info('START RESTFUL FUNCTION')
    data.update(getattr(ARF, m.lower())(
                                        handle,
                                        ring,
                                        idx,
                                        api=api,
                                        collection=collection,
                                        rqurl=request.url,
                                        rqargs=request.args,
                                        rqform=request.form))

    lggr.info('END RESTFUL FUNCTION')

    data['collection'] = collection
    data['searchbox'] = True

    if 'status' in data.keys():
        status = int(data['status'])
    else:
        status = 200

    if 'redirect' in data:
        
        lggr.info('END route_dispatcher')     
        return data 

    elif api: 

        if 'accept' in request.args:
            accept = request.args.get("accept").lower()
        else:
            accept = 'json'
  

        print('ACCEPT:',accept)

        if accept=='csv':

            #This is where a function converts output into CSV.
            def generate(data_raw,fl=None,fl_names=None):

                d = data_raw['items']

                cvsdocIO = cStringIO.StringIO()
                writer = csv.writer(cvsdocIO , delimiter=',',quoting=csv.QUOTE_NONNUMERIC)

                #Generate the header first 
                humancsvheader = ['_id'] 
                csvheader = ['_id'] 
                for f in fl:

                    csvheader.append(f)
                    if fl_names:
                        humancsvheader.append(fl_names[f])
               

                if fl_names:
                    headerline = [ str(f) for f in humancsvheader]
                else:
                    headerline = [ str(f) for f in csvheader]
      

                #headerline = [ str(f) for f in csvheader]
                writer.writerow(headerline)

                # Add the items
                for row in d:
                    
                    line = [] 
                    print('row:',row)

                    for field in csvheader: 
                    # Fill the line with authorized data
                        
                        print('Field:',field)
                        if field in row:
                            #print('Field:',field)
                            #print('rowfield:',row[field])
                            v = row[field]
                            print(v)

                            if isinstance(v, list):
                                r = [str(p) for p in v]
                                line.append('|'.join(r))

                            else:
                                line.append(row[field])
                        else:
                            line.append('')
                    
                    strline = [ str(f) for f in line]
                    writer.writerow(strline)
                    #csvline = ','.join(strline) + '\n'
                    #csvdoc += csvline

                csvdoc = cvsdocIO.getvalue()
                cvsdocIO.close()
 
                lggr.info('END route_dispatcher')
                return csvdoc
            
            if 'fl' in request.args:
                fl = request.args.get("fl").lower().split(',')
            else:
                #fl = data['fieldnames']
                #fl = data['fieldlabels']
                fl = data['fieldids']

            if 'human' in request.args:
                csvout = generate(data['raw_out'],fl,data['fieldnames'])
            else:
                csvout = generate(data['raw_out'],fl)

            #print('csvout:',csvout)

            response = make_response(csvout)
            # This is the key: Set the right header for the response
            # to be downloaded, instead of just printed on the browser
            if idx:
                response.headers["Content-Disposition"] = "attachment; filename="+str(handle)+"_"+str(ring)+"_"+str(idx)+".csv"
            else:
                response.headers["Content-Disposition"] = "attachment; filename="+str(handle)+"_"+str(ring)+".csv"

            lggr.info('END route_dispatcher')
            return response

            #return Response(csvout), mimetype='text/csv')


        elif accept=='json':
            # By default we return JSON
            data['json_out'] = json.dumps(data['raw_out'])
            print('JSONOUT',data['json_out'])
            
            lggr.info('END route_dispatcher')
            return render_template(data['template'], data=data), status
     

    elif request.headers.get('Accept') and request.headers.get('Accept').lower() == 'application/json': 
        lggr.info('END route_dispatcher')   
        return render_template(data['template'], data=data), status     
    else:
        lggr.info('END route_dispatcher')
        return render_template(data['template'], data=data)
        
def tool_dispatcher(tool):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)
    
    MRT = MyRingTool()

    data = getattr(MRT, tool.lower())(request)
    
    if  hasattr(current_user,'id'):
        data['handle']=current_user.id
    data['current_user']=current_user

    o = urlparse.urlparse(request.url)
    data['host_url']=urlparse.urlunparse((URL_SCHEME, o.netloc, '', '', '', ''))

    t = time.time()
    data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))

    if 'redirect' in data:
        return data                 
    else:
        return render_template(data['template'], data=data)


def patch_dispatcher(patchnumber):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    MRP = MyRingPatch()
    patch = str(patchnumber)
    data = getattr(MRP, patch.lower())(request)
    
    if 'redirect' in data:
        return data              
    else:    
        return render_template(data['template'], data=data)


def index_dispatcher(handle,ring=None,idx=None,unindex=False):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)    

    ESM = ElasticSearchModel()

    if unindex:
        data = ESM.unindexer(handle,ring,idx)
    else:
        if ring:
            data = ESM.indexer(request.url,handle,ring,idx)
        else:
            data = ESM.handle_indexer(request.url,handle)

    if 'redirect' in data:
        return data              
    else:    
        return render_template(data['template'], data=data)


def collection_dispatcher(depth,handle,collection=None,idx=None,api=False):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    MAM = MainModel(tid=tid,ip=ip)
    ACF = AvispaCollectionsRestFunc(tid=tid,ip=ip)

    if request.args.get("rq"):
        method = request.args.get("rq")+'_rq'
    elif request.args.get("rs"):
        method = request.args.get("rq")+'_rs'
    elif request.args.get("method"):
        method = request.args.get("method")
    else:
        method = request.method

    #method = request.method

    data = {}

    m = method+depth
    

    data['method'] = m

    if not api:
        MAM = MainModel()
        authorization_result = MAM.user_is_authorized(
                                                     current_user.id,
                                                     m,
                                                     depth,
                                                     handle,
                                                     collection=collection)

        if not authorization_result['authorized']:
            return render_template('avispa_rest/error_401.html', data=data),401

        data['user_authorizations'] = authorization_result['user_authorizations']

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
            data['is_org'] = False

        else:
            handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
            if handle_user_doc:
                data['handle_actualname'] = handle_user_doc['name']
                data['handle_profilepic'] = handle_user_doc['profilepic']
                data['handle_location'] = handle_user_doc['location']

                if 'is_org' in handle_user_doc:
                    if handle_user_doc['is_org']:
                        data['is_org'] = True
                    else:
                        data['is_org'] = False



        data['handle']=handle
        data['collection']=collection
        data['idx']=idx
        data['current_user']=current_user

        o = urlparse.urlparse(request.url)
        data['host_url']=urlparse.urlunparse((URL_SCHEME, o.netloc, '', '', '', ''))

        data['image_cdn_root'] = IMAGE_CDN_ROOT

        t = time.time()
        data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))

    rqargs = request.args
    rqform = request.form
    rqurl = request.url

    data.update(getattr(ACF, m.lower())(
                                        handle,
                                        collection,
                                        idx,
                                        api=api,
                                        rqurl=request.url,
                                        rqargs=request.args,
                                        rqform=request.form))

    if 'status' in data.keys():
        status = int(data['status'])
    else:
        status = 200

    if 'redirect' in data:
        return data             
    elif api:     
        return render_template(data['template'], data=data), status     
    else:
        return render_template(data['template'], data=data)


def home_dispatcher(handle):
    
    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip) 

    MAM = MainModel(tid=tid,ip=ip)
    ACF = AvispaCollectionsRestFunc(tid=tid,ip=ip)

    data = {}
    
    if MAM.user_exists(handle):

        method= 'GET_a_home'
        data['method'] = method
        depth = '_a'  
        authorization_result = MAM.user_is_authorized(current_user.id,method,depth,handle)

        if 'authorized' not in authorization_result:
            return render_template('avispa_rest/error_401.html', data=data),401

        data['user_authorizations'] = authorization_result['user_authorizations']
 
        m = 'get_a_x'
           
        collectionsd = getattr(ACF, m.lower())(handle,None,None) 
        print('collectionsd:')
        print(collectionsd) 


        data['handle'] = handle
        #data['rings'] = rings
        data['collections'] = collectionsd

        data['image_cdn_root'] = IMAGE_CDN_ROOT


        '''
        
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
            
            ##self.lggr.debug('NEEDLE:',needle)
            h_new[str(needle)] = 0
            h_update[str(needle)] = 0
            h_generic[str(needle)] = 0
            needle = needle - one_day

        ##self.lggr.debug('h_new:',h_new)

            
        for ringx in ringcounts:
            ringdb = current_user.id+'_'+ringx
            ring_dac = MAM.select_ring_doc_view(ringdb,'ring/dailyactivity',current_user.id,5000)
            for item_dac in ring_dac:
                for n in item_dac['new']:
                    if n == str(today):
                        pass
                        #self.lggr.debug('NEW TODAY:',item_dac['new'][n])

                    if n in h_generic:
                        h_generic[n] += item_dac['new'][n]

                    
                    if n in h_new:
                        h_new[n] += item_dac['new'][n]
                    else:
                        h_new[n] = item_dac['new'][n]
                    

                for n in item_dac['update']:
                    if n == str(today):
                        pass
                        #self.lggr.debug('UPDATED TODAY:',item_dac['update'][n])

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


        # END DAILYGRAPH

        '''
        


        #This is to be used by the user bar
        cu_user_doc = MAM.select_user_doc_view('auth/userbasic',current_user.id)
        print('cu_user_doc:')
        print(cu_user_doc)
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
            data['is_org'] = False

        else:
            handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
            if handle_user_doc:
                data['handle_actualname'] = handle_user_doc['name']
                data['handle_profilepic'] = handle_user_doc['profilepic']
                data['handle_location'] = handle_user_doc['location']

                if 'is_org' in handle_user_doc:
                    if handle_user_doc['is_org']:
                        data['is_org'] = True
                    else:
                        data['is_org'] = False


        
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

            
            #data['collections'] = {}
            #data['collections']['collectionlistlen'] = 1
            #data['collections']['collectionlist'] = []
            if len(data['organizations'])!=0:
                if len(data['organizations'][0]['collections'])!=0:
                    collection_dict = data['organizations'][0]['collections'][0]
                    
                    collection_dict['valid'] = True
                    collection_dict['handle'] = data['organizations'][0]['handle']
                    collection_dict['external'] = True
                    #cd = []
                    #cd['collectionlist'].append(collection_dict)
                    #data['collections'] = cd
                    data['collections']['collectionlist'].append(collection_dict)
            #raise

     
        return render_template(data['template'], data=data)

    else:
        data['redirect'] = '/'+current_user.id+'/_home'
        return data


def history_dispatcher(handle,ring=None):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip) 

    MAM = MainModel(tid=tid,ip=ip) 

    data = {}
    
    if MAM.user_exists(handle):

        method= 'GET_a_home'
        data['method'] = method
        depth = '_a'  
        authorization_result = MAM.user_is_authorized(current_user.id,method,depth,handle)

        if 'authorized' not in authorization_result:
            return render_template('avispa_rest/error_401.html', data=data),401

        data['user_authorizations'] = authorization_result['user_authorizations']
        data['handle'] = handle
        data['image_cdn_root'] = IMAGE_CDN_ROOT


        ##DAC
        
        # Daily Activity Graph steps
        #0. Create the general count dictionary (with 365 slots)
        #1. Retrieve all rings for this handle. Use view myringusers:ring/count
        ringcounts = MAM.select_user_doc_view('rings/count',handle)
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

            h_new[str(needle)] = 0
            h_update[str(needle)] = 0
            h_generic[str(needle)] = 0
            needle = needle - one_day
        
        timeline = {}
            
        for ringx in ringcounts:
            ringdb = handle+'_'+ringx
            ring_dac = MAM.select_ring_doc_view(ringdb,'ring/dailyactivity',batch=5000,showall=True)


            #All the for loops below are very short. Should not cause lag

            for item_dac in ring_dac:
 
                for t in item_dac['value']:

                    # t is the history type. It could be 'new', 'update', etc
                    # item_dac['value'][t] is a date

                    for q in item_dac['value'][t]:
                        # q is a date

                        if q not in timeline:
                            timeline[q] = []

                        if len(item_dac['value'][t])>0:
                            parts = ringdb.split('_',1)


                            timeline[q].append({
                                                'id':item_dac['id'],
                                                'author':item_dac['key'],
                                                'action':t,
                                                'size':item_dac['value'][t][q],
                                                'handle': parts[0],
                                                'ring':parts[1]})
                


                for n in item_dac['value']['new']:
                    if n == str(today):
                        pass

                    date = n[:10]

                    if date in h_generic:
                        h_generic[date] += item_dac['value']['new'][n]

                    
                    if date in h_new:
                        h_new[date] += item_dac['value']['new'][n]
                    else:
                        h_new[date] = item_dac['value']['new'][n]
                    

                for n in item_dac['value']['update']:

                    if n == str(today):
                        pass
                        #self.lggr.debug('UPDATED TODAY:',item_dac['update'][n])

                    date = n[:10]

                    if n in h_generic:
                        h_generic[date] += item_dac['value']['update'][n]
                    
                    
                    if n in h_update:
                        h_update[date] += item_dac['value']['update'][n]
                    else:
                        h_update[date] = item_dac['value']['update'][n]

        data['timeline'] = collections.OrderedDict(sorted(timeline.items(), key=lambda t: t[0],reverse=True))
   

        #data['dac_totals_date'] = h_generic
        data['dac_totals_date'] = h_generic

        totals_list = [ h_generic.get(k, 0) for k in h_generic]
        for tl in totals_list:
            if tl==0:
                del tl

        # [::-1] is used to reverse a list 
        data['dac_totals'] = totals_list[::-1]



        # END DAILYGRAPH

        ## END DAC DAC
        


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
            data['is_org'] = False

        else:
            handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
            if handle_user_doc:
                data['handle_actualname'] = handle_user_doc['name']
                data['handle_profilepic'] = handle_user_doc['profilepic']
                data['handle_location'] = handle_user_doc['location']

                if 'is_org' in handle_user_doc:
                    if handle_user_doc['is_org']:
                        data['is_org'] = True
                    else:
                        data['is_org'] = False


        
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

            data['template'] = 'avispa_rest/history.html'
        else:
            #This is a regular user
         
            
            data['template'] = 'avispa_rest/history.html'

     
        return render_template(data['template'], data=data)

    else:
        data['redirect'] = '/'+current_user.id+'/_home'
        return data
    

def people_dispatcher(depth,handle,person=None):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    MAM = MainModel(tid=tid,ip=ip)
    APR = AvispaPeopleRestFunc(tid=tid,ip=ip)

    data = {}
    data['section'] = '_people'
    data['image_cdn_root'] = IMAGE_CDN_ROOT

    if request.args.get("rq"):
        method = request.args.get("rq")+'_rq'
    elif request.args.get("rs"):
        method = request.args.get("rq")+'_rs'
    elif request.args.get("method"):
        method = request.args.get("method")
    else:
        method = request.method

    #method = request.method
    m = method+depth

    data['method'] = m


    #depth = '_a_p'
    authorization_result = MAM.user_is_authorized(current_user.id,m.lower(),depth,handle)
    if not authorization_result['authorized']:
        return render_template('avispa_rest/error_401.html', data=data),401
    data['user_authorizations'] = authorization_result['user_authorizations']
    
    
    data.update(getattr(APR, m.lower())(
                                        handle,
                                        person,
                                        rqform=request.form))

    
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
        data['is_org'] = False

    else:
        handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
        if handle_user_doc:
            data['handle_actualname'] = handle_user_doc['name']
            data['handle_profilepic'] = handle_user_doc['profilepic']
            data['handle_location'] = handle_user_doc['location']

            if 'is_org' in handle_user_doc:
                if handle_user_doc['is_org']:
                    data['is_org'] = True
                else:
                    data['is_org'] = False


    if 'redirect' in data:
        return data                 
    else:
        return render_template(data['template'], data=data)



def teams_dispatcher(depth,handle,team=None):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    MAM = MainModel(tid=tid,ip=ip)
    ATR = AvispaTeamsRestFunc(tid=tid,ip=ip)

    data = {}
    data['section'] = '_teams'
    data['image_cdn_root'] = IMAGE_CDN_ROOT

    if request.args.get("rq"):
        method = request.args.get("rq")+'_rq'
    elif request.args.get("rs"):
        method = request.args.get("rq")+'_rs'
    elif request.args.get("method"):
        method = request.args.get("method")
    else:
        method = request.method

    #method = request.method
    m = method+depth
    data['method'] = m

    #depth = '_a_n'
    authorization_result = MAM.user_is_authorized(current_user.id,m.lower(),depth,handle,team=team)
    if not authorization_result['authorized']:
        return render_template('avispa_rest/error_401.html', data=data),401
    data['user_authorizations'] = authorization_result['user_authorizations']


    try:
        data.update(getattr(ATR, m.lower())(
                                            handle,
                                            team,
                                            rqform=request.form,
                                            rqargs=request.args))
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
        data['is_org'] = False

    else:
        handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
        if handle_user_doc:
            data['handle_actualname'] = handle_user_doc['name']
            data['handle_profilepic'] = handle_user_doc['profilepic']
            data['handle_location'] = handle_user_doc['location']

            if 'is_org' in handle_user_doc:
                if handle_user_doc['is_org']:
                    data['is_org'] = True
                else:
                    data['is_org'] = False



    if 'redirect' in data:
        return data                 
    else:
        return render_template(data['template'], data=data)



def labels_dispatcher(depth,handle,ring):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    MAM = MainModel(tid=tid,ip=ip)
    ALR = AvispaLabelsRestFunc(tid=tid,ip=ip)

    data = {}
    data['section'] = '_teams'
    data['image_cdn_root'] = IMAGE_CDN_ROOT

    if request.args.get("rq"):
        method = request.args.get("rq")+'_rq'
    elif request.args.get("rs"):
        method = request.args.get("rq")+'_rs'
    elif request.args.get("method"):
        method = request.args.get("method")
    else:
        method = request.method

    #method = request.method
    m = method+depth
    data['method'] = m

    #depth = '_a_n'
    authorization_result = MAM.user_is_authorized(current_user.id,m.lower(),depth,handle,team=team)
    if not authorization_result['authorized']:
        return render_template('avispa_rest/error_401.html', data=data),401
    data['user_authorizations'] = authorization_result['user_authorizations']


    try:
        data.update(getattr(ALR, m.lower())(request,handle,team))
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
        data['is_org'] = False

    else:
        handle_user_doc = MAM.select_user_doc_view('auth/userbasic',handle)
        if handle_user_doc:
            data['handle_actualname'] = handle_user_doc['name']
            data['handle_profilepic'] = handle_user_doc['profilepic']
            data['handle_location'] = handle_user_doc['location']

            if 'is_org' in handle_user_doc:
                if handle_user_doc['is_org']:
                    data['is_org'] = True
                else:
                    data['is_org'] = False



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

    #self.lggr.debug('IMAGE SERVED using Flask: /_images/'+depth1+'/'+depth2+'/'+filename)

    avispa_rest.static_folder=IMAGE_FOLDER_NAME+'/'+depth1+'/'+depth2
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

    result = teams_dispatcher('_a_m_n',handle,team)
 
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
        result = route_dispatcher('_a',handle,api=True,collection=collection)       
    elif request.method == 'POST':
        if 'method' in request.args:
            if request.args.get('method').lower()=='put':
                result = collection_dispatcher('_a_x_y',handle,api=True,collection=collection) 
            elif request.args.get('method').lower()=='post':
                result = route_dispatcher('_a',handle,api=True,collection=collection)
        else:
            result = route_dispatcher('_a',handle,api=True,collection=collection)

    elif 'rq' in request.args:
        if request.args.get('rq').lower() == 'put':
            result = collection_dispatcher('_a_x_y',handle,api=True,collection=collection)
        if request.args.get('rq').lower() == 'post':
            result = route_dispatcher('_a',handle,api=True,collection=collection)


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

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)
    lggr.debug('flag1');

    if ('rq' not in request.args) and ('method' not in request.args): 

        #result = route_dispatcher('_a',handle,collection=collection) 
        #We are assuming that not having a collection specific page is ok?
        result = home_dispatcher(handle)  

    elif request.method == 'POST':
        if 'method' in request.args:
            if request.args.get('method').lower()=='put':
                # Put the Collection metadata
                result = collection_dispatcher('_a_x_y',handle,collection) 
            elif request.args.get('method').lower()=='post':
                # Post the Ring
                result = route_dispatcher('_a',handle,collection=collection)
        else:
            # Post the ring
            result = route_dispatcher('_a',handle,collection=collection)

    elif 'rq' in request.args:
        if request.args.get('rq').lower() == 'put':
            # Show the form to Edit the Collection metadata
            result = collection_dispatcher('_a_x_y',handle,collection)
        if request.args.get('rq').lower() == 'post':
            # Get the Ring Modeler
            result = route_dispatcher('_a',handle,collection=collection)

    else:
        #Every collection specific GET
        result = collection_dispatcher('_a_x_y',handle,collection)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result


@avispa_rest.route('/_api/<handle>/_collections/<collection>/<ring>', methods=['GET', 'POST','PUT','PATCH','DELETE'])
def api_collections_route_a_x_y_b(handle,collection,ring):


    result = route_dispatcher('_a_b',handle,ring,api=True,collection=collection)

    if 'redirect' in result:
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



#API
@avispa_rest.route('/_api/<handle>', methods=['GET','POST'])
def api_route_a(handle):

    result = route_dispatcher('_a',handle,api=True)
 
    if 'redirect' in result:
        return redirect(result['redirect'])        
    else:
        return result

#API
@avispa_rest.route('/_api/<handle>/<ring>', methods=['GET','POST'])
def api_route_a_b(handle,ring):

    result = route_dispatcher('_a_b',handle,ring,api=True)
 
    #if 'redirect' in result:
     #   return redirect(result['redirect'])        
    #else:
     #   return result

    return result

#API
@avispa_rest.route('/_api/<handle>/<ring>/<idx>', methods=['GET','POST'])
def api_route_a_b_c(handle,ring,idx):

    result = route_dispatcher('_a_b_c',handle,ring,idx,api=True)

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




    


