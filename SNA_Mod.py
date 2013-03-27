'''
Created on Nov 24, 2012

@author: nicolas
'''
'''
Created on May 16, 2012

@author: nicolas
Carga Coleccion de Mongo en un graph de networkx
'''
import os,sys
import csv
import string
import json
import networkx as net
from decimal import *
from collections import Counter
#import twitter_text


STOPWORDS="stopWords.csv"
DB = "gnip"
COL="gnip_politica"
LIMIT=100000
TRIAD_TARGET='300'

def entity_count_mapper(tweet):
    for ele in tweet:
        print ele
        
        
def create_graph(results_input):
    g=net.DiGraph()
    for results in results_input:
        for result in results:
            try:
                g.add_node(result['user']['screen_name'], 
                           name=result['user']['name'],
                           location=result['user']['location'])
            except Exception,e:
                if 'location' in e:
                    try:
                        g.add_node(result['user']['screen_name'], 
                                   name=result['user']['name'], 
                                   location= result['user']['time_zone'])
                    except Exception as e:
                        if 'location' in e:
                            g.add_node(result['user']['screen_name'], 
                                   name=result['user']['name'])
            if "user_mentions" in result:
                for user in result["user_mentions"]:
                    g.add_edge(result['user']['screen_name'],user["screen_name"],texto=result["text"])
            if 'retweet' in result:
                print 'here'
            
    return g                        

#def create_graph(results_input):  V1.0
#    g=net.DiGraph()
#    for result in results_input:
#        if len(result["twitter_entities"]["user_mentions"])>0:
#            for user in result["twitter_entities"]["user_mentions"]:
#                try:
#                    #cuando tengamos klout agregamos esto otra vez
##                    if "klout_score" in result["gnip"]:
##                        #print "adding %s" % result["actor"]["preferredUsername"]
##                        g.add_edge(result["actor"]["preferredUsername"],user["screen_name"],weight=result["gnip"]["klout_score"],regla=result["gnip"]["matching_rules"][0]["value"])
##                    else:
##                        # print "adding %s" % result["actor"]["preferredUsername"]
#                    #g.add_weighted_edges_from(result["from_user"],user["screen_name"],1,texto=result["text"])
#                    
#                    g.add_edge(result["from_user"],user["screen_name"],texto=result["text"],idioma=result["iso_language_code"])
#                except Exception,e:
#                    print e
#    return g

def freq_counter(files):
    cnt = Counter()
    total=0
    freq="["
    reader=csv.reader(open(os.path.join( os.path.dirname(sys.argv[0]), 'in',STOPWORDS)),delimiter=',', quotechar='"')
    stopList=[[row[0],1] for row in reader] #reading the stop list
    stopDict=dict(stopList)
    for results in files:
        for result in results:
            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation) #quita puntuacion
            textIn= result["text"].translate(remove_punctuation_map)
            for word in textIn.split():
                if word in stopDict:
                    pass
                else:
                    total+=1
                    cnt[word] += 1
    for element in cnt:
        if freq=="[":
            freq+='{"palabra":"'+element+'", "frecuencia": "'+str(Decimal(cnt[element])/Decimal(total))+'"}'
        else:
            freq+=',{"palabra":"'+element+'", "frecuencia": "'+str(Decimal(cnt[element])/Decimal(total))+'"}'
    freq+="]"
    return json.loads(freq),cnt
        
def save_to(input_file,file_name):
    print "saving to %s" %os.path.join( os.path.dirname(sys.argv[0]), 'out',file_name )
    if not os.path.isdir('out'):
        os.mkdir('out')
    f = open(os.path.join( os.path.dirname(sys.argv[0]), 'out',file_name ), 'w')
    f.write("Usuario,Numero de triadas de tipo %s\n" %TRIAD_TARGET)
    for user in input_file:
        f.write("%s,%s\n"%(user[1],user[0]))
    f.close()
    
def save_to_gml(graph,path):
    net.write_gml(graph,path)
    
def save_to_gexf(graph,path):
    net.write_gexf(graph, path)

def save_to_graphml(graph,path):
    net.write_graphml(graph, path)


def create_insta_likes_graph(results):
    g=net.DiGraph()
    for result in results:
        try:
            g.add_node(result['user']['username'], nombre_completo=result['user']['full_name'],id=result['user']['id'],link=result['link'])
        except Exception as e:
            print e
        if result['likes']['count']>0:
            for like in result['likes']['data']:
                g.add_node(like['username'], nombre_completo=like['full_name'],id=like['id'])
                g.add_edge(like['username'],result['user']['username'])
        if result['comments']['count']>0:
            for comment in result['comments']['data']:
                g.add_edge(comment['from']['username'],result['user']['username'],comment=comment['text'].encode("utf8","ignore"))
                g.add_node(comment['from']['username'], dict(nombre_complet=comment['from']['full_name'],id=comment['from']['id']),created=comment['created_time'])
    return g


def create_insta_friends_graph(parent, friends, graph=None):
    if graph:
        g=graph
    else:
        g=net.DiGraph()
    g.add_node(parent['username'],nombre_completo=parent['full_name'],id=parent['id'])
    for friend in friends:
        g.add_edge(parent['username'],friend['username'])
        g.add_node(friend['username'],nombre_completo=friend['full_name'],id=friend['id'])
    return g
       
#def calculate_triads(results,day_start):
#    print "creando red...\n"
#    tweet_graph=create_graph(results)
#    # seleccionar solo componentes conectados
#    print "calculando componentes...\n"
#    components=net.connected_component_subgraphs(tweet_graph)
#    # seleccionamos el componente mas grande
#    cc=components[0]
#    print components
#    print "calculando triadas....\n"
#    census,node_census=triadic.triadic_census(cc)
#    closed_triads=[[-k,v]for k,v in sorted ([[-node_census[k][TRIAD_TARGET],k]for k in node_census.keys()])]
#    return closed_triads
    