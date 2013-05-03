# -*- coding: utf-8 -*-
'''
Created on Feb 14, 2013

@author: nicolas
'''
import Includes.twitter as twitter
from Includes.twitter import Status
import datetime
import sys,os
import json

APP_NAME = 'ThorneHarvester' 
CONSUMER_KEY = '68R3Ko3fjLyycenGbi3scQ' 
CONSUMER_SECRET = 'UlHLW4IT2ynvETI5vPy9rK8Kdu22Eyjp9Ekw5kFbZg'
ACCESS_TOKEN_KEY = '86863810-0eHImWsOim2LSAaNJMgpiSRv23Td8XmpboPcgZflA'
ACCESS_TOKEN_SECRET = '2Nqhcp2f4Ype3EfJHpD0LnPUCVvA7tblHsTjTHvExLY'

def save_json(results,query):
    now = datetime.datetime.now()
    strNow=now.strftime("%Y-%m-%d_%H_%M")
    Debug=True
    if Debug:
        f = open(os.path.join(os.path.dirname(sys.argv[0]), 'search_results_'+query+'.json'), 'w')
    else:
        f = open(os.path.join(os.path.dirname(sys.argv[0]), 'search_results_'+query+'_'+strNow+'.json'), 'w')
    try:
        f.write(results)
    except TypeError as e:
        print results + 'no es un archivo json'
    f.close()
    
    

#search_results= api.GetSearch('cocacola', '19.4341667,-99.1386111,10km', result_type='mixed', include_entities=True, query_users=True)

#cycles through trying to get all the results, if a page with no results is returned
#page_search is set to 15 so the while loop exits

def search_twitter(query, geocode, api):
    # pages_search tells max pages per search
    pages_search=15
    search_results={}
    page_search=1
    result_len=0
    while pages_search>=page_search:
        if page_search is 1:
            try:
                rate_limit=api.GetRateLimitStatus()
                if rate_limit['remaining_hits']>=50:
                    try:
                        search_results= api.GetSearch(query,
                                                      geocode,per_page=50, 
                                                      page= page_search,
                                                      result_type='recent',
                                                      include_entities=True, 
                                                      query_users=True)
                    except Exception as e:
                        print e
                else:
                    print 'Ya se ha llegado al limite de busquedas, espere una hora'
                result_len=len(search_results)
                
            except TypeError as e:
                pass
        else:
            rate_limit=api.GetRateLimitStatus()
            if rate_limit['remaining_hits']>=50:
                try:
                    search_results+= api.GetSearch(query,
                                                   geocode,
                                                   per_page=50, 
                                                   page= page_search, 
                                                   result_type='recent', 
                                                   include_entities=True, 
                                                   query_users=True)
                except Exception as e:
                    print e
            else:
                print 'Ya se ha llegado al limite de busquedas, espere una hora'
            if result_len is len(search_results):
                page_search=15
            else:
                result_len=len(search_results)
        page_search+=1
    if result_len>0:
        json_results="["
        for s in search_results:
            if json_results== "[":
                json_results+=Status.AsJsonString(s)
            else:
                json_results+=","+Status.AsJsonString(s)
        
        json_results+="]"
        #save_json(json_results,"json_results")
        return json_results          
    #save_json(json_results,query)

def get_trending(world_id,api):
    try:
        trial=api.GetTrendsWoeid(woeid=world_id)
        print trial
    except Exception as e:
        print e
    try:
        trial2= api.GetFriendsTimeline(user='TigranMimosa',count=100,retweets=True,include_entities=True)
        print trial2
    except Exception as e:
        print e
    try:
        trial3= api.GetStatus(id='2205941')
        print trial3
    except Exception as e:
        print e
    try:    
        trial4= api.UsersLookup(screen_name=['elcoco42','TigranMimosa'])
        print trial4
    except Exception as e:
        print e

def load_json(path,query):
    f = open(os.path.join(os.path.dirname(sys.argv[0]), 'search_results_'+query+'.json'), 'r')
    search_results=json.loads(f.read())
#api.GetSearch(term, geocode, since_id, max_id, until, per_page, page, lang, show_user, result_type, include_entities, query_users)
#    for search in search_results:
#        print 'text: '+ search.text.encode('utf-8','ignore')
#        print 'id: ' + str(search.id)
#        print 'user: '+ search.user.screen_name
#        try:
#            print 'Retweet count: ' + str(search.retweet_count)
#            if search.retweet_count is not None:
#                print 'not none'
#        except TypeError as e:
#            if 'NoneType' in e:
#                print 'Retweet count: 0'
#    
#        try:
#            print 'location: '+ str(search.location)
#        except TypeError as e:
#            if 'NoneType' in e:
#                print 'location: '
#        print '------------------------------------------------\n'

def set_up_api(consumer_key,consumer_secret,access_token_key,access_token_secret):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
    return api


#query='cocacola'
#geocode='19.4341667,-99.1386111,100km'
#world_id="116545"
#api=set_up_api(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)
#rate_limit=api.GetRateLimitStatus()
#retweet=[]
#if rate_limit['remaining_hits']>0:
#    twitter_search= search_twitter(query,geocode=geocode,api=api)
#    json_twitter=json.loads(twitter_search)
#    for ele in json_twitter:
#        try:
#            if ele["retweet_count"] and ele["retweet_count"]>0:
#                print 'here'
#        except Exception as e:
#            retweet+=api.GetRetweets(ele['id'])
#            if retweet != []:
#                print retweet
#            else:
#                pass
#    get_trending(world_id,api)
#    json_twitter=search_twitter(query,geocode=geocode,api=api)
