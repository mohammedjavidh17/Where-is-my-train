from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

root = requests.get('http://www.chennailocaltrain.com/beach-to-chengalpattu-train-timings-1.html').text
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
data = soup.find_all('table')
Datadf = pd.DataFrame([])
for i,d in enumerate(data):
    dataLst = []
    val = str(d.text)
    val = val.replace(' ', '')
    val = val.split()
    if len(val) > 238:
        buf = []
        buf.append(val[-224:])
        val = buf[0]
        for x in range(0, len(val), 8):
            
            dataLst.append(val[x:8+x])
        df = pd.DataFrame(dataLst).iloc[:, 1:-1]
        df = df.replace('--', np.nan)
        print(df)
        Datadf = pd.concat([Datadf, df], axis=1)

        
