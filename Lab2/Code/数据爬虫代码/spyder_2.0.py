import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from threading import Thread

max_urlcount=10000
root_url="https://bugs.eclipse.org/bugs/show_bug.cgi?id={}"
error_urllist=[]

Comp_list=['']*max_urlcount
Abstract_list=['']*max_urlcount
Importance_list=['']*max_urlcount
data={"Comp":Comp_list,"Abstract":Abstract_list,"Importance":Importance_list}
df=pd.DataFrame(data,index=range(max_urlcount))

def get(url,ID):
    try:
        target_url=url.format(ID)
        req = requests.get(target_url, allow_redirects=False, timeout=10.0)
        bf=BeautifulSoup(req.text)
        #print(bf)
        if bf.find('div',id='error_msg',class_='throw_error'):
            print("Error ID :"+target_url)
            error_urllist.append(ID)
          
        else:
            print(req.status_code, req.url)
            Table=bf.find('td',id='bz_show_bug_column_1',class_='bz_show_bug_column')   
            Component=Table.find_all('td')[6].get_text().replace(' ','').replace('\n',' ').split('  (showotherbugs)')[0]
            Importance=Table.find_all('td')[10].get_text().replace(' ','').replace('\n',' ')
            df['Abstract'][ID]=bf.find('span',id='short_desc_nonedit_display').string
            df['Comp'][ID]=Component
            df['Importance'][ID]=Importance
            
    except:
        pass

print("多线程爬取")
ts=[Thread(target=get,args=(root_url,i)) for i in range(max_urlcount)]
for t in ts:
    t.start()
for t in ts:
    t.join()

df=df.drop(error_urllist)
print(len(df))



df.to_csv('bugs.csv')

    




