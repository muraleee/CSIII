import requests
from bs4 import BeautifulSoup
import re
import urllib
from scrapy.http import TextResponse


def run():
    response = requests.get("https://en.wikipedia.org/wiki/Quantum_mechanics")
    response.raise_for_status()
    response = TextResponse(body=response.content, url="https://en.wikipedia.org/wiki/Quantum_mechanics")

    response.css('div.printfooter > a::text').extract_first()
    soup = BeautifulSoup(response.text, 'html.parser')

    a_tags= soup.findAll('a')
    s= []
    for tag in a_tags:
        #print(len(tag.contents))
        s.append(tag.get('href',None))

    wikis= []
    for i in range(len(s)):
     if re.search(r'^/wiki/.+', str(s[i])) or re.search(r'^https://en.wikipedia.org.+',str(s[i])):
        continue
     else:
        if re.search(r'^https://.+',str(s[i])):
         wikis.append(s[i])
    
    del wikis[2]
    
    print(wikis)

    '''
   
    s= "https://en.wikipedia.org"
    for counter in range(len(wikis)):
        s+=wikis[counter]
        print(s)
        r1= requests.get(s)
        #print(souper(r1))
        if counter==16:
           break
    '''


def souper(r1):
    soup = BeautifulSoup(r1.text, 'html.parser')
    print(r1.text)
    a_tags= soup.findAll('div',{'class':'thumbcaption'})
    
    print(len(a_tags))
    s= []
    for tag in a_tags:
        #print(len(tag.contents))
        #s.append(tag.get('href',None))
        #goes to check if its a div class that has an image
        if tag.parent== 'thumbinner':
           print("s")
        print(tag.child.text)
       # strs= re.findall('^<a href=.*', tag.parent)
       # print(len(strs))

    return 0


#print(soup)
'''
for tag in tags:
    print(tag.get_text())

resource = urllib.request.urlopen("http://www.digimouth.com/news/media/2011/09/google-logo.jpg")
output = open("file01.jpg","wb")
output.write(resource.read())
'''
run()