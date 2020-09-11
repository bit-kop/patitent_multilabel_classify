'''
爬取专利数据，网址：http://www.zlqiao.com/zlqiao/s-pat-b20.html?keywords=classification_A63B5%2F20
按照专利号爬取每个专利的摘要，然后写进文件，保存数据集
需要cookie
beautifulsoup部分需要根据具体的页面设定classname
page_num需要根据具体的页面设定，每个网站每页显示的条目数不一致
lixiaochao
'''

import requests
from bs4 import BeautifulSoup
import re
from distutils.filelist import findall
from lxml import etree

def get_pachong_data_one_page(base_url,page_num,classify_kws,Cookie):
    headers = {}
#     Host = "util.ms.casicloud.com"
#     User_Agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    Cookie = Cookie
#
#     headers['Host'] = Host
#     headers['User-Agent'] = User_Agent
    headers['Cookie'] = Cookie

# 第一次爬虫相关参数
    first_url = base_url+page_num+'.html?keywords=classification_'+classify_kws
    print(first_url)
    response = requests.get(first_url,headers=headers)
    contents = response.text
# print(contents)
    soup = BeautifulSoup(contents,'html.parser')

    total_abstract = []  # 第一次爬虫页面获取的摘要，但是显示不全
    total_href = []  # 需要第二次爬虫的页面
    for tag in soup.find_all('div',class_='msg-item-div mb40'):
        first_abstract = tag.find('div',class_='wysiwyg-color-gray').get_text()
        total_abstract.append(first_abstract)
        href = str(tag.find('a',class_='result-title mr10')).split('href="')[1].split('"')[0]
        total_href.append(href)

 # 第二次请求
    second_total_abstract = []  # 第二次爬虫页面获取的摘要
    second_total_label = [] # 对应摘要的label，个数不确定
    for href in total_href:
        second_url = base_url+ href
        response1 = requests.get(second_url,headers=headers)
        contents1 = response1.text
        soup1 = BeautifulSoup(contents1,'html.parser')

        # 爬取摘要
        for tag in soup1.find_all('div',class_='summary content-font mt10 mb10'):
            second_abstract = str(tag.find('span',id='patent-summary').get_text()).split('--')[0]
            second_total_abstract.append(second_abstract)

        # 爬取label

        tag_label = soup1.find_all('a', class_='classification-search tooltips')
        per_label = ''
        for label_text in tag_label:
            label = str(label_text).split('data-val="')[1].split('" ')[0]
            per_label += label + ','
        per_label = per_label.strip(',')
        second_total_label.append(per_label)
    return second_total_abstract, second_total_label

if __name__ == '__main__':
    # 需要爬取的数量
    total_abstract = []
    total_label = []
    base_url = 'http://www.zlqiao.com/zlqiao/'
    Cookie = 'JSESSIONID=1A8EB84169C582408BE65A8F6346CEF9; JSESSIONID=C9870E1E8A8838C5BF407E65BED0DE0B; Hm_lvt_2e0feccca9add6dc00fae2c02a5b1fbf=1598928096; Hm_lpvt_2e0feccca9add6dc00fae2c02a5b1fbf=1599010188'
    classify_kws = 'A63B5/20'
    per_page_num = 30  # 该网站每一页的数量是30
    # nums = [ i for i in range(450) if i%30==0]
    page_num = 's-pat-a'+str(90)
    second_total_abstract,second_total_label = get_pachong_data_one_page(base_url,page_num,classify_kws,Cookie)
    print(len(second_total_abstract))
    print(len(second_total_label))





