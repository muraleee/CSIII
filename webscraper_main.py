import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse


def run():
    url = "https://sfbay.craigslist.org/search/sfc/apa"

    housing_urls= []
    sqft_urls= [] 
    section_ranked=[]
    ranked = []
    #goes through 24 pages of craigslist  
    for i in range(24):
        if i == 0:
            housing_urls=souper(url)
            sqft_urls=sqft_search(housing_urls)
            section_ranked= rank_sqft(sqft_urls)
            for j in range(len(section_ranked)) :
                ranked.append(section_ranked[j])

            

#supposed to get all of the links from each page
def souper(url):
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ul_tags = soup.findAll('ul',{'class':'rows'})
    s=0

    #supposed to have the urls for the 1 page
    housing_urls= []
    li_tags= soup.findAll('li',{'class':'result-row'})
    for i in range(len(li_tags)):
      for tag in li_tags[i].find_all('a'):
           if s%3==0:
             housing_urls.append(tag.get('href',None))
           s+=1       
    
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

#supposed to find the features of the page of apartments and return a ranking, takes a while for it run
def sqft_search(housing_urls):
    housing_urls = housing_urls
   #list of sqft and corresponding urls
    sqft_urls =[]
    for i in range(len(housing_urls)): 
          r= requests.get(housing_urls[i]) 
          soup= BeautifulSoup(r.text, 'html.parser')

          spans= soup.findAll('span',{'class':'housing'})
          if len(spans) != 0:
            if re.search('.+\-(.+)ft.+',spans[0].text):
              sqfts= re.findall('.+\- (.+)ft.+',spans[0].text)
              sqft_urls.append([int(sqfts[0]), housing_urls[i]])
              print("done")
            else:
               housing_urls[i]= "error"
            spans.clear() 

                     
    return sqft_urls

def rank_sqft(sqft_urls):
 
  sqft_urls.sort() 
  sqft_urls.reverse()      
  print(sqft_urls[0][0])
  return 0
run()

