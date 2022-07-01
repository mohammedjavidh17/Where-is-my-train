from bs4 import BeautifulSoup
import requests
import numpy as np
from tkinter import *
from ttkwidgets.autocomplete import *
import pyautogui as pyg
import pandas as pd
import time
pyg

cf = pd.read_json('assets\\config.json').iloc[0,0]
stations = []
assets = [ 'assets\cgl-msb.csv', 'assets\\tmb-msb.csv', 'assets\\ajj-mas.csv', 'assets\mas-tpty.csv', 'assets\msb-trt.csv', 
'assets\\tmpl-msb.csv', 'assets\\vlcy-ms.csv'
]
for sta in assets:
    df = pd.read_csv(sta)
    buf = list(df.iloc[:, 0])
    for x in buf:
        stations.append(x)

testLink1 = [224,238,'http://www.chennailocaltrain.com/chengalpattu-to-beach-train-timings-1.html', 'assets\cgl-msb']
testLink2 = [144,157,'http://www.chennailocaltrain.com/tambaram-to-beach-train-timings-1.html', 'assets\\tmb-msb']
testLink3 = [232,245,'http://www.chennailocaltrain.com/arakkonam-to-Chennai-central-train-timings-1.html', 'assets\\ajj-mas.csv']
testLink4 = [320, 333, 'http://www.chennailocaltrain.com/chennai-to-tirupati-train-timings.html', 'assets\mas-tpty.csv']
testLink5 = [248, 260, 'http://www.chennailocaltrain.com/beach-to-tiruttani-train-timings.html', 'assets\msb-trt.csv']
testLink6 = [296, 300,'http://www.chennailocaltrain.com/tirumalpur-to-beach-train-timings.html' ,'assets\\tmpl-msb.csv']
testLink7 = [144, 150, 'http://www.chennailocaltrain.com/velachery-to-beach-train-timings-1.html', 'assets\\vlcy-ms.csv']

linkData = pd.read_csv('assets\linkData.csv')

def getData(siz:list, grp = 8):
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
        if siz[2][-6] != '1':
            link = siz[2]
            root = requests.get(link).text
        soup = BeautifulSoup(root, 'lxml')
        data = soup.find_all('table')

        for i,d in enumerate(data):
            dataLst = []
            val = str(d.text)
            val = val.replace(' ', '')
            val = val.split()
            

            if len(val) > siz[1]:
                if siz[-1] == 'assets\\tmpl-msb.csv':
                    if len(val) == 307:
                        for k in range(4):
                            val.insert(11, '--')
                flag.clear()
                
                flag.append(True)
                buf = []
                run = []
                run.append(val[-siz[0]-6:-siz[0]])
                buf.append(val[-siz[0]:])
                val = buf[0]
                for x in range(0, len(val), grp):
                    
                    dataLst.append(val[x:grp+x])
                df = pd.DataFrame(dataLst).iloc[:, 1:-1]
                df = df.replace('--', np.nan) #---
                df = df.replace('---', np.nan)
                df = pd.concat([pd.DataFrame(run, columns=list(range(1,7))).replace('--', np.nan), df])
                
                Datadf = pd.concat([Datadf, df], axis=1)
        if siz[2][-6] != '1':
            break
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
            buf.append(i)
            toRet.append(buf)
    return toRet

root = Tk()
width = root.winfo_screenwidth() - 50
height = root.winfo_screenheight() - 50
root.geometry('%dx%d'%(width, height))

def clrAll():
    try:
        for x in root.winfo_children:
            x.destroy()
    except:
        pass

def mainWindow():
    clrAll()

    def AutoFocus():
        if str(root.focus_get())[13:] == '!autocompletecombobox':
            To.focus_set()
    frm = LabelFrame(root)
    frm.place(relx=0.5, rely=0.01, anchor=N, relheight=0.98, relwidth=0.35)
    Label(frm, text="From : ", font=(cf['font'], cf['S2'])).grid(column=0, row=0, padx=20, pady=40)
    Label(frm, text="To : ", font=(cf['font'], cf['S2'])).grid(column=0, row=1, padx=20, pady=40)
    From = AutocompleteCombobox(frm, completevalues=stations, width= 30, font=(cf['font'], cf['S2']))
    From.grid(column=1, row=0, padx=20, pady=40)
    To = AutocompleteCombobox(frm, completevalues=stations, width= 30,font=(cf['font'], cf['S2']))
    To.grid(column=1, row=1, padx=20, pady=40)
    From.focus_set()
    Button(frm, text='Find Trains', font=(cf['font'], 19), bg='#92d437', command=lambda:reponseWindow([str(From.get()), str(To.get())])).grid(column=0, row=2, columnspan=2, padx=10, pady=60)
    root.bind('<Return>', lambda e: AutoFocus())

def reponseWindow(dta:list):
    print(dta)
    linkD1 = getAsset(dta)
    print(linkD1)

dg = pd.read_csv('assets\\linkData.csv')

for test in range(4,7):
    lst = list(dg.iloc[test, :])
    print(lst)
    getData(lst).to_csv('assets\\test.csv')

