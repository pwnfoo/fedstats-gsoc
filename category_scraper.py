from bs4 import BeautifulSoup
from urllib import urlopen

page = urlopen ('https://fedora-fedmsg.readthedocs.io/en/latest/topics.html')
soup = BeautifulSoup (page.read().decode('ascii', 'ignore'), 'html.parser')
categorylist = list()
for h3 in soup.findAll('h3'):
    if len(h3.text.split('.')) > 2 and h3.text.split('.') not in categorylist :
        categorylist.append(h3.text.split('.'))

print categorylist
