# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 21:55:01 2016

@author: sravanthi
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import os
import pandas as pd
chromedriver = "/Users/Manoj/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


def get_movie_list(url):
    url_list = []
    
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    link = driver.find_element_by_xpath('//*[@id="body"]/table[3]/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody')
    tr = link.find_elements_by_css_selector('tr')
#print(tr[2].find_elements_by_css_selector('a'))


    for i in tr[2:len(tr)-4]:
       item =i.find_elements_by_css_selector('a')
       url_list.append(item[0].get_attribute('href'))
    movies_data = pd.DataFrame(columns=["Release Date","Name","Domestic Gross","genre","Run Time",
    "Rating","Budget","No_theatres","Actors","Producer","Writer","Director"],index=range(len(url_list)))
    movies_data['Actors'] = movies_data['Actors'].astype(list)
    #url_list = ["http://www.boxofficemojo.com/movies/?id=pixar2015.htm"]
    for j in range(len(url_list)):
        
        
        try:
            driver = webdriver.Chrome(chromedriver)
            driver.get(url_list[j])
            movies_data.ix[j,"Name"] = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/font/b').text
            movies_data.ix[j,"Domestic Gross"] = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[1]/td/font/b').text
            movies_data.ix[j,"Release Date"] = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[2]/td[2]/b/nobr/a').text
            movies_data.ix[j,"genre"] = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[3]/td[1]/b').text
            movies_data.ix[j,"Run Time"]  = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[3]/td[2]/b').text
            movies_data.ix[j,"Rating"] = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[4]/td[1]/b').text

            movies_data.ix[j,"Budget"] = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[4]/td[2]/b').text

            div = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[1]/div[2]/div[2]')
            tables = div.find_elements_by_css_selector('tr')

            for tab in tables:
               if "Widest Release" in tab.text:
                  td = tab.find_elements_by_css_selector('td')
                  movies_data.ix[j,"No_theatres"] = td[1].text
            try:
               body = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/div/div[2]/table/tbody')
               tr = body.find_elements_by_css_selector('tr')
        
               for row in tr:
                  td = row.find_elements_by_css_selector('td')
                  if 'Director' in td[0].text:
                     movies_data.ix[j,"Director"]= ((td[1].text).split("\n"))[0]
                  elif 'Writer' in td[0].text:
                     movies_data.ix[j,"Writer"]= ((td[1].text).split("\n"))[0]
                  elif 'Producer' in td[0].text:
                     movies_data.ix[j,"Producer"]=((td[1].text).split("\n"))[0]
                  elif 'Actor' in td[0].text:
                     item = (td[1].text).split("\n")
                     movies_data.ix[j,"Actors"] = [i for i in item[:min(3,len(item))]]
            except:
               movies_data.ix[j,"Director"]= "nan" 
               movies_data.ix[j,"Writer"]= "nan" 
               movies_data.ix[j,"Producer"]= "nan" 
               movies_data.ix[j,"Actors"]= []
 

        
        
            driver.close()
        except:
            driver.close()
            print("unable to load",url_list[j])

    return movies_data
        
url = 'http://www.boxofficemojo.com/yearly/chart/?yr=2004&p=.htm'
driver = webdriver.Chrome(chromedriver)
driver.get(url)
data_2004 = get_movie_list(url)
data_2004.to_csv("2004_op.csv")
body = driver.find_element_by_xpath('//*[@id="body"]/table[3]/tbody/tr/td[1]/center[1]')
a = body.find_elements_by_css_selector('a')
links = [i.get_attribute('href') for i in a]
for i in range(len(links)):
  data_2004 = get_movie_list(links[i])
  data_2004.to_csv("2004_"+str(i)+".csv")