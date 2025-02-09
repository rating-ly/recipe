from bs4 import BeautifulSoup
>>> from urllib.request import Request, urlopen
>>> import re
>>> req = Request('https://addapinch.com/the-best-chocolate-cake-recipe-ever/', headers={'User-Agent': 'Mozilla/5.0'})
>>> html_page = urlopen(req).read()
>>> print(html_page)

py -m pip install beautifulsoup4