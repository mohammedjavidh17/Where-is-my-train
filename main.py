from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

testLink = [224,238,'http://www.chennailocaltrain.com/beach-to-chengalpattu-train-timings-1.html']
testLink1 = [224,238,'http://www.chennailocaltrain.com/beach-to-chengalpattu-train-timings-1.html']
testLink2 = [144,157,'http://www.chennailocaltrain.com/tambaram-to-beach-train-timings-1.html']
def get(siz):
    root = requests.get(siz[2]).text
    soup = BeautifulSoup(root, 'lxml')
    data = soup.find_all('table')
    Datadf = pd.DataFrame([])
    for i,d in enumerate(data):
        dataLst = []
        val = str(d.text)
        val = val.replace(' ', '')
        val = val.split()
        print(len(val))
        if len(val) > siz[1]:
            buf = []
            run = []
            
            if True:
                run.append(val[-siz[0]-6:-siz[0]])
                buf.append(val[-siz[0]:])
                val = buf[0]
                for x in range(0, len(val), 8):
                    
                    dataLst.append(val[x:8+x])
                df = pd.DataFrame(dataLst).iloc[:, 1:-1]
                df = df.replace('--', np.nan)
                df = pd.concat([pd.DataFrame(run, columns=list(range(1,7))), df])
                #print(df)
                Datadf = pd.concat([Datadf, df], axis=1)
    return Datadf
get(testLink2).to_csv('assets\\test.csv')

        
