import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse


def run():
    url = "https://sfbay.craigslist.org/search/sfc/apa"

    housing_urls= []
     
    #goes through 24 pages of craigslist  
    for i in range(24):
        if i == 0:
            print(souper(url))


def souper(url):
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ul_tags = soup.findAll('ul',{'class':'rows'})
    z=0

    #supposed to have the urls for the 1 page
    housing_urls= []
    li_tags= soup.findAll('li',{'class':'result-row'})
    for i in range(len(li_tags)):
      for tag in li_tags[i].find_all('a'):
        if i==0:
           print(tag.get('href',None))
    #need to find a way to isolate the link

    #print(li_tags[0])
    '''
    for child in ul_tags[0].children:
        if z==0:
          print(child)
          #s=re.findall('<a.+', child)
    '''    
        
           

    '''
    for index in range(len(ul_tags)): 
        for child in ul_tags[index].children:
            if z== 0:
              print(child)
            z+=1
    '''
    return housing_urls

run()