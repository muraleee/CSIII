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

def next_page(url):
    r= requests.get(url)
    new_url= ""
    soup = BeautifulSoup(r.text, 'html.parser')
    a_tags= soup.findAll('a',{'class':'button next'})
    for tag in a_tags:
        new_url = tag.get('href', None)
    
    
    return "https://sfbay.craigslist.org"+ new_url



url=  next_page(url)
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
  #print(sqft_urls[0][0])
  sqft_urls = repeat_check(sqft_urls)

  ranks= sqft_urls
  
  return ranks

def repeat_check(sqft_urls):
     no_repeats = sqft_urls
     url_string= ""
     removing= []
     for i in range(len(sqft_urls)-1):
        j=i+1
        url_string= sqft_urls[i][1]
        url_st= sqft_urls[j][1]
        #re.search('.+\/d/(.+)\/.+',url_string)
        lists= re.findall('.+\/d/(.+)\/.+',url_string)
        temp= re.findall('.+\/d/(.+)\/.+',url_st)
        if lists[0] == temp[0]:
           #print("check")
           removing.append([sqft_urls[j][0],sqft_urls[j][1]])

     for counter in range(len(removing)):
        no_repeats.remove(removing[counter])


     
     return no_repeats

section_ranked = rank_sqft(sqft_search(souper(url)))
ranked =[]
for j in range(len(section_ranked)):
             ranked.append(section_ranked[j])

print(ranked)

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