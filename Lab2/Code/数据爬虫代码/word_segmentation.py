import nltk
import re
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd

symbol='1'
Plist=[]
noun_list={}
verb_list={}


df = pd.read_excel("bugs.xlsx")
for i in df.index:
    if pd.isnull(df['Importance'][i])==False and df['Importance'][i][1]==symbol and pd.isnull(df['Abstract'][i])==False:
        Plist.append(df['Abstract'][i])

lmtzr=WordNetLemmatizer() #词形还原
for abstract in Plist:
    sentence=abstract.split(' ')
    for i in range(len(sentence)):
        sentence[i]=re.sub('[^a-zA-Z]','',sentence[i])
        
    sen_tag=nltk.pos_tag([sen for sen in sentence if sen])  ##过滤掉‘’这样的空字符串
    for word in sen_tag:
        if word[1]=='NN' or word[1]=='NNS' or word[1]=='NNP' or word[1]=='NNPS':#名词
            new_word=lmtzr.lemmatize(word[0].lower(),'n')
            if new_word not in noun_list:
                noun_list[new_word]=1
            else:
                noun_list[new_word]+=1
                
        elif word[1]=='VB' or word[1]=='VBD' or word[1]=='VBG' or word[1]=='VBN' or word[1]=='VBN' or word[1]=='VBP' or word[1]=='VBZ':
            new_word=lmtzr.lemmatize(word[0].lower(),'v')
            if new_word not in verb_list:
                verb_list[new_word]=1
            else:
                verb_list[new_word]+=1

list1=sorted(noun_list.items(),key=lambda item:item[1],reverse=True)
list2=sorted(verb_list.items(),key=lambda item:item[1],reverse=True)
#print(list)

filename='P{}_{}.xlsx'
df1=pd.DataFrame(list1)
df1.to_excel(filename.format(symbol,'noun'))

df2=pd.DataFrame(list2)
df2.to_excel(filename.format(symbol,'verb'))


#abstract='DCR - Should Tree and TreeItem have an interface for tree ops? (1F931DR)'
#sentence=abstract.split(' ')
#for i in range(len(sentence)):
#    sentence[i]=re.sub('[^a-zA-Z]','',sentence[i])
#    
#print(sentence)
