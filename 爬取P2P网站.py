# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import numpy as np
import requests
import time
import random
from bs4 import BeautifulSoup
 
# s=requests.session()
 
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
#根据浏览器下自行修改

headers['Cookie'] = 'gr_user_id=a11ecd75-ae49-4853-b332-6d7ef973a8d0; Hm_lvt_603ab75906557bfe372ca494468e3e1b=1523261865; Hm_lpvt_603ab75906557bfe372ca494468e3e1b=1523261944; user_id=q9A0J5Jo; user_session=a8d9a123-9644-462b-b187-2ba087e7f508; 0a1b4118dd954ec3bcc69da5138bdb96_gr_last_sent_sid_with_cs1=718060fd-2dca-44b0-9d56-1714a3b50f57; 0a1b4118dd954ec3bcc69da5138bdb96_gr_last_sent_cs1=105038; 0a1b4118dd954ec3bcc69da5138bdb96_gr_cs1=105038'
#根据浏览器F12下的Request Headers->Cookie自行复制上去即可
 
driver = webdriver.Chrome()

def loginRRD(username, password):
    try:
        print(u'准备登陆人人贷...')
        driver.get("https://www.we.com/loginPage.action")
        elem_user = driver.find_element_by_name("j_username")
        elem_user.send_keys(username)
        elem_pwd = driver.find_element_by_name("j_password")
        elem_pwd.send_keys(password)
        
        time.sleep(20)
        print(u'登录成功')
    except Exception as e:
        print("error")
    finally:
        print(u'sss')
 
def parse_userinfo(loanid):#自定义解析借贷人信息的函数
    timestamp=str(int(time.time())) + '%03d' % random.randint(0,999)
    urll="http://www.we.com/lend/detailPage.action?loanId=%.0f&timestamp=" % loanid+timestamp   #这个urll我也不知道怎么来的，貌似可以用urll="http://www.we.com/loan/%f" % loanid+timestamp  <br>    #(就是页面本身，我也没试过)

    # result = s.get(urll,headers=headers)
    driver.get(urll)
    # html = BeautifulSoup(result.text,'lxml')
    html = BeautifulSoup(driver.page_source,'lxml')
    info = html.find_all('table',class_="ui-table-basic-list")
    info1= info[0]
    info2 = info1.find_all('div',class_="basic-filed")
    userinfo = {}
    for item in info2:
        vartag = item.find('span')
        var = vartag.string
        if var == '信用评级':
            var = '信用评分'
            pf1 = repr(item.find('em'))
            value = re.findall(r'\d+',pf1)
        else:
            valuetag = item.find('em')
            value = valuetag.string
        userinfo[var]=value
    data = pd.DataFrame(userinfo)
    return data
 
rrd=pd.read_csv('loanId.csv') #loanId是之前散标数据中的loanId,将其单独整理为一个csv文档
loanId=rrd.ix[:,'loanId']
user_info = ['昵称', '信用评分',
 
            '年龄', '学历', '婚姻',
 
            '申请借款', '信用额度', '逾期金额', '成功借款', '借款总额', '逾期次数','还清笔数', '待还本息', '严重逾期',
 
            '收入', '房产', '房贷', '车产', '车贷',
 
'公司行业', '公司规模', '岗位职位', '工作城市', '工作时间']
 
table = pd.DataFrame(np.array(user_info).reshape(1, 24), columns=user_info)
 
username = "13554764024"
password = "chhh654171572"

loginRRD(username, password)
# parse_userinfo(2511380)
 
# i = 1 
# for loanid in loanId:
#     table = pd.concat([table, parse_userinfo(loanid)])
#     print(i)
#     i += 1 #看一下循环多少次

table = pd.concat([table, parse_userinfo(2511380)])
print(table)
 
table.to_csv('userinfo.csv',header=False,encoding="utf_8_sig")
