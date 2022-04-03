import requests
from bs4 import BeautifulSoup
import json
import re
from googlesearch import search



for j in search("In what country can you visit Machu Picchu?", tld="com", num=1, stop=1, pause=2):
    url = j

body = requests.get(url)

body_text = body.content  # or body.text

print(body.content) 