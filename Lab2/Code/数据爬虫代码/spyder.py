import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from threading import Thread
#import json

#url="https://bugs.eclipse.org/bugs/buglist.cgi?quicksearch=bugs"   
#req=requests.get(url=url)
#html=req.text
def get(url,ID):
    try:
        url=url.format(ID)
        req = requests.get(url, allow_redirects=False, timeout=10.0)
        #print(req.status_code, req.url)
        bf=BeautifulSoup(req.text)
        Table=bf.find('td',id="bz_show_bug_column_1",class_="bz_show_bug_column")    

        importance=Table.find_all('td')[10].get_text().replace(' ','').replace('\n',' ')
        print(importance)
        df['Importance'][ID]=importance

    except:
        pass


ID_list=[]
Comp_list=[]
Abstract_list=[]
Importance_list=[]

html=open("bugs.txt").read()
bf=BeautifulSoup(html)

for k in bf.find_all('td',class_="first-child bz_id_column"):
    ID_list.append(k.find('a').string)
    
for k in bf.find_all('td',class_="bz_component_column nowrap"):
    Comp_list.append(k.find('span').string)

for k in bf.find_all('td',class_="bz_short_desc_column"):
    Abstract_list.append(k.find('a').string)
    
Importance_list=['']*len(ID_list)
data={"Comp":Comp_list,"Abstract":Abstract_list,"Importance":Importance_list}
df=pd.DataFrame(data,index=ID_list)

print("多线程爬取")
url="https://bugs.eclipse.org/bugs/show_bug.cgi?id={}"   
ts=[Thread(target=get,args=(url,ID_list[i])) for i in range(len(ID_list))]
for t in ts:
    t.start()
for t in ts:
    t.join()

print(len(Importance_list))
print(df['Importance'][ID_list[0]])
df.to_csv("bugs.csv")


    
    



    