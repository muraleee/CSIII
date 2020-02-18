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

urls= ["https://sfbay.craigslist.org/sfc/apa/d/pleasanton-fabulous-3-bed2bath/7073151657.html", "https://sfbay.craigslist.org/sfc/vac/d/oakland-rare-find-lodge-in-the-oakland/7071103395.html"]


#this method should give 2 pic_urls to later be downloaded
def pic_return(urls):
      
    pic_pairs= []  
    pic_urls=[]

    for i in range(len(urls)):
          r= requests.get(urls[i])
          #is the literal picture urls, supposed to have 2 of them 
          soup = BeautifulSoup(r.text, 'html.parser')
          div_tags= soup.findAll('div',{'id':'thumbs'})
          s=0
          for i in range(len(div_tags)):
           for tag in div_tags[i].find_all('a'):
               if s < 2:
                pic_urls.append(tag.get('href',None))
                s+=1
                
          pic_pairs.append([pic_urls[len(pic_urls)-2],pic_urls[len(pic_urls)-1]])     

           

    print(pic_pairs)
    return pic_pairs

pic_pairs= pic_return(urls)

def dwnloaded_pics(pic_pairs):
  

 for i in range(len(pic_pairs)):
  for j in range(len(pic_pairs[i])):
     with open('apt'+ str(i+1)+'-'+str(j+1) +'.jpg', 'wb') as handle:
      r = requests.get(pic_pairs[i][j], stream=True)
      print("attempting download...")
      if not r.ok:
          print(r)

      for block in r.iter_content(1024):
          if not block:
               break

          handle.write(block)
     print(handle)
 return 0

dwnloaded_pics(pic_pairs)