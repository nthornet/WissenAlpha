# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2012

@author: nicolas
'''
import Includes.twitter as twitter
import os,sys
import csv
import string
import json
import Includes.networkx as net
from decimal import *
from insta_wissen import insta_search
from collections import Counter
#import twitter_text
from Twitter_Interface import set_up_api, load_json, search_twitter
#import json
import datetime
import Dock
import NetX
#from OAuth                      import oauth_login
from TwitterSearch              import get_search
#from extract_tweet_entities     import get_entities
#from Geocoder                   import processTweet 
#from Geocoder                   import processTweetText
from SNA_Mod                    import create_graph
from SNA_Mod                    import save_to_gexf, save_to_graphml
from SNA_Mod                    import freq_counter, entity_count_mapper
#from SQL_Tools                  import insert_Gephi

path=os.path.join(os.path.dirname(sys.argv[0]), 'out')
gexf_path=os.path.join(os.path.dirname(sys.argv[0]), 'out/gexf')
json_path=os.path.join(os.path.dirname(sys.argv[0]), 'out/json')
csv_path=os.path.join(os.path.dirname(sys.argv[0]), 'out/csv')
TOP=10
APP_NAME = 'ThorneHarvester' 
CONSUMER_KEY = '68R3Ko3fjLyycenGbi3scQ' 
CONSUMER_SECRET = 'UlHLW4IT2ynvETI5vPy9rK8Kdu22Eyjp9Ekw5kFbZg'
ACCESS_TOKEN_KEY = '86863810-0eHImWsOim2LSAaNJMgpiSRv23Td8XmpboPcgZflA'
ACCESS_TOKEN_SECRET = '2Nqhcp2f4Ype3EfJHpD0LnPUCVvA7tblHsTjTHvExLY'

def action1():
    pass # put a function here

def action2():
    pass # blah blah

def action3():
    pass # and so on

def no_such_action():
    pass # print a message indicating there's no such action


def cargar_json(files):
    count=0
    for dirname, dirnames, filenames in os.walk(path+'/json'):
        for subdirname in dirnames:
            print os.path.join(dirname, subdirname)
            for filename in filenames:
                if filename != ".DS_Store" and "users_" not in filename:
                    count+=1
                    files[count]=os.path.join(dirname, filename)
        proyecto=raw_input("\nComo se llama tu proyecto?")
        print "escoger todos los archivos que quiera cargar separados por coma"
        user_input=Dock.display_menu(files,output=2)
        print user_input
        input_split=user_input.split(",")
        paths=[]
        for item in input_split:
            paths.append(files[int(item)])
        loaded_data=Dock.combine_json(paths)




class Timer:
    def __init__(self,searches,stop, begin):
        self.searcher=searches


class Instagram_menu:
    def main_menu(self):
        geo=None
        ids=[]
        print "-----------------Menu Instagram-------------------"
        main_menu={1:"Buscar",2:"Cargar Red Desde Json"}
        user_input=Dock.display_menu(main_menu)
        if main_menu[user_input]=="Buscar":
            insta_results,insta_friends_json,geo= self.buscar()
        elif main_menu[user_input]=="Cargar Red Desde Json":
            data,proyecto= self.load()
        if geo:
            self.process(insta_results,insta_friends_json)
        else:
            self.process(data,proyecto)
         
    def buscar(self):
        proyecto=""
        geo=None
        now = datetime.datetime.now()
        strNow=now.strftime("%Y-%m-%d %H:%M")
        query=raw_input('\nQue Busqueda te Gustaria hacer?: ')
        geo=raw_input('\nSi te gustaria agregar un codigo de geolocalizacion agreguelo aqui si no dejelo en blanco. \n'+
                      'La golocalizacion es de la siguiente manera latitude,longitude,radio en metros \n'+
                      'por ejempo para mexico df con un radio de una milla seria 19.4341667,-99.1386111,5000 : ')
        if geo is "":
            print "la Busqueda se tiene que hacer con geocodigo"
            geo=raw_input('\nSi te gustaria agregar un codigo de geolocalizacion agreguelo aqui si no dejelo en blanco. \n'+
                      'La golocalizacion es de la siguiente manera latitude,longitude,radio en metros \n'+
                      'por ejempo para mexico df con un radio de una milla seria 19.4341667,-99.1386111,5000 : ')
        proyecto=raw_input("\nComo se llama tu proyecto?")
        
        insta_results,insta_friends_json=insta_search(query,geo)
        return insta_results,insta_friends_json,geo
        
    def process(self,insta_results,insta_friends_json):
        
        Dock.csv_instagram(insta_results,input_type='like')
        Dock.csv_instagram(insta_friends_json,input_type='friends')
        
        
class Twitter_menu:
    def main_menu(self):
        geo=None
        ids=[]
        print "-----------------Menu Twitter-------------------"
        main_menu={1:"Buscar",2:"Cargar Red Desde Json"}
        user_input=Dock.display_menu(main_menu)
        if main_menu[user_input]=="Buscar":
            data,proyecto,geo= self.buscar()
        elif main_menu[user_input]=="Cargar Red Desde Json":
            data,proyecto= self.load()
        if geo:
            self.process(data,proyecto,geo)
        else:
            self.process(data,proyecto)
            
    def buscar(self):
        proyecto=""
        geo=""
        now = datetime.datetime.now()
        strNow=now.strftime("%Y-%m-%d %H:%M")
        MAX_PAGES = 15
        RESULTS_PER_PAGE = 100
        query=raw_input('\nQue Busqueda te Gustaria hacer?: ')
        geo=raw_input('\nSi te gustaria agregar un codigo de geolocalizacion agreguelo aqui si no dejelo en blanco. \n'+
                      'La golocalizacion es de la siguiente manera latitude,longitude,radio \n'+
                      'por ejempo para mexico df con un radio de una milla seria 19.4341667,-99.1386111,1mi : ') 
        proyecto=raw_input("\nComo se llama tu proyecto?")
        #geo="19.4341667,-99.1386111,1mi" #Geolocalizacion
        twitter_api = set_up_api(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)
        search_results= search_twitter(query, geo, twitter_api)
        if geo!="":
            f = open(os.path.join(os.path.dirname(sys.argv[0]), 'out/json', 'search_results_'+query+'_'+geo+'_'+strNow+'.json'), 'w')
            f.write(search_results)
            f.close()
        else:
            f = open(os.path.join(os.path.dirname(sys.argv[0]), 'out/json', 'search_results_'+query+'_'+strNow+'.json'), 'w')
            f.write(search_results)
            f.close()
        loaded_data=search_results
        return loaded_data,proyecto,geo
    
    def load(self):
        
        files={}
        id=0
        for dirname, dirnames, filenames in os.walk(path+'/json'):
            for subdirname in dirnames:
                print os.path.join(dirname, subdirname)
            for filename in filenames:
                if filename != ".DS_Store" and "users_" not in filename:
                    id+=1
                    files[id]=os.path.join(dirname, filename)
        proyecto=raw_input("\nComo se llama tu proyecto?")
        print "escoger todos los archivos que quiera cargar separados por coma"
        user_input=Dock.display_menu(files,output=2)
        print user_input
        input_split=user_input.split(",")
        paths=[]
        for input in input_split:
            paths.append(files[int(input)])
        return Dock.combine_json(paths),proyecto
    
    def process(self,loaded_data,proyecto,geo=""):
        if isinstance(loaded_data, str):
            loaded_data=json.loads(loaded_data)
            try:
                count_json,count=freq_counter([loaded_data])
            except Exception as e:
                if "expected string or buffer" in e:
                    print "Contador de frequencias recibe un string: No se guardo el csv"
        else:
            count_json,count=freq_counter(loaded_data)

        try:
        #-----------------USER PROCESSING----------------------
            lst_users=Dock.find_users(loaded_data)
            Dock.json_csv_xlwt(lst_users,"user",proyecto,csv_path)
       #user_info=[]
#        for item in loaded_data:
#            user_info.append(Dock.user_csv(item))
        except twitter.TwitterError as e:
            print "solo se puede conseguir informacion de usuarios si se carga un json"
        graph=create_graph(loaded_data) 
        Dock.json_csv_xlwt(loaded_data,"tweet",proyecto,csv_path)
        Dock.json_csv_xlwt(count_json,"freq_count",proyecto,csv_path)
        if geo != "":
            gexf_filename='search_results_'+proyecto+'_'+geo+'.gexf'
            save_to_gexf(graph,gexf_path+'/'+gexf_filename)
        else:
            gexf_filename='search_results_'+proyecto+'.gexf'
            save_to_gexf(graph,gexf_path+'/'+gexf_filename)   
         
        
        
if __name__ == '__main__':
    Dock.create_folders(os.path.dirname(sys.argv[0]))
    main_menu={1:"Twitter",2:"Instagram"}
    user_input=Dock.display_menu(main_menu)
    if main_menu[user_input] is 'Twitter':
        tweet_menu=Twitter_menu()
        tweet_menu.main_menu()
    elif main_menu[user_input] is 'Instagram':
        insta_menu=Instagram_menu()
        insta_menu.main_menu()
    
    
        
    
        

print "done"