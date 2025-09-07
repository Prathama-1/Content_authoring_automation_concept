#search the page inside of AEM
#get the metadata of the page
#compare the metadata of the page with the metadata of the live page(view page source)

#I wil need access to aem hosted page.
#it is there in sites.html/content/ups-pt/us/en....
#connection to aem repository

import requests
from bs4 import BeautifulSoup

url = ""
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

title = soup.find("meta", attrs={"property": "og:title"})["content"]
description = soup.find("meta", attrs={"name": "description"})["content"]

print(f"Title: {title}")
print(f"Description: {description}")

