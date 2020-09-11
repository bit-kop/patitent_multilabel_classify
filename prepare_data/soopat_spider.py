# 爬取糗事百科信息。

# 注意：爬取任何一个网站，首先要确定的就是这个网站是静态网站还是动态网站。
# 其次看看这个GET请求是否携带了特殊的参数。最后需要留意请求头中的Cookie信息。

import sqlite3
import re
from urllib.request import Request, urlopen
from fake_useragent import UserAgent


class DataTool(object):
    """
    工具类：对提取的元组中的数据，进行整理，删除无效的字符(\n，<br/>)
    """
    def process_data(self, origin_data):
        """
        用于对提取的原始元组进行数据处理的函数
        :param origin_tuple_data: 原始数据元组
        :return: 返回整理之后的元组
        """
        # 需要处理的数据：用户昵称、段子内容
        # sub()是正则表达式中的替换数据的方法，需要将\n这个字符替换成空字符
        # 参数：1. 替换规则 2. 替换结果 3. 要匹配的字符串
        # pattern = re.compile(r'[\u4e00-\u9fa5]*.*?[A-Z]*', re.S)
        data = re.sub(r"<font class='rh'>", '', origin_data)
        data = re.sub(r'</font>', '', data)
        data = re.sub(r'-', '', data)
        print(data)

        return data


class Spider(object):
    """
    爬虫类
    """
    def __init__(self):
        # 将各个页面通用的路径，不变的路径声明称为属性，调用方便，直接在这个属性的后面拼接页码。
        self.base_url = 'http://www.soopat.com/Home/Result?SearchWord=csi&PatentIndex='
        # 初始化请求头，伪造浏览器请求头中的User-Agent字段值，如果不修改User-Agent字段值，有一个默认的值User-Agent: python-3.7 xxx。
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.12 Safari/537.36'
        # }
        # 实例化工具类DataTool的对象
        self.tool = DataTool()
        # 实例化ua对象
        self.ua = UserAgent()

    def get_list_html(self, page_num):
        """
        获取每一个列表页的html网页源代码(这个获取的源代码就是 "右键-网页源代码" 中的内容)
        page_num：表示将要请求的页面的页码。
        :return:
        """
        # 构造每一页的url地址
        page_url = self.base_url + str(page_num)
        # 向page_url发送GET请求，开始获取当前页page_num的网页源代码
        # 先构造Request请求对象
        headers = {
            # random属性：从ie、firefox、chrome等浏览器的ua中，随机获取一个ua。
            'User-Agent': self.ua.random
        }
        request = Request(page_url, headers=headers)
        try:
            response = urlopen(request)
        except Exception as e:
            print('请求失败：地址{}，原因{}'.format(page_url, e))
            return None
        else:
            # try语句中的请求没有出现异常，就会执行else语句，如果出现异常了就不会执行else语句了。
            # print(response)
            html = response.read().decode()
            return html

    def parse_list_html(self, html):
        """
        解析上一个函数请求的html源代码
        :param html: 请求成功返回列表页的网页源代码，请求失败返回None
        :return:
        """
        if html:
            # 使用正则表达式开始解析网页源代码
            # 写正则注意事项：
            # 1. 尽量找到要匹配的零散数据所在的标签，而且这个标签必须和这些零散的数据一样能够循环。因为findall()函数在循环匹配数据的时候，是按照整个正则表达式规则循环匹配的。
            # 2. 在参考网页中 "审查元素" 来设置正则匹配规则的时候，一定要确认是否和 "网页源代码" 中的标签顺序、属性顺序等保持一致，如果不一致的话，必须参考 "网页源代码" 来设置正则匹配规则。因为 "审查元素" 中的Html代码是经过JS渲染之后的源代码。
            pattern = re.compile(r'<div class="PatentBlock".*?<h2 class="PatentTypeBlock".*?<a .*?>(.*?)<font size.*?', re.S)
            results_list = re.findall(pattern, html)
            processed_list = []
            for data in results_list:
                new_data = self.tool.process_data(data)
                processed_list.append(new_data)

            return processed_list

        else:
            print('html源代码为None')


if __name__ == '__main__':
    obj = Spider()

    # 循环爬取多页数据。
    for x in range(0, 600, 10):
        # range()取1到10之间的整数，能取到1，无法取到10
        html = obj.get_list_html(x)
        txt = '\n'.join(obj.parse_list_html(html))
        with open('../data/csi.txt', 'a', encoding='utf-8') as f:
            f.write(txt)
