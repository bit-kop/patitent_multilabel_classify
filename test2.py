import re

import requests
from bs4 import BeautifulSoup

headers = {}
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
# Cookie = 'advu1=; advu2=; advu3=; advu4=; patentids=; __gads=ID=39749bef77b34ccb:T=1599030409:S=ALNI_MZIUfgDpVS0wdwUsoj_vnwNqcNW7g; auth=edb7T%2FgOOh1YSGegaOn0Aso5C0Uce5Mx1ymkox4uGBw7N%2BGlIhf2r6tQPqP4WVKj2ujIXbfe4j5DXhHuRutx8n97pjiv; suid=871541525AC14CBE; sunm=lixiaochaosb; ASP.NET_SessionId=o3nvyr5vafay5phfvezrdpki'
# headers['Cookie'] = Cookie
headers['User-Agent'] = User_Agent

response = requests.get('http://www.soopat.com/Home/Result?SearchWord=A01H1%2F00&PatentIndex=500',headers=headers)
contents = response.text
soup = BeautifulSoup(contents,'lxml')
#

# 获取每页所有分类号与摘要
for tag in soup.find_all('div',attrs={"style":"min-height: 180px;max-width: 1080px;"}):
    text = tag.find('span', attrs={"class": "PatentContentBlock"}).get_text()
    # print(text)
    str1 = text.split('：')[1]
    res1 = ''.join(re.findall('[\u4e00-\u9fa5]', str1))
    str2 = str1.split(res1[0])[0]
    all_label = re.sub('\(.*?\)[\u0041-\u005a]', '', str2.strip())
    print(all_label)
    abstract = str(text).split('摘要:')[1]
    print(abstract)
for each in soup.find_all('div',attrs={"style":"min-height: 180px;max-width: 1080px;"}):
    text = each.find('span', attrs={"class": "PatentAuthorBlock"}).get_text().strip()
    main_label = re.sub('\(.*?\)', '', str(text).split('主分类号：')[1].replace('I',''))
    print(main_label)