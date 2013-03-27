'''
Created on 09/05/2012

@author: Nicolas
'''
'''
Created on 08/05/2012

@author: Nicolas
'''
import pprint
import Includes.networkx as net
import urllib
#import matplotlib
#import pylab
#import matplotlib.pyplot as plot


def sorted_map(map):
    ms=sorted(map.iteritems(),key=lambda(k,v):(-v,k))
    return ms

def trim_degrees(g,degree=1):
    g2=g.copy()
    d=net.degree(g2)
    for n in g2.nodes():
        if d[n]<=degree:g2.remove_node(n)
    return g2

def trim_edges(g,weight=1):
    g2=net.Graph()
    for f, to, edata in g.edges(data=True):
        if edata['weight']>weight:
            g2.add_edge(f,to,edata)
    return g2

def island_method(g, iterations=5):
    weights=[edata['weight'] for f,to,edata in g.edges(data=True)]
    mn=int(min(weights))
    mx=int(max(weights))
    step=int((mx-mn)/iterations)
    return [[threshold,trim_edges(g,threshold)] for threshold in range(mn,mx,step)]

def getLjFriends(g,name):
    response=urllib.urlopen('http://www.livejournal.com/misc/fdata.bml?user='+name)
    for line in response.readlines():
        if line.startswith('#'):continue
        parts=line.split()
        if len(parts)==0: continue
        if parts[0]=='<':
            g.add_edge(parts[1],name)
        else:
            g.add_edge(name,parts[1])
    return g

def snowBallSampling(g,center,max_depth=2,current_depth=0,taboo_list=[]):
    print center,current_depth,max_depth,taboo_list
    if current_depth==max_depth:
        print 'to deep'
        return taboo_list
    if center in taboo_list:
        return taboo_list
    else:
        taboo_list.append(center)
    getLjFriends(g,center)
    for node in g.neighbors(center):
        taboo_list=snowBallSampling(g,node,current_depth=current_depth+1,max_depth=max_depth,taboo_list=taboo_list)
    return taboo_list

    