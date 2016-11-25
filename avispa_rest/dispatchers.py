# Import flask dependencies
import urlparse, time, datetime, collections, json, csv, types, cStringIO
import logging
from AvispaLogging import AvispaLoggerAdapter
from flask import render_template,request,make_response,url_for
from TypesController import TypesController
from CollectionsController import CollectionsController
from PeopleCollection import PeopleCollection
from TeamsCollection import TeamsCollection
from Tool import Tool
from Patch import Patch
from ElasticSearchModel import ElasticSearchModel
from flask.ext.login import current_user
from env_config import IMAGE_CDN_ROOT,TEMP_ACCESS_TOKEN,URL_SCHEME
from MainModel import MainModel

logger = logging.getLogger('Avispa')
lggr = AvispaLoggerAdapter(logger, {'tid': '0','ip': '0'})
lggr.debug('Controller start')

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

def types_dispatcher(depth,handle,ring=None,idx=None,api=False,collection=None):
      
    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    lggr.info('START types_dispatcher')

    MAM = MainModel(tid=tid,ip=ip)
    TYC = TypesController(tid=tid,ip=ip)

    
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
            lggr.info('END types_dispatcher')
            return render_template('avispa_rest/error_401.html', data=data),401
 
        authorization_result = MAM.user_is_authorized(user_handle,m,depth,handle,ring=ring,idx=idx,api=api)

    if not api:

        lggr.info('Not an API call')
  
        authorization_result = MAM.user_is_authorized(current_user.id,m,depth,handle,ring=ring,idx=idx,api=api)
        
        if not authorization_result['authorized']:
            lggr.info('END types_dispatcher')
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
        search_path = "/%s/%s"%(handle,ring)            

        data['search_url'] = urlparse.urlunparse(('', '', search_path,'', '', ''))


        data['image_cdn_root'] = IMAGE_CDN_ROOT

        t = time.time()
        data['today']= time.strftime("%A %b %d, %Y ",time.gmtime(t))


    lggr.info('START RESTFUL FUNCTION')
    data.update(getattr(TYC, m.lower())(
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
        
        lggr.info('END types_dispatcher')     
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
 
                lggr.info('END types_dispatcher')
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

            lggr.info('END types_dispatcher')
            return response


        elif accept=='json':
            # By default we return JSON
            data['json_out'] = json.dumps(data['raw_out'])
            print('JSONOUT',data['json_out'])
            
            lggr.info('END types_dispatcher')
            return render_template(data['template'], data=data), status
     

    elif request.headers.get('Accept') and request.headers.get('Accept').lower() == 'application/json': 
        lggr.info('END types_dispatcher')   
        return render_template(data['template'], data=data), status     
    else:
        lggr.info('END types_dispatcher')
        return render_template(data['template'], data=data)
        
def tool_dispatcher(tool):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)
    
    TOL = Tool()

    data = getattr(TOL, tool.lower())(request)
    
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

    PAT = Patch()
    patch = str(patchnumber)
    data = getattr(PAT, patch.lower())(request)
    
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
    '''
    This dispatcher takes care only for collection administrative functions
    '''

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    MAM = MainModel(tid=tid,ip=ip)
    COC = CollectionsController(tid=tid,ip=ip)

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

        #This is the data from the handle we are visiting
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

    data.update(getattr(COC, m.lower())(
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
    COC = CollectionsController(tid=tid,ip=ip)

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
           
        collectionsd = getattr(COC, m.lower())(handle,None,None) 
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

        #This is the data from the handle we are visiting
        handle_user_doc = MAM.select_user_doc_view('auth/userbyhandle',handle)
        if handle_user_doc:

            data['handle_actualname'] = handle_user_doc['name']

            #Grab the last reference only
            if 'profilepic' in handle_user_doc:
                parts = handle_user_doc['profilepic'].split(',')
                data['handle_profilepic'] = parts[-1]
            else:
                data['handle_profilepic'] = ''

            data['handle_location'] = handle_user_doc['location']
            data['handle_about'] = handle_user_doc['about']

            if 'is_org' in handle_user_doc:
                if handle_user_doc['is_org']:
                    data['is_org'] = True
                else:
                    data['is_org'] = False
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
                    data['name'] = person_user_doc['name']
                    data['location'] = person_user_doc['location']

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
        data['redirect'] = url_for('avispa_rest.home',
                         handle=current_user.id,
                         _external=True,
                         _scheme=URL_SCHEME)
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
        data['redirect'] = url_for('avispa_rest.home',
                         handle=current_user.id,
                         _external=True,
                         _scheme=URL_SCHEME)
        return data
    

def people_dispatcher(depth,handle,person=None):

    tid,ip = setup_log_vars()
    lggr = setup_local_logger(tid,ip)

    MAM = MainModel(tid=tid,ip=ip)
    PEC = PeopleCollection(tid=tid,ip=ip)

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
    
    
    data.update(getattr(PEC, m.lower())(
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
    TEC = TeamsCollection(tid=tid,ip=ip)

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
        data.update(getattr(TEC, m.lower())(
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

