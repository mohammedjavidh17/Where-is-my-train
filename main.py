from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

assets = ['assets\\ajj-mas.csv', 'assets\cgl-msb.csv', 'assets\mas-tpty.csv', 'assets\msb-trt.csv','assets\\tmb-msb.csv', 
'assets\\tmpl-msb.csv', 'assets\\trt-msb.csv', 'assets\\vlcy-ms.csv'
]
testLink = [224,238,'http://www.chennailocaltrain.com/beach-to-chengalpattu-train-timings-1.html']
testLink1 = [224,238,'http://www.chennailocaltrain.com/beach-to-chengalpattu-train-timings-1.html']
testLink2 = [144,157,'http://www.chennailocaltrain.com/tambaram-to-beach-train-timings-1.html']
def getData(siz:list):
    j = 1
    Datadf = pd.DataFrame([])
    while True:
        flag = [False]
        try:
            link = siz[2][:-6]+str(j)+siz[2][-5:]
            print(link)
            root = requests.get(link).text
        except:
            break
        soup = BeautifulSoup(root, 'lxml')
        data = soup.find_all('table')
        for i,d in enumerate(data):
            dataLst = []
            val = str(d.text)
            val = val.replace(' ', '')
            val = val.split()
            #print(len(val))
            if len(val) > siz[1]:
                flag.clear()
                flag.append(True)
                buf = []
                run = []
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
        if not flag[0]:
            break
        j+=1
    return Datadf

def getAsset(Dta:list):
    toRet = []
    for i,loc in enumerate(assets):
        df = pd.read_csv(loc)
        dta = list(df.iloc[:, 0])
        if Dta[0] in dta and Dta[1] in dta:
            buf = []
            buf.append(loc)
            a = dta.index(Dta[1])-dta.index(Dta[0])
            buf.append(a)
            toRet.append(buf)
    return toRet
print(getAsset(['VELACHERY', 'LIGHT HOUSE']))
