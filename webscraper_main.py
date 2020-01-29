import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse


def run():
    url = "https://sfbay.craigslist.org/search/sfc/apa"



    for i in range(24):
        if i == 0:
            print(souper(url))


def souper(url):
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ul_tags = soup.findAll('ul',{'class':'rows'})
    z=0
    for child in ul_tags[0].children:
        if z==0:
          print(child)
          li_tags= child.findAll('li')
          
        
           

    '''
    for index in range(len(ul_tags)): 
        for child in ul_tags[index].children:
            if z== 0:
              print(child)
            z+=1
    '''
    return 0

run()