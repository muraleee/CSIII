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
'''
for i in range(len(sqft_urls)-1):
        j=i+1
        url_string= sqft_urls[i]
        url_st= sqft_urls[j]
        #re.search('.+\/d/(.+)\/.+',url_string)
        lists= re.findall('.+\/d/(.+)\/.+',url_string)
        temp= re.findall('.+\/d/(.+)\/.+',url_st)
        if lists[0] == temp[0]:
           print("check")
           removing.append(sqft_urls[j])

for counter in range(len(removing)):
    no_repeats.remove(removing[counter])
'''
picture_urls= []
url= "https://sfbay.craigslist.org/sfc/apa/d/san-francisco-studio-for-rent-on-cuvier/7072501937.html"

r1= requests.get(url)

soup = BeautifulSoup(r1.text, 'html.parser')

div_tags= soup.findAll('div',{'id':'thumbs'})

pic_urls= []
z=0
for i in range(len(div_tags)):
      for tag in div_tags[i].find_all('a'):
       if z < 2: 
         pic_urls.append(tag.get('href',None))
       z+=1

picture_urls.append(pic_urls)
print(picture_urls[0])
'''
with open('apt_'+str(j)+'pic.jpg', 'wb') as handle:
    r = requests.get(pic_urls[j], stream=True)
    print("attempting download...")
    if not r.ok:
        print(r)

    for block in r.iter_content(1024):
        if not block:
            break

        handle.write(block)
'''




