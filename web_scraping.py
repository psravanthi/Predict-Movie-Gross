# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 14:36:48 2016

@author: sravanthi
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
temp = []

def return_artist_list(url_list):
    for i in url_list:
        response = requests.get(i)
        page = response.text
        soup = BeautifulSoup(page)
        tables=soup.find_all("table")
        rows =[row for row in tables[3].find_all('tr')]
        val = []
        for row in rows:
           val.append(row.find_all("td"))
        temp.extend([x[0].text for x in val[1:]])
    artists = pd.DataFrame(index=range(len(temp)),columns=['names','movies'])
    artists['names'] = temp
    
    artists['movies'] = artists['movies'].astype(list)
    for i in artists['names']:
        tp = []
        name = "".join(c for c in i if c not in (',','.','-',"\'"))
        response = requests.get("http://www.boxofficemojo.com/people/chart/?view=Actor&id="+name.replace(" ","").lower()+".htm")
        page = response.text
        soup = BeautifulSoup(page)
        tables=soup.find_all("table")
    
        rows =[row for row in tables[2].find_all('tr')]
    
        val = []
        for row in rows:
           val.append(row.find_all("td"))
        tp.extend([x[1].text for x in val[1:]])
        print(tp[:2])
        artists.ix[i,"movies"] = tp
        
    return artists

## Actors    
url = 'http://www.boxofficemojo.com/people/'
response = requests.get(url) 
page = response.text
soup = BeautifulSoup(page)   
tables=soup.find_all("table")
url_list = ['http://www.boxofficemojo.com/people/']
for i in tables[2].find_all('a')[:2] :
    url_list.append('http://www.boxofficemojo.com'+i['href'])
actors = return_artist_list(url_list)
#actors.to_csv("actors.csv")
''''
## Directors
url = 'http://www.boxofficemojo.com/people/?view=Director&p=.htm'
url_list = ['http://www.boxofficemojo.com/people/?view=Director&p=.htm']
response = requests.get(url) 
page = response.text
soup = BeautifulSoup(page)   
tables=soup.find_all("table")
url_list.append('http://www.boxofficemojo.com'+tables[2].find_all('a')[0]['href'])
directors = return_artist_list(url_list)
#directors.to_csv("actors.csv")

##Screenwriters
## Producers
'''