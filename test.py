from bs4 import BeautifulSoup
import requests
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

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

if __name__ == '__main__':
    # 隧道域名:端口号
    tunnel = "tps189.kdlapi.com:15818"

    # 用户名密码方式
    username = "t19910236789571"
    password = "6lnnfh8f"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    print(proxies)
    #
    headers = {}
    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    # Cookie = 'advu1=; advu2=; advu3=; advu4=; patentids=; __gads=ID=39749bef77b34ccb:T=1599030409:S=ALNI_MZIUfgDpVS0wdwUsoj_vnwNqcNW7g; auth=edb7T%2FgOOh1YSGegaOn0Aso5C0Uce5Mx1ymkox4uGBw7N%2BGlIhf2r6tQPqP4WVKj2ujIXbfe4j5DXhHuRutx8n97pjiv; suid=871541525AC14CBE; sunm=lixiaochaosb; ASP.NET_SessionId=o3nvyr5vafay5phfvezrdpki'
    # headers['Cookie'] = Cookie
    headers['User-Agent'] = User_Agent
    response = requests.get('http://www.soopat.com/Home/Result?SearchWord=A63B5/20&PatentIndex=0', headers=headers,proxies=proxies)
    contents = response.text
    print(response.status_code)
    print(contents)
