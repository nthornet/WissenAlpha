# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2012

@author: nicolas
'''
import sys
import os
import json
import HTMLParser
#import pylab
import networkx as nx
from types import *
import NetX
import Includes.xlwt as xlwt
from datetime import datetime
import Includes.pytz as pytz

class Tweet:

    def __init__(self, 
                 from_sn=None, 
                 from_name=None, 
                 to_sn=None, 
                 to_name=None,  
                 idioma= None, 
                 lugar=None,
                 source=None, 
                 hashtag=None,
                 urls=None,
                 text=None,
                 creado=None,
                 protected=None):
        self.from_sn=from_sn
        self.from_name=from_name
        self.to_sn=to_sn
        self.from_name=from_name
        self.to_name=to_name
        self.idioma=idioma
        self.lugar=lugar
        self.source=source
        self.hashtag=hashtag
        self.urls=urls
        self.text=text
        self.creado=creado
        self.protected=protected
        
    def __iter__(self):
        for attr in dir(Tweet()):
            if not attr.startswith("__") and not callable(attr):
                yield attr  
        
    def fix_time(self,date):
        local = pytz.timezone ("America/Mexico_City")
        if '+0000' in date: 
            date=date.replace(' +0000','')
        naive = datetime.strptime (date, "%a %b %d %H:%M:%S %Y")
        naive=naive.replace(tzinfo=pytz.utc).astimezone(local)
        return naive.strftime('%d %b %Y %H:%M:%S')
        
    def load_json(self,json):
        if 'text' in json:
            self.text= json['text']
            
        if 'location' in json:
            self.lugar=json['location']
        elif 'location' in json['user']:
            self.lugar=json['user']['location']
        elif 'time_zone' in json['user']:
            self.lugar=json['user']['time_zone']
             
        if 'source' in json:
            h = HTMLParser.HTMLParser() 
            try:
                self.source = h.unescape(json['source'])
            except:
                self.source = json['source']
        
        if 'hashtags' in json:
                output=None
                for hashtag in json['hashtags']:
                    if output is None:
                        output="%s" %hashtag
                    else:
                        output+=", %s" %(hashtag)
                self.hashtag=output
        
        if 'user_mentions' in json:
            for user in json['user_mentions']:
                
                if self.to_name is None:
                    self.to_name= user['name']
                else:
                    self.to_name+= ", %s" %(user['screen_name'])
                    
                if self.to_sn is None:
                    self.to_sn= user['name']
                else:
                    self.to_sn+= ", %s" %(user['screen_name'])
                    
        if 'urls' in json:
            for url in json['urls']:
                print url
                
        if 'user' in json:
            if json['user']['name']:
                self.from_name=json['user']['name']
            if json['user']['screen_name']:
                self.from_sn=json['user']['screen_name']
            if json['user']['lang']:
                self.idioma=json['user']['lang']
            if json['user']['protected']:
                self.protected=json['user']['protected']
                
        if json['created_at']:
            self.creado=self.fix_time(json['created_at'])

class User:
    def __init__(self, 
                 creado=None, 
                 descripcion=None, 
                 favoritos=None, 
                 followers=None,  
                 friends= None,
                 lenguaje=None,
                 lugar=None,
                 nombre=None,
                 screen_name=None,
                 status=None,
                 protected=None):
        self.creado=creado
        self.descripcion=descripcion
        self.favoritos=favoritos
        self.followers=followers
        self.friends=friends
        self.lenguaje=lenguaje
        self.lugar=lugar
        self.nombre=nombre
        self.screen_name=screen_name
        self.status=status
        self.protected=protected
        
    def __iter__(self):
        for attr in dir(Tweet()):
            if not attr.startswith("__") and not callable(attr):
                yield attr  
        
    def fix_time(self,date):
        local = pytz.timezone ("America/Mexico_City")
        if '+0000' in date: 
            date=date.replace(' +0000','')
        naive = datetime.strptime (date, "%a %b %d %H:%M:%S %Y")
        naive=naive.replace(tzinfo=pytz.utc).astimezone(local)
        return naive.strftime('%d %b %Y %H:%M:%S')

    def load_json(self,json_user):
        if 'created_at' in json_user:
            try:
                self.creado=self.fix_time(json_user['created_at'])
            except Exception as e:
                print e
                self.creado=None
        if 'followers_count' in json_user:
            self.followers= json_user['followers_count']
        if 'friends_count' in json_user:
            self.friends= json_user['friends_count']
        if 'description' in json_user:
            self.descripcion= json_user['description']
        if 'favourites_count' in json_user:
            self.favoritos= json_user['favourites_count']
        if 'lang' in json_user:
            self.lenguaje= json_user['lang']
        if 'location' in json_user:
            self.lugar= json_user['location']
        if 'name' in json_user:
            self.nombre=json_user['name']
        if 'protected' in json_user:
            self.protected= json_user['protected']
        if 'screen_name' in json_user:
            self.screen_name=json_user['screen_name']
        if 'status' in json_user:
            if 'text' in json_user['status']:
                self.status=json_user['status']['text']
                
                

class Instagram:
    def __init__(self, 
                 creado=None, 
                 descripcion=None, 
                 favoritos=None, 
                 followers=None,  
                 friends= None,
                 lenguaje=None,
                 lugar=None,
                 nombre=None,
                 screen_name=None,
                 status=None,
                 protected=None):
        self.creado=creado
        self.descripcion=descripcion
        self.favoritos=favoritos
        self.followers=followers
        self.friends=friends
        self.lenguaje=lenguaje
        self.lugar=lugar
        self.nombre=nombre
        self.screen_name=screen_name
        self.status=status
        self.protected=protected
    
    
class Instagram_User:
    pass


def find_users(input_json):
    users=[]
    for item in input_json:
        if isinstance(item, list):
            for ele in item:
                if 'user' in ele:
                    if ele['user'] not in users:
                        users.append(ele['user'])
        else:
            if 'user' in item:
                if item['user'] not in users:
                    users.append(item['user'])
    return users
        


def loadJsons(paths):
    output=[]
    for path in paths:
        if os.path.isfile(path):
            raw_file=open(path).read()
#           try:
            output.append(json.loads(raw_file))
#            i=i+1
#            print "length "+str(len(output))+ " at count "+str(i)
#            except:
    return output

#def output_graph(inputGraph):
#    d=nx.degree(inputGraph)
#    ds=NetX.sorted_map(d)
#    names1=[x[0] for x in ds[0:10]]
#    c=nx.closeness_centrality(inputGraph)
#    cs=NetX.sorted_map(c)
#    names2=[x[0] for x in cs[0:10]]
#    b=nx.betweenness_centrality(inputGraph)
#    bs=NetX.sorted_map(b)
#    names3=[x[0] for x in bs[0:10]]
#    e=nx.eigenvector_centrality(inputGraph,max_iter=1000)
#    es=NetX.sorted_map(e)
#    names4=[x[0] for x in es[0:10]]
#    names =list(set(names1)|set(names2)|set(names3)|set(names4))
#    table=["Name","Degree","closeness","betweenness","eigenvector"]
#    table.append([[name,d[name],c[name],b[name],e[name]]for name in names])
#    pp = pprint.PrettyPrinter()
#    print "\nTable "
#    pp.pprint(table)
#    print"\ntop gossipers"
#    pp.pprint(es[:10])
    
#    nx.draw(inputGraph)
 #   pylab.show()
    
#    print >> sys.stderr, "number nodes:", inputGraph.number_of_nodes()
#    print >> sys.stderr, "Node degrees:", sorted(nx.degree(inputGraph))
    
def createProject(files):
    pass

def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
            return obj

def create_folders(path):
    if not os.path.isdir(path+'/out'):
        os.mkdir(path+'/out')
    if not os.path.isdir(path+'/out/gexf'):
        os.mkdir(path+'/out/gexf')
    if not os.path.isdir(path+'/out/json'):
        os.mkdir(path+'/out/json')
    if not os.path.isdir(path+'/out/csv'):
        os.mkdir(path+'/out/csv')
    if not os.path.isdir(path+'/in'):
        os.mkdir(path+'/in')
    if not os.path.isdir(path+'/in/projects'):
        os.mkdir(path+'/in/projects')
        
def read_project(prt_file):
    pass

def display_menu(menu,output=1):
    for option in menu:
        print '[%i] %s' % (option, menu[option]) 
        # Prompt the user
    if output==1:
        idx = int(raw_input('\nEscoge una Funcion: '))
    elif output==2:
        idx = raw_input('\nEscoge una Funcion: ')
    return idx

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&quot;",'"')
    s = s.replace("&amp;", "&")
    return s

def clean_source(s):
    s=unescape(s)
    s=s.replace('<a href="',"")
    s=s.replace('">',";")
    s=s.replace('</a>',"")
    return s
    
def combine_json(json_list):
    new_list = []
    for piece in json_list:
        json_piece=loadJsons([piece])
        for item in json_piece:
            if item not in new_list:
                new_list.append(item)

    return new_list
  
def user_csv(tweets):
    lst_out=[]
    counter=0
    found=False
    for tweet in tweets:
        counter+=1
        if counter % 5 == 0:
            print counter
        try:
            if lst_out == []:
                pass
            else:
                for user in lst_out:
                    if tweet['user']['name'] == user['name']:
                        found= True
            if found==False:
                lst_out.append(tweet['user'])            
        except Exception as e:
            print e
    return lst_out
            
def insta_json_csv(results, type):
    if type is 'friends':
        for result in results:
            print result
    elif type is 'like':
        for result in results:
            print result

def csv_tweet_inner (element, output, index_r, index_c, sheet):
    tweet_holder=Tweet()
    tweet_holder.load_json(element)
    for attr, value in tweet_holder.__dict__.iteritems(): #itterate over variables and their values
        if attr is 'mention' and value is not None:    
            for user in value:
                output+="Screen Name: %s, Nombres Real: %s , " %(user['to_sn'],user['to_name'])
            value=output
            output=""
        sheet.write(index_r,index_c,value)
        index_c+=1
    index_c=0
    index_r+=1
    return output, index_r, index_c, sheet
        
def json_csv_xlwt(input_json,type,proyecto,path):
    if type=="user": #prepara el json de usuarios para convertitlo en xls
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        filename=proyecto + '_user.xls'
        csv_file = path+"/" + filename
        while os.path.isfile(csv_file):
            print "ya existe "+ filename
            rewrite_menu={1:"sobre escribir",2:"cambiar nombre"}
            id=display_menu(rewrite_menu)
            if rewrite_menu[id]=="cambiar nombre":
                filename=raw_input('\nQue nombre le quieres poner al archivo '+ filename + ': ')
                if '.xls' in filename:
                    csv_file=(path+"/" +filename)
                else:
                    csv_file=(path+"/" +filename+'.xls')
            else:
                break
        index_r=0
        index_c=0
        for element in User().__dict__.iteritems(): #Set headers
            sheet.write(index_r,index_c,element[0])
            index_c+=1 #move by coloumn
        index_c=0
        index_r+=1
        for json_user in input_json:
            cl_user=User()
            cl_user.load_json(json_user)
            for attr, value in cl_user.__dict__.iteritems(): #itterate over variables and their values
                sheet.write(index_r,index_c,value)
                index_c+=1
            index_c=0
            index_r+=1
#        for ele_ind in input_json:
#            element=input_json[ele_ind]
#            try:
#                for lst_element in [element["screen_name"],element["name"],element["status"]["text"],element["lang"],str(element["followers_count"]),str(element["friends_count"])]:
#                    sheet.write(index_r,index_c,lst_element)
#                    index_c+=1
#                index_c=0
#                index_r+=1
#            except KeyError as e:
#                if e.message == "status":
#                    for lst_element in [element["screen_name"],element["name"],"None",element["lang"],str(element["followers_count"]),str(element["friends_count"]),element["location"]]:
#                        sheet.write(index_r,index_c,lst_element)
#                        index_c+=1
#                index_c=0
#                index_r+=1
#            except UnicodeEncodeError as e:
#                print e
        wbk.save(csv_file)
                
    elif type=="tweet": #prepara el json de tweets para convertitlo en xls
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        filename=proyecto + '_tweet.xls'
        csv_file = path+"/" + filename
        while os.path.isfile(csv_file):
            print "ya existe "+ filename
            rewrite_menu={1:"sobre escribir",2:"cambiar nombre"}
            id=display_menu(rewrite_menu)
            if rewrite_menu[id]=="cambiar nombre":
                filename=raw_input('\nQue nombre le quieres poner al archivo '+ filename+ ': ')
                if '.xls' in filename:
                    csv_file=(path+"/" +filename)
                else:
                    csv_file=(path+"/" +filename+'.xls')
            else:
                break
        index_r=0
        index_c=0
        for element in Tweet().__dict__.iteritems(): #Set headers
            sheet.write(index_r,index_c,element[0])
            index_c+=1 #move by coloumn
        index_c=0
        index_r+=1
        output="" # needed for elements with lists-------------------------------------------------------------------------------
        for search in input_json:
            if isinstance(search,dict):
                output, index_r, index_c,sheet= csv_tweet_inner(search,output,index_r,index_c,sheet)
            else:   
                for element in search:
                    output, index_r, index_c,sheet= csv_tweet_inner(search,output,index_r,index_c,sheet)
                
        wbk.save(csv_file)             
    elif type=="freq_count": #prepara la lista de frequencias de palabras para pasar a xls
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        filename=proyecto + '_word_freq.xls'
        csv_file = path+"/" + filename
        while os.path.isfile(csv_file):
            print "ya existe "+ filename
            rewrite_menu={1:"sobre escribir",2:"cambiar nombre"}
            id=display_menu(rewrite_menu)
            if rewrite_menu[id]=="cambiar nombre":
                filename=raw_input('\nQue nombre le quieres poner al archivo '+ filename + ': ')
                if '.xls' in filename:
                    csv_file=(path+"/" +filename)
                else:
                    csv_file=(path+"/" +filename+'.xls')
            else:
                break
        index_r=1
        sheet.write(0,0,"Palabra")
        sheet.write(0,1,"Frecuencia")
        for element in input_json:
            sheet.write(index_r,0,element["palabra"])
            sheet.write(index_r,1,element["frecuencia"])
            index_r+=1
        wbk.save(csv_file)
        