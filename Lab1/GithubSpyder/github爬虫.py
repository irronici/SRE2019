import requests
import json

def get_issue_json(start_pages,end_pages):
    issues_url="https://api.github.com/repos/microsoft/vscode/issues?page={}"   
    general_filename='IssuesData/page{}.json'
    for page in range(start_pages,end_pages+1):
        target_url=issues_url.format(page)
        filename=general_filename.format(page)
        print(target_url)
        req=requests.get(url=target_url)
        html=req.text
        f=open(filename,'w',encoding='utf-8')
        f.write(html)
        f.close()
        
def get_issue_title(start_pages,end_pages):
    general_filename='IssuesData/page{}.json'
    issues_record=[]
    for page in range(start_pages,end_pages+1):
        filename=general_filename.format(page)
        f=open(filename,'r',encoding='utf-8')
        Datas=json.load(f)
        
        print("第"+str(page)+"页:\n")
        for data in Datas:
            print(data['title'])
            
            #如果需要其他字段信息再修改吧
            issues_record.append(data['title'])
        print('\n')

    f=open('IssuesData/issue.txt','w',encoding='utf-8')
    for issue in issues_record:
        f.write(issue)
        f.write('\n')
    f.close()
    
def issue_spyder(start_pages,end_pages):
    get_issue_json(start_pages,end_pages)
    get_issue_title(start_pages,end_pages)
    
if __name__ == "__main__":
    issue_spyder(1,100)