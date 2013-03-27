'''
Created on Feb 12, 2013

@author: nicolas
'''
import sys, os
import datetime
import Includes.instagram  as instagram
from Includes.instagram import client, subscriptions
import json
from SNA_Mod import create_insta_likes_graph as create_likes_graph
from SNA_Mod import save_to_gexf, create_insta_friends_graph as create_friends_graph
from Includes.instagram.oauth2 import OAuth2AuthExchangeError

CONFIG = {
    'client_id': '421812b047504600b13f296a1d1a0706',
    'client_secret': '18f82125712848488034def45511c8c9',
    'redirect_uri': 'https://www.wissenmedia.com'
}


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
    
    
def friends_network(levels,api,media,graph=None):
    #creates the network with the levels specified  
    user_id =media['user']['id']
    try:
        friends, next=api.user_followed_by(user_id)
        if graph:
            friends_graph=create_friends_graph(media['user'],friends,graph)
        else:
            friends_graph=create_friends_graph(media['user'],friends)
        return friends_graph,friends
    except Exception as e:
        return e
  
    
def insta_search(search,geo):
    save=True
    lugar= geo.split(',')
    query=search+'_'+lugar[0]+'_'+lugar[1]+'_'+lugar[2]
    
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
    insta_results = unauthenticated_api.media_search(q=search, lat=lugar[0], lng=lugar[1], distance=lugar[2])
        #add processing to get user info
    save_json(insta_results,query)
    friends_json= post_processing(insta_results,unauthenticated_api,query)
    return insta_results,friends_json
    
    
def post_processing(insta_results, unauthenticated_api,query):
    friends_graph=None
    #Dock.insta_json_csv(insta_results, type='likes')
    graph= create_likes_graph(insta_results)
    save_to_gexf(graph,os.path.join(os.path.dirname(sys.argv[0])+'/out/gexf'+query+'.gexf'))
    for media in insta_results:
        if friends_graph:
            friends_graph,friends_json=friends_network(1,unauthenticated_api,media,graph=friends_graph)
        else:
            friends_graph,friends_json=friends_network(1,unauthenticated_api,media)
    save_to_gexf(friends_graph,os.path.join(os.path.dirname(sys.argv[0])+'/out/gexf'+query+'_friends.gexf'))
    return friends_json
    #Dock.insta_json_csv(friends_json, type='friends')
#        users, next=unauthenticated_api.user_followed_by(media.user.id)
#        print media.user.username +' followed by:'
#        for user in users:
#            print user.username
#            print '\n'
#        print 'done'