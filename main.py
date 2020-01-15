import requests
from bs4 import BeautifulSoup
import re


r = requests.get("https://en.wikipedia.org/wiki/Quantum_mechanics")
r.raise_for_status()
soup = BeautifulSoup(r.text, 'html.parser')


tags = soup.findAll('a')