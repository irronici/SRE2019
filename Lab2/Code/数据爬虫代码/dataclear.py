import pandas as pd
import numpy as np
import requests
from threading import Thread
from bs4 import BeautifulSoup

reprocess_list=[]
del_list=[]
root_url="https://bugs.eclipse.org/bugs/show_bug.cgi?id={}"

df = pd.read_excel("bugs.xlsx")
for i in df.index:
   if pd.isnull(df['Comp'][i]):
       reprocess_list.append(i)

#print(reprocess_list)
def get(url,i):
    try:
        index=reprocess_list[i]
        ID=df['ID'][index]
        target_url=url.format(ID)
        req = requests.get(target_url, allow_redirects=False, timeout=10.0)
        bf=BeautifulSoup(req.text)
        #print(bf)
        if bf.find('div',id='error_msg',class_='throw_error'):
            print("Error ID :"+target_url)
            del_list.append(index)
    
        else:
            print(req.status_code, req.url)
            Table=bf.find('td',id='bz_show_bug_column_1',class_='bz_show_bug_column')   
            Component=Table.find_all('td')[6].get_text().replace(' ','').replace('\n',' ').split('  (showotherbugs)')[0]
            Importance=Table.find_all('td')[10].get_text().replace(' ','').replace('\n',' ')
            df['Abstract'][index]=bf.find('span',id='short_desc_nonedit_display').string
            df['Comp'][index]=Component
            df['Importance'][index]=Importance
    except:
        pass
#    
print("多线程爬取")
ts=[Thread(target=get,args=(root_url,i)) for i in range(200)]
for t in ts:
    t.start()
for t in ts:
    t.join()

print(del_list)
df=df.drop(del_list)
##print(len(df))
df.to_excel("bugs.xlsx")
