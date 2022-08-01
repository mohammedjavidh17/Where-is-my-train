from tkinter import messagebox
from tkinter.ttk import Progressbar
from bs4 import BeautifulSoup
import requests
import numpy as np
from tkinter import *
from ttkwidgets import *
from datetime import datetime as dt
from ttkwidgets.autocomplete import *
import pyautogui as pyg
import urllib.request
import pandas as pd
pyg

Root = Tk()
width = Root.winfo_screenwidth() - 1000
height = Root.winfo_screenheight() - 50
Root.geometry('%dx%d'%(width, height))
cf = pd.read_json('assets\\config.json').iloc[0,0]
stations = []
assets = [ 'assets\\cgl-msb.csv', 'assets\\tmb-msb.csv', 'assets\\ajj-mas.csv', 'assets\\mas-tpty.csv', 'assets\\msb-trt.csv', 
'assets\\tmpl-msb.csv', 'assets\\vlcy-ms.csv'
]
for sta in assets:
    df = pd.read_csv(sta)
    buf = list(df.iloc[:, 0])
    for x in buf:
        stations.append(x)
revLink = {
    'http://www.chennailocaltrain.com/chengalpattu-to-beach-train-timings-1.html' : 'http://www.chennailocaltrain.com/beach-to-chengalpattu-train-timings-1.html',
    'http://www.chennailocaltrain.com/tambaram-to-beach-train-timings-1.html' : 'http://www.chennailocaltrain.com/beach-to-tambaram-train-timings-1.html',
    'http://www.chennailocaltrain.com/arakkonam-to-Chennai-central-train-timings-1.html' : 'http://www.chennailocaltrain.com/chennai-central-to-arakkonam-train-timings-1.html',
    'http://www.chennailocaltrain.com/chennai-to-tirupati-train-timings.html' : 'http://www.chennailocaltrain.com/tirupati-to-chennai-train-timings.html',
    'http://www.chennailocaltrain.com/beach-to-tiruttani-train-timings.html' : 'http://www.chennailocaltrain.com/tiruttani-to-chennai-beach-train-timings.html',
    'http://www.chennailocaltrain.com/tirumalpur-to-beach-train-timings.html' : 'http://www.chennailocaltrain.com/beach-to-tirumalpur-train-timings.html',
    'http://www.chennailocaltrain.com/velachery-to-beach-train-timings-1.html' : 'http://www.chennailocaltrain.com/beach-to-velachery-train-timings-1.html'
}

#TestSets
testLink1 = [224,238,'http://www.chennailocaltrain.com/chengalpattu-to-beach-train-timings-1.html', 'assets\cgl-msb']
testLink2 = [144,157,'http://www.chennailocaltrain.com/tambaram-to-beach-train-timings-1.html', 'assets\\tmb-msb']
testLink3 = [232,245,'http://www.chennailocaltrain.com/arakkonam-to-Chennai-central-train-timings-1.html', 'assets\\ajj-mas.csv']
testLink4 = [320, 333, 'http://www.chennailocaltrain.com/chennai-to-tirupati-train-timings.html', 'assets\mas-tpty.csv']
testLink5 = [248, 260, 'http://www.chennailocaltrain.com/beach-to-tiruttani-train-timings.html', 'assets\msb-trt.csv']
testLink6 = [296, 300,'http://www.chennailocaltrain.com/tirumalpur-to-beach-train-timings.html' ,'assets\\tmpl-msb.csv']
testLink7 = [144, 150, 'http://www.chennailocaltrain.com/velachery-to-beach-train-timings-1.html', 'assets\\vlcy-ms.csv']

linkData = pd.read_csv('assets\linkData.csv')

def getData(siz:list, lod, grp = 8):
    j = 1
    lodVal = 0
    Datadf = pd.DataFrame([])
    while True:
        if lodVal >= 100:
            lodVal = 0
        flag = [False]
        try:
            link = siz[2][:-6]+str(j)+siz[2][-5:]
            lod['value'] = lodVal
            lodVal = lodVal+20
            Root.update()
            root = requests.get(link).text
            print(link, lodVal)
            Root.update()
        except:
            break
        if siz[2][-6] != '1':
            link = siz[2]
            lod['value'] = lodVal
            lodVal = lodVal+20
            Root.update()
            root = requests.get(link).text
            print(link, lodVal)
            Root.update()
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
                if siz[-2] == 'http://www.chennailocaltrain.com/beach-to-tirumalpur-train-timings.html':
                    if len(val) == 310:
                        val.insert(-27, '--')        
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
def getAsset(Dta:list):    #[from, to]
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

def clrAll():
    for x in Root.winfo_children():
        x.destroy()
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
def back():
    clrAll()
    mainWindow()
def BackButton(fr):
    return Button(fr, text="\u274C", font=(cf['font'], 10),bg='#d62929', command=back).place(relx=0.98, rely=0.02, anchor=NE) 
def mainWindow():
    clrAll()
    def AutoFocus():
        if str(Root.focus_get())[13:] == '!autocompletecombobox':
            To.focus_set()
    Lbl = Label(Root, text="Checking Connections.. " , font=(cf['font'], 12))
    Lbl.pack(anchor=CENTER)
    Root.update()
    if not connect():
        messagebox.showerror("Internet not connected", "Check your Internet Connection")
        Root.destroy()
    Lbl.destroy()
    global frm
    global trFrm 
    frm = LabelFrame(Root)
    frm.place(relx=0.5, rely=0.01, anchor=N, relheight=0.98, relwidth=0.75)
    Label(frm, text='Devoloped by Javidh (2022)', font=('Consolas', 12)).place(relx=0.98, rely=0.98, anchor=SE)
    trFrm = Frame(frm)
    trFrm.place(relx=0.5, rely=0.45, anchor=N)
    Label(frm, text="From : ", font=(cf['font'], cf['S2'])).grid(column=0, row=0, padx=20, pady=40)
    Label(frm, text="To : ", font=(cf['font'], cf['S2'])).grid(column=0, row=1, padx=20, pady=40)
    From = AutocompleteCombobox(frm, completevalues=stations, width= 30, font=(cf['font'], cf['S2']))
    From.grid(column=1, row=0, padx=20, pady=40)
    To = AutocompleteCombobox(frm, completevalues=stations, width= 30,font=(cf['font'], cf['S2']))
    To.grid(column=1, row=1, padx=20, pady=40)
    From.focus_set()
    global find
    find = Button(frm, text='Find Trains', font=(cf['font'], 19), bg='#92d437', command=lambda:reponseWindow([str(From.get()), str(To.get())]))
    find.grid(column=0, row=2, columnspan=2, padx=10, pady=60)
    Root.bind('<Return>', lambda e: AutoFocus())
def reponseWindow(dta:list):
    find['state'] = DISABLED
    usedBuf = 1
    DisDta = []
    LnkDta = []
    def Disp(Data):
        Frms = []
        pg = [0]
        def inc(e=None):
            a = pg[0]+1
            pg.clear()
            pg.append(a)
            try:
                Frms[a].tkraise()
            except:
                Frms[0].tkraise()
                pg.clear()
                pg.append(0)
        def dec(e=None):
            a = pg[0]-1
            pg.clear()
            pg.append(a)
            try:
                Frms[a].tkraise()
            except:
                Frms[-1].tkraise()
                pg.clear()
                pg.append(len(Frms)-1)
        sel = IntVar()
        sel.set(-1)
        def routDis(dta:list): #[buf, ind]
            Frms1 = []
            Apg = [0]
            tk = Tk()
            width = Root.winfo_screenwidth() - 1200
            height = Root.winfo_screenheight() - 200
            tk.geometry('%dx%d'%(width, height))
            tk.title(DisDta[dta[0]-1])
            Label(tk, text='Devoloped by Javidh (2022)', font=('Consolas', 12)).place(relx=0.98, rely=0.98, anchor=SE)
            df = pd.read_csv('buff\\'+str(dta[0])+'.csv').iloc[:, dta[1]+1]
            df1 = pd.read_csv(LnkDta[0][dta[0]-1][0])
            if LnkDta[0][dta[0]-1][-2] < 0:
                df1 = df1.iloc[::-1]
            def inc0(e=None):
                a = Apg[0]+1
                Apg.clear()
                Apg.append(a)
                try:
                    Frms1[a].tkraise()
                except:
                    Apg.clear()
                    a = len(Frms1)-1
                    Apg.append(a)
            def dec0(e=None):
                a = Apg[0]-1
                Apg.clear()
                Apg.append(a)
                if a >= 0:
                    Frms1[a].tkraise()
                else:
                    Apg.clear()
                    Apg.append(0)
            indx =0
            toR = 0
            flg = False
            for i in range(0, df.shape[0]-8+1):
                if flg:
                    break
                AFrm = Frame(tk)
                AFrm.place(relx=0.5, rely=0.5, anchor=CENTER, relheight=0.99, relwidth=0.99)
                Label(AFrm, text='Pg - '+str(i+1), font=(cf['font'], 12)).pack(pady=10)
                Button(AFrm, text='UP', font=(cf['font'], 12),padx=5, pady=5, command=dec0).pack(pady=10)
                for j in range(8):
                    tk.update()
                    try:
                        BFrm = Frame(AFrm, width=500, height=50)
                        BFrm.pack(pady=10)
                        lb = Label(BFrm, text=df1.iloc[indx,0]+' --> '+df.iloc[indx+1], font=(cf['font'], 15))
                        #	u"\U0001F686"
                        if True:
                            tim0 = list(map(int, df.iloc[indx+1].split(':')))
                            now = dt.now()
                            try:
                                tim1 = list(map(int, df.iloc[indx+2].split(':')))
                            except:
                                lb['text'] = lb['text'] +' '+ u"\U0001F686"
                                break
                            Tim0 = now.replace(hour=tim0[0], minute=tim0[1])
                            Tim1 = now.replace(hour=tim1[0], minute=tim1[1])
                            if Tim1 >= now and Tim0 <= now:
                                lb['text'] = lb['text'] +' '+ u"\U0001F686"
                                toR = indx
                                print(toR)
                        lb.place(relx=0.99,rely=0.99 ,anchor=SE)
                    except:
                        flg = True
                    indx = indx+1
                Button(AFrm, text='DOWN', font=(cf['font'], 12),padx=5, pady=5, command=inc0).pack(pady=10)
                Label(AFrm, text='Devoloped by Javidh (2022)', font=('Consolas', 12)).place(relx=0.98, rely=0.98, anchor=SE)
                Frms1.append(AFrm)
                indx = indx-7
            Apg.clear()
            Apg.append(toR)
            Frms1[toR].tkraise()
            tk.bind('<Down>', inc0)
            tk.bind('<Up>', dec0)
            tk.mainloop()
        def onClick():
            ind = sel.get()
            print(usedBuf)
            for x in range(1, usedBuf):
                df = pd.read_csv('buff\\'+str(x)+'.csv')
                print(df.shape[1])
                if x == 1:
                    if ind < df.shape[1]-1:
                        routDis([x, ind])
                        break
                elif x == 2:
                    df0 = pd.read_csv('buff\\'+str(1)+'.csv')
                    ind = ind - df0.shape[1] +1
                    if ind < df.shape[1]-1:
                        routDis([x, ind])
                        break
                elif x == 3:
                    df1 = pd.read_csv('buff\\'+str(2)+'.csv')
                    ind = ind - df1.shape[1] +1
                    if ind < df.shape[1]-1:
                        routDis([x, ind])
                        break
        for wig in Root.winfo_children():
            wig.destroy()
        valueCnt = -1
        for x in range(1, usedBuf):
            df = pd.read_csv('buff\\'+str(x)+'.csv')
            print('buff\\'+str(x)+'.csv')
            for y in range(df.shape[1]):
                if y%9 == 0:
                    frm1 = Frame(Root)
                    frm1.place(relx=0.5, rely=0.5, relheight=0.98, relwidth=0.98, anchor=CENTER)
                    PgN = len(Frms)
                    Label(frm1, text=DisDta[x-1], font=(cf['font'], 12)).pack(pady=15)
                    Label(frm1, text='Pg - '+str(PgN), font=(cf['font'], 12)).place(relx=0.05, rely=0.05, anchor=NW)
                    Button(frm1, text='<-', font=(cf['font'], 12),padx=5, pady=5, command=dec).place(relx=0.025, rely=0.1)
                    Button(frm1, text='->', font=(cf['font'], 12),padx=5, pady=5, command=inc).place(relx=0.1, rely=0.1)
                    BackButton(frm1)
                    Label(frm1, text='Devoloped by Javidh (2022)', font=('Consolas', 12)).place(relx=0.98, rely=0.98, anchor=SE)
                    Frms.append(frm1)
                    if y==0:
                        continue
                D0 = Data[x-1]
                D1 = pd.read_csv(D0[0])
                if D0[-2] < 0:
                    D1 = D1.iloc[::-1]
                fromInd = None
                toInd = None
                for j, k in enumerate(list(D1.iloc[:, 0])):
                    if str(k) == dta[0]:
                        fromInd = j+1
                    if str(k) == dta[-1]:
                        toInd = j+1
                fromTim = str(df.iloc[fromInd, y])
                toTim = str(df.iloc[toInd, y])
                run = str(df.iloc[0, y])
                valueCnt = valueCnt+1
                if fromTim == 'nan' or toTim == 'nan':
                    continue
                toDis = dta[0]+ ' - ' +dta[1]+'  -  '+run+'\n'+fromTim+ ' - ' +toTim
                Radiobutton(frm1, text=toDis, variable=sel, value=valueCnt,indicator =0 , font=(cf['font'], 12), command = onClick, padx=10, pady=10).pack(pady=15)
        Root.bind('<Right>', inc)
        Root.bind('<Left>', dec)
        Frms[0].tkraise()
    for wid in trFrm.winfo_children():
        wid.destroy()
    linkD1 = getAsset(dta)
    LnkDta.append(linkD1)
    print('linkD1,',linkD1)
    Var = IntVar()
    Var.set(0)
    Label(trFrm, text="Available Trains", font=(cf['font'], 19)).pack()
    Load = Progressbar(trFrm, length=100, mode='indeterminate', orient=HORIZONTAL)
    Load.pack()
    for trn in linkD1:
        Root.update_idletasks()
        ind = trn[-1]
        siz = list(linkData.iloc[ind, :])
        if trn[-2] > 0:
            getData(siz=siz, lod=Load).to_csv('buff\\'+str(usedBuf)+'.csv')
            usedBuf = usedBuf+1
        else:
            lnk = revLink[siz[-2]]
            Nsiz = [siz[0], siz[1], lnk, siz[-1]]
            getData(siz=Nsiz, lod=Load).to_csv('buff\\'+str(usedBuf)+'.csv')
            usedBuf = usedBuf+1
    Load.destroy()
    for i,train in enumerate(linkD1):
        if train[-2] > 0:
            td = str(pd.read_csv(train[0]).iloc[0, 0]) +' - '+str(pd.read_csv(train[0]).iloc[-1, 0]) 
            DisDta.append(td)
            td = td + ' Local EMU'
        else:
            td = str(pd.read_csv(train[0]).iloc[-1, 0]) +' - '+ str(pd.read_csv(train[0]).iloc[0, 0]) 
            DisDta.append(td)
            td = td + ' Local EMU'
        Label(trFrm, text=td, font=(cf['font'], cf['S2'])).pack(pady=10, padx=10)
        Root.update()
    btn = Button(trFrm, text="Get Timing", font=(cf['font'], cf['S2']), command=lambda : Disp(linkD1))
    btn.pack(pady=15)
    if len(linkD1) == 0:
        btn['state'] = DISABLED
    else:
        btn['state'] = NORMAL
    find['state'] = NORMAL
 
mainWindow() 
Root.mainloop() 
