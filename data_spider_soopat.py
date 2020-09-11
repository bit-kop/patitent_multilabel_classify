'''
爬取专利数据，网址：http://www.zlqiao.com/zlqiao/s-pat-b20.html?keywords=classification_A63B5%2F20
按照专利号爬取每个专利的摘要，然后写进文件，保存数据集
采用隧道代理，每请求一次就换一次ip，快代理：https://www.kuaidaili.com/usercenter/tps/?orderid=949910236789481
beautifulsoup部分需要根据具体的页面设定classname
page_num需要根据具体的页面设定，每个网站每页显示的条目数不一致
lixiaochao
'''
import os

import requests
from bs4 import BeautifulSoup
import re
from distutils.filelist import findall
from lxml import etree
import time
import re

#设置代理ip
import random

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[0].text + ':' + tds[1].text)
    return ip_list

# 从本地文件获取ip

def get_ip_list_local():

    ip_list = []
    with open('../data/dailiIP',encoding='utf-8') as f:
        ips = f.readlines()
        for ip in ips:
            ip = ip.strip().split('@')[0]
            print(ip)
            ip_list.append(ip)
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

#  设置10次重连，如果一次请求不成功，重新请求
def get_response(url,headers,proxies):
  i = 0
  while i < 10:
    try:
      response = requests.get(url, timeout=5,headers=headers,proxies=proxies)
      return response
    except requests.exceptions.RequestException:
      i += 1

# 获取每一页的数据，包括专利的摘要
def spider_per_page(headers,base_url,search_word,page_num,proxies):
    # time.sleep(1)
# 爬虫相关参数
    request_url = base_url+'SearchWord='+search_word+'&'+'PatentIndex='+page_num
    print(request_url)

    # 如果请求失败，就重新请求：
    response = get_response(request_url,headers=headers,proxies=proxies)
    # response = requests.get(request_url,headers=headers,proxies=proxies)
    print(response.status_code)
    contents = response.text
    soup = BeautifulSoup(contents,'lxml')
#

# 获取每页所有分类号与摘要
    all_label_per_page = []
    abstract_perpage=[]
    for tag in soup.find_all('div',attrs={"style":"min-height: 180px;max-width: 1080px;"}):
        text = tag.find('span', attrs={"class": "PatentContentBlock"}).get_text()

        str1 = text.split('：')[1]
        res1 = ''.join(re.findall('[\u4e00-\u9fa5]', str1))
        str2 = str1.split(res1[0])[0]
        all_label = re.sub('\(.*?\)[\u0041-\u005a]', '', str2.strip())

        all_label_per_page.append(all_label)
        abstract = str(text).split('摘要:')[1]
        abstract_perpage.append(abstract)

# 获取每页主分类号：PatentAuthorBlock
    main_label_per_page = []
    for each in soup.find_all('div',attrs={"style":"min-height: 180px;max-width: 1080px;"}):
        text = each.find('span', attrs={"class": "PatentAuthorBlock"}).get_text().strip()
        main_label = re.sub('\(.*?\)', '', str(text).split('主分类号：')[1].replace('I',''))
        main_label_per_page.append(main_label)

    return main_label_per_page,all_label_per_page,abstract_perpage

if __name__ == '__main__':

    cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
    main_label_path = os.path.join(cur_dir, 'data/D01D100_main_label.txt')
    all_label_path = os.path.join(cur_dir, 'data/D01D100_all_label.txt')
    abstract_path = os.path.join(cur_dir, 'data/D01D100_abstract.txt')

    headers = {}
    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    # Cookie = 'advu1=; advu2=; advu3=; advu4=; patentids=; __gads=ID=39749bef77b34ccb:T=1599030409:S=ALNI_MZIUfgDpVS0wdwUsoj_vnwNqcNW7g; auth=edb7T%2FgOOh1YSGegaOn0Aso5C0Uce5Mx1ymkox4uGBw7N%2BGlIhf2r6tQPqP4WVKj2ujIXbfe4j5DXhHuRutx8n97pjiv; suid=871541525AC14CBE; sunm=lixiaochaosb; ASP.NET_SessionId=o3nvyr5vafay5phfvezrdpki'
    # headers['Cookie'] = Cookie
    headers['User-Agent'] = User_Agent
    base_url = 'http://www.soopat.com/Home/Result?'
    search_word = 'D01D1/00'

    total_main_label = []
    total_all_label = []
    total_abstract = []

    nums = [i for i in range(2000) if i%10 ==0]
    print(nums)

    for num in nums:

        print('第'+str(round(num/10)+1)+'页：')

        tunnel = "tps189.kdlapi.com:15818"
        # time.sleep(1)
        # 用户名密码方式
        username = "t19910236789571"
        password = "6lnnfh8f"
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
            "https": "https://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
        }

        print(proxies)

        page_num = str(num)
        main_label_per_page,all_label_per_page,abstract_perpage = spider_per_page(headers, base_url, search_word, page_num,proxies)

        print(len(main_label_per_page))
        print(len(all_label_per_page))
        print(len(abstract_perpage))
        total_main_label +=main_label_per_page
        total_all_label+= all_label_per_page
        total_abstract+=abstract_perpage

    print('最后一共怕爬取到：' + str(len(total_main_label)) + '条数据')
    print(len(total_main_label))
    print(len(total_all_label))
    print(len(total_abstract))

    f1 = open(main_label_path, 'a', encoding='utf-8')
    f2 = open(all_label_path, 'a', encoding='utf-8')
    f3 = open(abstract_path, 'a', encoding='utf-8')

    for line in total_main_label:
        f1.write(str(line) + '\n')

    for line in total_all_label:
        f2.write(str(line) + '\n')

    for line in total_abstract:
        f3.write(str(line) + '\n')

    f1.close()
    f2.close()
    f3.close()



