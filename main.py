from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

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
data = soup.find_all('table', height=["822", "862", '842'])

for i,d in enumerate(data):
    dataLst = []
    val = str(d.text)
    val = val.replace(' ', '')
    val = val.split()
    for x in range(0, len(val), 8):
        if i>1:
            x = x+1
        dataLst.append(val[15+x:15+8+x])
    df = pd.DataFrame(dataLst).iloc[:-2, :]
    df = df.replace('--', np.nan)
    print(df)
