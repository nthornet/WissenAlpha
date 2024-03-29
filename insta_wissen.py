# -*- coding: utf-8 -*-
'''
Created on Feb 12, 2013

@author: nicolas
'''
import sys, os
import datetime
import Includes.instagram  as instagram
from Includes.instagram import client, subscriptions
import json
from Dock import to_unicode
from SNA_Mod import create_insta_likes_graph as create_likes_graph
from SNA_Mod import save_to_gexf, create_insta_friends_graph as create_friends_graph
from Includes.instagram.oauth2 import OAuth2AuthExchangeError

CONFIG = {
    'client_id': '421812b047504600b13f296a1d1a0706',
    'client_secret': '18f82125712848488034def45511c8c9',
    'redirect_uri': 'https://www.wissenmedia.com'
}
path=os.path.join(os.path.dirname(sys.argv[0]), 'out')
gexf_path=os.path.join(os.path.dirname(sys.argv[0]), 'out/gexf')
json_path=os.path.join(os.path.dirname(sys.argv[0]), 'out/json')
csv_path=os.path.join(os.path.dirname(sys.argv[0]), 'out/csv')

def save_json(results,query):
    now = datetime.datetime.now()
    strNow=now.strftime("%Y-%m-%d_%H_%M")
    Debug=True
    if Debug:
        f = open(os.path.join(os.path.dirname(sys.argv[0]), 'search_results_'+query+'.json'), 'w')
    else:
        f = open(os.path.join(os.path.dirname(sys.argv[0]), 'search_results_'+query+'_'+strNow+'.json'), 'w')
    f.write(json.dumps(results, indent=1))
    f.close()
    
def getCursor(link):
    if "cursor=" in link:
        start=link.find('cursor=')
        end=link.find('&')
        return link[start+len('cursor='):end]


def friends_network(levels,api,media,friends_graph=None):
    #creates the network with the levels specified  
    user_id =media['user']['id']
    try:
        friends, next=api.user_followed_by(user_id)
        while next:
            cursor_next=getCursor(next)
            if friends_graph:
                friends_graph=create_friends_graph(media['user'],friends,friends_graph)
            else:
                friends_graph=create_friends_graph(media['user'],friends)
            friends, next=api.user_followed_by(user_id, cursor=cursor_next)
        return friends_graph,friends
    except Exception as e:
        if 'not valid JSON' in e:
            print 'Hubo un error con el json pero se ha continuado con la operacion'
        friends_graph,friends
  
    
def insta_search(search,geo):
    save=True
    if geo:
        lugar= geo.split(',')
        query=search+'_'+lugar[0]+'_'+lugar[1]+'_'+lugar[2]
    else:
        lugar= None
    
    
    unauthenticated_api = client.InstagramAPI(**CONFIG)
    try:
        url = unauthenticated_api.get_authorize_url(scope=["likes","comments"])
        print 'Connect with Instagram: %s' % url
    except Exception, e:
        print e
    
    try:
        code= raw_input('cual es el codigo?')
        access_token = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            print 'Could not get access token'   
            api = client.InstagramAPI(access_token=access_token)
            try:
                recent_media, next = api.user_recent_media()
                photos = []
                for media in recent_media:
                    photos.append(media['images']['thumbnail']['url'])
                    print ''.join(photos)
            except instagram.bind.InstagramClientError as e:
                print "cant get user media"
    except OAuth2AuthExchangeError as e:
        print e
    if lugar:
        insta_results = unauthenticated_api.media_search(q=search, lat=lugar[0], lng=lugar[1], distance=lugar[2])
    else:
        insta_results = unauthenticated_api.media_search(q=search)
        #add processing to get user info
    save_json(insta_results,query)
    friends_json= post_processing(insta_results,unauthenticated_api,query)
    return insta_results,friends_json
    
    
def post_processing(insta_results, unauthenticated_api,query):
    friends_graph=None
    friends_json=None
    #Dock.insta_json_csv(insta_results, type='likes')
    graph= create_likes_graph(insta_results)
    gexf_filename='search_results_'+query+'.gexf'
    save_to_gexf(graph,gexf_path+'/'+gexf_filename)
    for media in insta_results:
        if friends_graph:
            try:
                friends_graph,friends_json=friends_network(1,unauthenticated_api,media,friends_graph=friends_graph)
            except Exception as e:
                print e
        else:
            friends_graph,friends_json=friends_network(1,unauthenticated_api,media)
    gexf_filename='search_results_'+query+'_friends.gexf'
    save_to_gexf(graph,gexf_path+'/'+gexf_filename)
    return friends_json
    #Dock.insta_json_csv(friends_json, type='friends')
#        users, next=unauthenticated_api.user_followed_by(media.user.id)
#        print media.user.username +' followed by:'
#        for user in users:
#            print user.username
#            print '\n'
#        print 'done'