import pandas as pd

noun_dict={}
pandas_list=[]
noun_rootname="P{}_noun.xlsx"
for i in range(1,6):
    filename=noun_rootname.format(i)
    temp=pd.read_excel(filename)
    pandas_list.append(temp)
    for index in temp.index:
        if temp[0][index] not in noun_dict:
            noun_dict[temp[0][index]]=temp[1][index]
        else:
            noun_dict[temp[0][index]]+=temp[1][index]
        
list1=sorted(noun_dict.items(),key=lambda item:item[1],reverse=True)
df1=pd.DataFrame(list1)

for i in range(1,6):
    colname='P'+str(i)
    df1[colname]=0

for i in range(len(pandas_list)):
    temp=pandas_list[i]
    col='P'+str(i+1)
    for index in temp.index:
         values=df1.loc[df1[0]==temp[0][index],1].values
         if len(values)>0:
             Sum=values[0]
             df1.loc[df1[0]==temp[0][index],col]=temp[1][index]/Sum

df1.to_excel("noun_statistics.xlsx")
#Sum=df1.loc[df1[0]=='error',1].values[0]
#print(Sum)
#print(df1[1][df1[0]=='view'][0])