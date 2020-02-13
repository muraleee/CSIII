import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse

url_string = "https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370575.html"
url_st= "https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370471.html"
sqft_urls= ["https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370575.html","https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370471.html"]
sqft_urls.append("https://sfbay.craigslist.org/sfc/apa/d/oakland-house-for-rent/7069370274.html")
no_repeats = sqft_urls
url_string= ""
removing= []
url= "https://sfbay.craigslist.org/search/sfc/apa"


#for getting pictures
'''
urls= ["https://sfbay.craigslist.org/sfc/apa/d/pleasanton-fabulous-3-bed2bath/7073151657.html", "https://sfbay.craigslist.org/sfc/apa/d/san-francisco-beautiful-new-remodeling/7073146920.html"]


#this method should give 2 pic_urls to later be downloaded
def pic_return(urls):
      
    
     r= requests.get(urls[0])
     #is the literal picture urls, supposed to have 2 of them 
     pic_urls=[]
     soup = BeautifulSoup(r.text, 'html.parser')
     div_tags= soup.findAll('div',{'id':'thumbs'})
     s=0
     for i in range(len(div_tags)):
       for tag in div_tags[i].find_all('a'):
            if s < 2:
             pic_urls.append(tag.get('href',None))
            s+=1
            
     print(pic_urls)
     return 0

pic_return(urls)
'''