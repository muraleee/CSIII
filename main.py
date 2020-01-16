import requests
from bs4 import BeautifulSoup
import re
import urllib



r = requests.get("https://en.wikipedia.org/wiki/Quantum_mechanics")
r.raise_for_status()
soup = BeautifulSoup(r.text, 'html.parser')

a_tags= soup.findAll('a')

for tag in a_tags:
    print(tag.get('href',None))
#print(soup)
'''
for tag in tags:
    print(tag.get_text())

resource = urllib.request.urlopen("http://www.digimouth.com/news/media/2011/09/google-logo.jpg")
output = open("file01.jpg","wb")
output.write(resource.read())
'''