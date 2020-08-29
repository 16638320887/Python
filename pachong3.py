import requests
import xlwt
from bs4 import BeautifulSoup
import urllib.request
import time
import lxml
import os
import time

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
print("爬取博客开始")
#添加
main_url='https://blog.csdn.net/qq_36958104'

page=1
#url = main_url + '/article/list/' + str(page)
#https://blog.csdn.net/qq_36958104/article/list/1
#    qq_36958104
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
ss=None
flag=0
count=1
page_flag=1
#for count in range(2000):
while(count<10):
    try:
        url = main_url + '/article/list/' + str(count)
        r=requests.get(url,headers=headers,timeout=10)
        print(r.text)
        # r.raise_for_status()    
        # print("网页编码是："+r.encoding)
        # # print(r.)
        # # 获取页面内容
        # # print(r.text)
        # 给excel放数据的  一个就是一行
        all_lists = []
        book = xlwt.Workbook(encoding='utf-8')#创建工作簿
        soup = BeautifulSoup(r.text, 'lxml')
        # 下面的这种方法会报错   TypeError("'NoneType' object is not callable")
        # ss=soup.findall("class",class_="article-item-box csdn-tracking-statistics")
        # 找到所有class为article-item-box csdn-tracking-statistics的节点
        row0 = ['文章标题','文章链接']#定义表头，即Excel中第一行标题
        sheet = book.add_sheet('bokewangzhi',cell_overwrite_ok=True)
        sheet.write(0,0,row0[0])#写入表
        
        sheet.write(0,1,row0[1])#写入表
        for s in soup.findAll(name="div", attrs={"class" :"article-item-box csdn-tracking-statistics"}):
            for ss in s.findAll(name="h4"):
                    sss=ss.find(name="a",href=True);
                    #print("文章标题："+ss.getText().replace("","").strip()+"\n文章链接："+sss['href'])
                    print("文章标题："+ss.getText().replace("","").strip())
                    opener.open(sss['href'])#打开网页刷访问
                    print(sss['href'])#打印网址链接                   
                    list=[ss.getText().replace("原创","").strip()]
                    all_lists.append(list)
                    print(list)
        #第一行开始
        i=1
        for all_list in all_lists:
            j=0
            for data in all_list:
                    sheet.write(i,j,data)#迭代列，并写入数据，#重新设置，需要cell_overwrite_ok=True
                    j+=1
            i+=1
        book.save("bokewangzhi.xls")
        count=count+1
        print("第",count,"页数据")
        #time.sleep(10)
        if count>5:
           count=0
           flag+=1
           print('爬取次数统计',flag*200)
           print("重新开始")
           time.sleep(60)
    except Exception as e:
     print("出现异常------异常信息："+repr(e));
     #os.system('python pachong3.py') #启动dos
    except urllib.error.HTTPError:
     print('urllib.error.HTTPError')
     time.sleep(60)
    except urllib.error.URLError:
     print('urllib.error.URLError')
     time.sleep(60)





    
