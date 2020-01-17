import requests
from bs4 import BeautifulSoup
import re
import urllib


def run():
    r = requests.get("https://en.wikipedia.org/wiki/Quantum_mechanics")
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    a_tags= soup.findAll('a')
    s= []
    for tag in a_tags:
        #print(len(tag.contents))
        s.append(tag.get('href',None))

    wikis= []
    for i in range(len(s)):
     if re.search(r'^/wiki/.+', str(s[i])):
        wikis.append(s[i])

    s= "https://en.wikipedia.org"
    for counter in range(len(wikis)):
        s+=wikis[counter]
        r1= requests.get(s)
        souper(r1)
        if counter==50:
           break



def souper(r1):
    soup = BeautifulSoup(r1.text, 'html.parser')
    a_tags= soup.findAll('a')

    s= []
    for tag in a_tags:
        #print(len(tag.contents))
        s.append(tag.get('href',None))
        #goes to check if its a div class that has an image
        soup.parent


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