import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from threading import Thread

max_urlcount=50
root_url="https://bugs.eclipse.org/bugs/show_bug.cgi?id={}"
error_urllist=[]

Comp_list=['']*max_urlcount
Abstract_list=['']*max_urlcount
Importance_list=['']*max_urlcount
data={"Dependency":['']}
df=pd.DataFrame(data,index=range(max_urlcount))

def isrepeat(addItem,list):
    for i in list:
        if addItem == i:
            return True
    return False


def get(url,ID,list):
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
            Table=bf.find('ul',class_='bug_urls')
            bug_urls=Table.find_all('a')
            for item in bug_urls:
                if str.isdigit(item.string) and isrepeat(item.string,list)==False:
                    list.append(item.string)
                    get(url,item.string,list)
                #print(item.get('href'))
                #print(item.string)  
    except:
        pass


def getDependencyUrls():
     search_url="https://bugs.eclipse.org/bugs/buglist.cgi?quicksearch=File"
     req=requests.get(search_url, allow_redirects=False, timeout=10.0)
     bf=BeautifulSoup(req.text)
     idTable=bf.find_all('td',class_="first-child bz_id_column")
     #for item in idTable:
     for i in range(max_urlcount):
         item=idTable[i]
         id=item.find('a').string
         dependencyUrls=[]
         dependencyUrls.append(id)
         get(root_url,id,dependencyUrls)
         if len(dependencyUrls)>1:
             df['Dependency'][id]=dependencyUrls
    
     print(df)
        
#get(root_url,542090)
getDependencyUrls()
