import json
import requests
from bs4 import BeautifulSoup


links = []
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
url = "https://delta.ir/sitemap/mainCitySeachSiteMap.xml"

r = requests.get(url, headers=headers)

xml_text = r.text

soup = BeautifulSoup(xml_text)
sitemapTags = soup.find_all("url")

for sitemap in sitemapTags:
    links.append(sitemap.findNext("loc").text)


for link in links:
    print(link)

# with open('links.json','r') as json_file:
#     links = json.loads(json_file.read())
#     new_link = links[0]['res']
    

    