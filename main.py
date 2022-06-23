from bs4 import BeautifulSoup
import requests

root = requests.get('http://www.chennailocaltrain.com/chengalpattu-to-beach-train-timings-1.html').text
soup = BeautifulSoup(root, 'lxml')
dayS = soup.find_all('tr', bgcolor="#804000")
day = []
for x in dayS:
    a = x.text
    b = list(a.split())
    b.remove("RUNNING")
    b.remove("DAYS")
    for y in b:
        day.append(y)
