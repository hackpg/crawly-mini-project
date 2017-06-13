import requests
from bs4 import BeautifulSoup
import domain
from newspaper import Article

url = "http://timesofindia.indiatimes.com/entertainment"
r = requests.get(url)

soup = BeautifulSoup(r.content , 'html.parser')

links = soup.find_all("a")

#print(links)

our = set()

count = 0

for link in links:
    comp = str(link.get("href"))
    if count <= 2 and comp.find('timesofindia')!=-1 and comp.find('cms') == -1:
        #print(link)
        our.add(comp)
        count = count + 1

print(our)

for item in our:
    art = Article(item)
    art.download()
    art.parse()
    print(art.top_image)
