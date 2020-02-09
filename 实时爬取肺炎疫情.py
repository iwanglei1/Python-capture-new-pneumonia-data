# coding=utf-8
'''
time 2020-02-09
author wanglei
'''
import urllib.request
import bs4
import lxml
import time
from selenium import webdriver
from twilio.rest import Client


url ="https://ncov.dxy.cn/ncovh5/view/pneumonia_peopleapp?from=timeline&isappinstalled=0"
def getpage(url):
    driver = webdriver.Firefox()
    try :
        driver.get(url)
        driver.refresh()
        time.sleep(2)
    except Exception as e:
        pass
    time.sleep(2)
    a = driver.page_source
    driver.close()
    return a  #a即是我想要的异步加载完成后的html文件


def getHtml(url):                 #获取原始页面
    page=urllib.request.urlopen(url)
    html=page.read()
    return html

def getData(html):
    soup=bs4.BeautifulSoup(html,"html.parser")
    title=soup.title.string
    QZ_total=soup.find("strong",style="color: rgb(247, 76, 49);").string #总人数
    QZ_today_add=soup.find("em",style="color: rgb(247, 76, 49);").string #总人数相比昨日
    YS_total=soup.find("strong",style="color: rgb(247, 130, 7);").string #总疑似人数
    YS_today_add=soup.find("em",style="color: rgb(247, 130, 7);").string #总疑似比昨日
    ZZ_total = soup.find("strong", style="color: rgb(162, 90, 78);").string  #重症总人数
    ZZ_today_add = soup.find("em", style="color: rgb(162, 90, 78);").string  #重症比昨日
    SW_total = soup.find("strong", style="color: rgb(93, 112, 146);").string  # 死亡总人数
    SW_today_add = soup.find("em", style="color: rgb(93, 112, 146);").string  # 死亡比昨日
    ZY_total = soup.find("strong", style="color: rgb(40, 183, 163);").string  # 治愈总人数
    ZY_today_add = soup.find("em", style="color: rgb(40, 183, 163);").string  # 治愈比昨日
    Total_data=[]
    temp=[QZ_total,QZ_today_add,YS_total,YS_today_add,ZZ_total,ZZ_today_add,SW_total,SW_today_add,ZY_total,ZY_today_add]
    Total_data.extend(temp)
    #td_list=soup.find_all('td')
    #quezhen=soup.find_all('td')
    return Total_data
    #return title

#page=getHtml(url)

def Send_SMS(message):
    account_sid = 'AC50142b0434f722ac0b0d275bebdd1172'
    auth_token = '7fb3cf8b93554e46fce5565890428de0'
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=message,
        from_='+12013992154',
        to='+86 13563303463'
    )


while(1):
    page = getpage(url)
    x = getData(page)  # "X"  为抓取的疫情数据，依次为： 总人数、总人数+、总疑似、总疑似+、总重症、总重症+、总死亡、总死亡+、总治愈、总治愈+
    #print(x[0])

    ##构建发送的简单字符串
    Message_YQ1="早上好呀 今天又是充满希望的一天"
    Message_YQ2="今天新冠肺炎的总确诊人数为： "+str(x[0])+",较昨天： "+str(x[1])+",总疑似人数为： "+str(x[2])+",总疑似人数较昨天： "+str(x[3]) \
        + ",重症人数为： "+str(x[4]) +",较昨天： " +str(x[5])+",死亡总人数为： " +str(x[6]) + ",较昨天增加了： "+str(x[7]) \
        + ",治愈总人数： "+str(x[8]) + ",较昨天增加了： "+str(x[9])
    Message_YQ=Message_YQ1+Message_YQ2
    Send_SMS(Message_YQ)
    print(Message_YQ)
    time.sleep(21600)  # 隔多久发送短信提醒 单位为秒

