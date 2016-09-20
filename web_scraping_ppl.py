# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 14:36:48 2016

@author: sravanthi
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
temp = []
temp_url_list = []
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
        temp_url_list.extend(["http://www.boxofficemojo.com/people"+((x[0].find('a'))['href'])[1:] for x in val[1:]])
    artists = pd.DataFrame(index=range(len(temp)),columns=['names','movies'])
    artists['names'] = temp
    
    artists['movies'] = artists['movies'].astype(list)
    for i in range(len(temp_url_list)):
        movie_list = []
        response = requests.get(temp_url_list[i])
        page = response.text
        soup = BeautifulSoup(page)
        tables=soup.find_all("table")
        

        rows =[row for row in tables[2].find_all('tr')]
    
    #print(rows[1])
        val = []
        for row in rows[1:]:
           val.append(row.find_all("td"))
        movie_list.extend([x[1].text for x in val])
    
        artists.ix[i,"movies"] = movie_list
        
    return artists
'''
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
'''

##Screenwriters
screenwriter = return_artist_list(["http://www.boxofficemojo.com/people/?view=Writer&p=.htm"])
#directors.to_csv("actors.csv")
## Producers
#producer = return_artist_list(["http://www.boxofficemojo.com/people/?view=Producer&p=.htm"])
#producer.to_csv("actors.csv")
