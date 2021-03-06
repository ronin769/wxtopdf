#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''

# https://www.cnblogs.com/xiao-apple36/p/9447877.html#_label0
import os
import tempfile
import pdfkit
import urllib3
from PIL import Image
from bs4 import BeautifulSoup
from lxml.etree import XML
from selenium import webdriver
import time
import json
import random
import requests
import re
from lxml import etree
from selenium.common.exceptions import WebDriverException, NoSuchWindowException

str_to_bytes = lambda x: bytes(x, encoding='utf-8')
backgroud_image_p = re.compile('background-image:[ ]+url\(\"([\w\W]+?)\"\)')
js_content = re.compile('js_content.*?>((\s|\S)+)</div>')
find_article_json_re = re.compile('var msgList = (.*?)}}]};')
get_post_view_perm = re.compile('<script>var account_anti_url = "(.*?)";</script>')

agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]


# 类名-登录获取 cookie 和 token
class QRLogin():
    def __init__(self, loginName, loginPass):
        self.qrCookie = ""
        self.loginName = loginName
        self.loginPass = loginPass

    def wechatLogin(self):
        # 用webdriver启动谷歌浏览器
        print("启动浏览器，打开微信公众号登录界面...")
        driver = webdriver.Chrome()
        driver.get("https://mp.weixin.qq.com/")
        # driver.maximize_window()
        time.sleep(3)
        print("正在输入微信公众号登录账号和密码......")
        # 清空账号框中的内容
        driver.find_element_by_name("account").clear()
        driver.find_element_by_name("password").clear()

        # driver.find_element_by_name("account").click()
        driver.find_element_by_name("account").send_keys(self.loginName)
        # driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").send_keys(self.loginPass)

        # 在自动输完密码之后,需要手动点一下记住我,使用脚本模拟:
        print("请在登录界面点击:记住账号")
        driver.find_element_by_class_name("frm_checkbox_label").click()

        # 自动点击登录按钮进行登录
        driver.find_element_by_class_name("btn_login").click()

        while True:
            """
            扫码登录之后,如果未设置密码登录,会一直循环等待,直到设置了账号密码,为了避免频繁访问被封号,每个请求等13秒再执行
            """
            cookieData = {}
            # 扫码登录之后
            # 获取到的 cookie 中的键值对，列表转字典
            for cookie in driver.get_cookies():
                cookieData[cookie['name']] = cookie['value']

            # 二维码
            if "data_bizuin" in cookieData.keys():
                print("二维码_success")
                print(cookieData)
                self.qrCookie = cookieData
                # print("+++++++++++++++++++++")
                # print(self.qrCookie)

                return cookieData
                # break

            # 密码登录
            elif "noticeLoginFlag" in cookieData.keys():
                print("密码登录_success")
                print(cookieData)
                time.sleep(13)


            else:
                print("还未登录")
                print(cookieData)
                time.sleep(13)
        # driver.quit()

    def getToken(self, qrCookie):

        # from requests.packages import urllib3
        urllib3.disable_warnings()  # 关闭警告

        url = 'https://mp.weixin.qq.com'

        # 长链接
        # 增加重试连接次数
        session = requests.Session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 5
        time.sleep(13)

        # 请求
        response = session.get(url=url, cookies=qrCookie, verify=False, timeout=20)

        # print(responseUrl)
        # https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=2076568187
        responseUrl = str(response.url)

        # 正则找到 token=2076568187
        qrToken = re.findall(r'token=(\d+)', responseUrl)[0]

        print("获取token为：", qrToken)  # 2076568187
        return qrToken


# 类名-通过微信ID搜索公众号名和该公众号下的文章总数和文章列表
class GetBizDetail():
    def __init__(self, qrCookie, qrToken, bizName, headers, session):
        self.qrCookie = qrCookie
        self.qrToken = qrToken
        self.bizName = bizName
        self.headers = headers
        self.session = session

    def getBizNameLists(self):
        # 搜索微信公众号的接口地址
        searchBizNameUrl = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        # /cgi-bin/searchbiz?
        # action=search_biz&begin=0&count=5&query=lazy-thought&token=1988512250&lang=zh_CN&f=json&ajax=1

        # 搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
        getBizNameParams = {
            'action': 'search_biz',
            'token': self.qrToken,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': self.bizName,
            'begin': '0',
            'count': '5'
        }
        # 打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers

        bizNameResponse = self.session.get(url=searchBizNameUrl, cookies=self.qrCookie, headers=self.headers, params=getBizNameParams, timeout=30)

        # {"base_resp":{"ret":0,"err_msg":"ok"},"list":[{"fakeid":"MzA3NTEzMTUwNA==","nickname":"懒人在思考","alias":"lazy-thought","round_head_img":"http:\/\/mmbiz.qpic.cn\/mmbiz_png\/kicMePHlP6TCeqLFYtlvUv8dMiaKdqyOia6mOyGSb0HcEbmDks6diaibnSbZeRicUSACwwWLhFAibKJOicz5xjK3bwicQzw\/0?wx_fmt=png","service_type":1}],"total":1}

        # 取搜索结果中公众号列表
        bizNameLists = bizNameResponse.json().get('list')

        bizNameResponseLists = []
        for perBizName in bizNameLists:
            perBizNameDict = {}
            # print(perBizName)
            # {'fakeid': 'MzA3NTEzMTUwNA==', 'nickname': '懒人在思考', 'alias': 'lazy-thought', 'round_head_img': 'http://mmbiz.qpic.cn/mmbiz_png/kicMePHlP6TCeqLFYtlvUv8dMiaKdqyOia6mOyGSb0HcEbmDks6diaibnSbZeRicUSACwwWLhFAibKJOicz5xjK3bwicQzw/0?wx_fmt=png', 'service_type': 1}

            # print(perBizName.keys())
            #  dict_keys(['fakeid', 'nickname', 'alias', 'round_head_img', 'service_type'])

            # 获取这个公众号的 fakeid，后面爬取公众号文章需要此字段
            # print(perBizName['fakeid'])
            # MzA3NTEzMTUwNA==
            # print(perBizName['nickname'])
            # 懒人在思考

            perBizNameDict['fakeid'] = perBizName['fakeid']
            perBizNameDict['nickname'] = perBizName['nickname']
            bizNameResponseLists.append(perBizNameDict)

        print("查询到的公众号列表：", bizNameResponseLists)
        return bizNameResponseLists

    def getBizArticle(self, fake_id, page_num_tmp, page_limit_tmp):

        # 微信公众号文章接口地址
        searchBizArticleUrl = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        # 搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
        getBizArticleParams = {
            'token': self.qrToken,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': page_num_tmp,  # 第几页
            'count': page_limit_tmp,  # 每页几个
            'query': '',
            'fakeid': fake_id,
            'type': '9'
        }
        # 打开搜索的微信公众号文章列表页
        bizArticleResponse = session.get(url=searchBizArticleUrl, cookies=self.qrCookie, headers=self.headers, params=getBizArticleParams, timeout=30)
        # {"app_msg_cnt":203,"app_msg_list":[{"aid":"2651081564_1","appmsgid":2651081564,"cover":"https://mmbiz.qlogo.cn/mmbiz_jpg/kicMePHlP6TBIWIpuFaWyFuCp5LUrRKGCKGADdM3qKfXuIrQrRrBgS9PGa2jjzgrahMVI4tvlNcHjjY9DxBEo3Q/0?wx_fmt=jpeg","create_time":1572577784,"digest":"面向金融行业安全人员的一次群在线分享，一些区块链安全攻防实践观点供大家参考。","has_red_packet_cover":0,"is_pay_subscribe":0,"item_show_type":0,"itemidx":1,"link":"http://mp.weixin.qq.com/s?__biz=MzA3NTEzMTUwNA==&mid=2651081564&idx=1&sn=87b1e8343e83fdebde078e6c3ce2f843&chksm=8485d443b3f25d55a42764f141160477c1f70a93059c223c002bf03b903997eb5c85761e0d6f#rd","tagid":[],"title":"聊聊区块链安全攻防实践","update_time":1572577784},{"aid":"2651081553_1","appmsgid":2651081553,"cover":"https://mmbiz.qlogo.cn/mmbiz_jpg/kicMePHlP6TCMV3RIRImjF27elRnvgmVicYnSB0uDsI9jejduU8UP8ELGIgtASFt4liak1umc8w1sNqTdvwE7BFbQ/0?wx_fmt=jpeg","create_time":1568530098,"digest":"这就是我的世界观，无论是个人发展，还是做一番事业。","has_red_packet_cover":0,"is_pay_subscribe":0,"item_show_type":0,"itemidx":1,"link":"http://mp.weixin.qq.com/s?__biz=MzA3NTEzMTUwNA==&mid=2651081553&idx=1&sn=7d8674144135c5f1379742432768530e&chksm=8485d44eb3f25d584ea2f19e30e2057a2fe46014accdf2c91e2ffa1ccd392def4f975e9fe146#rd","tagid":[],"title":"做好特定领域者","update_time":1568530098}],"base_resp":{"err_msg":"ok","ret":0}}

        bizArticleResponseJson = bizArticleResponse.json()
        # print(bizArticleResponseJson)
        # exit()

        # 获取文章总数和文章列表
        bizArticleNum = bizArticleResponseJson.get('app_msg_cnt')
        bizArticleList = bizArticleResponseJson.get('app_msg_list')

        return bizArticleNum, bizArticleList


class WechatSogouException(Exception):
    """基于搜狗搜索的的微信公众号爬虫接口  异常基类
    """
    pass


class WechatSogouVcodeOcrException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 验证码 识别错误 异常类
    """
    pass


class WechatSogouRequestsException(WechatSogouException):
    """基于搜狗搜索的的微信公众号爬虫接口 抓取 异常类

    Parameters
    ----------
    errmsg : str or unicode
        msg
    r : requests.models.Response
        return of requests
    """

    def __init__(self, errmsg, r):
        WechatSogouException('{} [url {}] [content {}]'.format(errmsg, r.url, r.content))
        self.status_code = r.status_code


class WechatSogouStructuring():

    @staticmethod
    def replace_str_html(self, s):
        """替换html‘&quot;’等转义内容为正常内容

        Args:
            s: 文字内容

        Returns:
            s: 处理反转义后的文字
        """
        html_str_list = [
            ('&#39;', '\''),
            ('&quot;', '"'),
            ('&amp;', '&'),
            ('&yen;', '¥'),
            ('amp;', ''),
            ('&lt;', '<'),
            ('&gt;', '>'),
            ('&nbsp;', ' '),
            ('\\', '')
        ]
        for i in html_str_list:
            s = s.replace(i[0], i[1])
        return s

    @staticmethod
    def replace_html(self, data):
        if isinstance(data, dict):
            return dict([(self.replace_html(k), self.replace_html(v)) for k, v in data.items()])
        elif isinstance(data, list):
            return [self.replace_html(l) for l in data]
        elif isinstance(data, str) or isinstance(data, unicode):
            return self.replace_str_html(data)
        else:
            return data

    def __handle_content_url(self, content_url):
        content_url = self.replace_html(content_url)
        return ('http://mp.weixin.qq.com{}'.format(
            content_url) if 'http://mp.weixin.qq.com' not in content_url else content_url) if content_url else ''

    @staticmethod
    def __get_post_view_perm(self, text):
        result = get_post_view_perm.findall(text)
        if not result or len(result) < 1 or not result[0]:
            return None

        r = requests.get('http://weixin.sogou.com{}'.format(result[0]), timeout=30)
        if not r.ok:
            return None

        if r.json().get('code') != 'success':
            return None

        return r.json().get('msg')

    @staticmethod
    def list_or_empty(self, content, contype=None):
        assert isinstance(content, list), 'content is not list: {}'.format(content)

        if content:
            return contype(content[0]) if contype else content[0]
        else:
            if contype:
                if contype == int:
                    return 0
                elif contype == str:
                    return ''
                elif contype == list:
                    return []
                else:
                    raise Exception('only can deal int str list')
            else:
                return ''

    def get_first_of_element(self, element, sub, contype=None):
        """抽取lxml.etree库中elem对象中文字

        Args:
            element: lxml.etree.Element
            sub: str

        Returns:
            elem中文字
        """
        content = element.xpath(sub)
        return self.list_or_empty(content, contype)

    @staticmethod
    def get_elem_text(self, elem):
        """抽取lxml.etree库中elem对象中文字

        Args:
            elem: lxml.etree库中elem对象

        Returns:
            elem中文字
        """
        if elem != '':
            return ''.join([node.strip() for node in elem.itertext()])
        else:
            return ''

    @staticmethod
    def get_gzh_by_search(self, text):
        """从搜索公众号获得的文本 提取公众号信息

        Parameters
        ----------
        text : str or unicode
            搜索公众号获得的文本

        Returns
        -------
        list[dict]
            {
                'open_id': '', # 微信号唯一ID
                'profile_url': '',  # 最近10条群发页链接
                'headimage': '',  # 头像
                'wechat_name': '',  # 名称
                'wechat_id': '',  # 微信id
                'post_perm': '',  # 最近一月群发数
                'view_perm': '',  # 最近一月阅读量
                'qrcode': '',  # 二维码
                'introduction': '',  # 介绍
                'authentication': ''  # 认证
            }
        """
        post_view_perms = WechatSogouStructuring.__get_post_view_perm(text)

        page = etree.HTML(text)
        lis = page.xpath('//ul[@class="news-list2"]/li')
        relist = []
        for li in lis:
            url = self.get_first_of_element(li, 'div/div[1]/a/@href')
            headimage = self.format_image_url(self.get_first_of_element(li, 'div/div[1]/a/img/@src'))
            wechat_name = self.get_elem_text(self.get_first_of_element(li, 'div/div[2]/p[1]'))
            info = self.get_elem_text(self.get_first_of_element(li, 'div/div[2]/p[2]'))
            qrcode = self.get_first_of_element(li, 'div/div[3]/span/img[1]/@src')
            introduction = self.get_elem_text(self.get_first_of_element(li, 'dl[1]/dd'))
            authentication = self.get_first_of_element(li, 'dl[2]/dd/text()')

            relist.append({
                'open_id': headimage.split('/')[-1],
                'profile_url': url,
                'headimage': headimage,
                'wechat_name': wechat_name.replace('red_beg', '').replace('red_end', ''),
                'wechat_id': info.replace('微信号：', ''),
                'qrcode': qrcode,
                'introduction': introduction.replace('red_beg', '').replace('red_end', ''),
                'authentication': authentication,
                'post_perm': -1,
                'view_perm': -1,
            })

        if post_view_perms:
            for i in relist:
                if i['open_id'] in post_view_perms:
                    post_view_perm = post_view_perms[i['open_id']].split(',')
                    if len(post_view_perm) == 2:
                        i['post_perm'] = int(post_view_perm[0])
                        i['view_perm'] = int(post_view_perm[1])
        return relist

    @staticmethod
    def get_article_by_search_wap(self, keyword, wap_dict):
        datas = []

        for i in wap_dict['items']:
            item = str_to_bytes(i).replace(b'\xee\x90\x8a' + str_to_bytes(keyword) + b'\xee\x90\x8b',
                                           str_to_bytes(keyword))
            root = XML(item)
            display = root.find('.//display')
            datas.append({
                'gzh': {
                    'profile_url': display.find('encGzhUrl').text,
                    'open_id': display.find('openid').text,
                    'isv': display.find('isV').text,
                    'wechat_name': display.find('sourcename').text,
                    'wechat_id': display.find('username').text,
                    'headimage': display.find('headimage').text,
                    'qrcode': display.find('encQrcodeUrl').text,
                },
                'article': {
                    'title': display.find('title').text,
                    'url': display.find('url').text,  # encArticleUrl
                    'main_img': display.find('imglink').text,
                    'abstract': display.find('content168').text,
                    'time': display.find('lastModified').text,
                },
            })

        return datas

    @staticmethod
    def get_article_by_search(self, text):
        """从搜索文章获得的文本 提取章列表信息

        Parameters
        ----------
        text : str or unicode
            搜索文章获得的文本

        Returns
        -------
        list[dict]
            {
                'article': {
                    'title': '',  # 文章标题
                    'url': '',  # 文章链接
                    'imgs': '',  # 文章图片list
                    'abstract': '',  # 文章摘要
                    'time': ''  # 文章推送时间
                },
                'gzh': {
                    'profile_url': '',  # 公众号最近10条群发页链接
                    'headimage': '',  # 头像
                    'wechat_name': '',  # 名称
                    'isv': '',  # 是否加v
                }
            }
            :param self:
        """
        page = etree.HTML(text)
        lis = page.xpath('//ul[@class="news-list"]/li')

        articles = []
        for li in lis:
            url = self.get_first_of_element(li, 'div[1]/a/@href')
            if url:
                title = self.get_first_of_element(li, 'div[2]/h3/a')
                imgs = li.xpath('div[1]/a/img/@src')
                abstract = self.get_first_of_element(li, 'div[2]/p')
                time = self.get_first_of_element(li, 'div[2]/div/span/script/text()')
                gzh_info = li.xpath('div[2]/div/a')[0]
            else:
                url = self.get_first_of_element(li, 'div/h3/a/@href')
                title = self.get_first_of_element(li, 'div/h3/a')
                imgs = []
                spans = li.xpath('div/div[1]/a')
                for span in spans:
                    img = span.xpath('span/img/@src')
                    if img:
                        imgs.append(img)
                abstract = self.get_first_of_element(li, 'div/p')
                time = self.get_first_of_element(li, 'div/div[2]/span/script/text()')
                gzh_info = li.xpath('div/div[2]/a')[0]

            if title is not None:
                title = self.get_elem_text(title).replace("red_beg", "").replace("red_end", "")
            if abstract is not None:
                abstract = self.get_elem_text(abstract).replace("red_beg", "").replace("red_end", "")

            time = re.findall('timeConvert\(\'(.*?)\'\)', time)
            time = self.list_or_empty(time, int)
            profile_url = self.get_first_of_element(gzh_info, '@href')
            headimage = self.get_first_of_element(gzh_info, '@data-headimage')
            wechat_name = self.get_first_of_element(gzh_info, 'text()')
            gzh_isv = self.get_first_of_element(gzh_info, '@data-isv', int)

            articles.append({
                'article': {
                    'title': title,
                    'url': url,
                    'imgs': self.format_image_url(imgs),
                    'abstract': abstract,
                    'time': time
                },
                'gzh': {
                    'profile_url': profile_url,
                    'headimage': headimage,
                    'wechat_name': wechat_name,
                    'isv': gzh_isv,
                }
            })
        return articles

    def get_gzh_info_by_history(self, text):
        """从 历史消息页的文本 提取公众号信息

        Parameters
        ----------
        text : str or unicode
            历史消息页的文本

        Returns
        -------
        dict
            {
                'wechat_name': '',  # 名称
                'wechat_id': '',  # 微信id
                'introduction': '',  # 描述
                'authentication': '',  # 认证
                'headimage': ''  # 头像
            }
        """

        page = etree.HTML(text)
        profile_area = self.get_first_of_element(page, '//div[@class="profile_info_area"]')

        profile_img = self.get_first_of_element(profile_area, 'div[1]/span/img/@src')
        profile_name = self.get_first_of_element(profile_area, 'div[1]/div/strong/text()')
        profile_wechat_id = self.get_first_of_element(profile_area, 'div[1]/div/p/text()')
        profile_desc = self.get_first_of_element(profile_area, 'ul/li[1]/div/text()')
        profile_principal = self.get_first_of_element(profile_area, 'ul/li[2]/div/text()')

        return {
            'wechat_name': profile_name.strip(),
            'wechat_id': profile_wechat_id.replace('微信号: ', '').strip('\n'),
            'introduction': profile_desc,
            'authentication': profile_principal,
            'headimage': profile_img
        }

    def get_article_by_history_json(self, text, article_json=None):
        """从 历史消息页的文本 提取文章列表信息

        Parameters
        ----------
        text : str or unicode
            历史消息页的文本
        article_json : dict
            历史消息页的文本 提取出来的文章json dict

        Returns
        -------
        list[dict]
            {
                'send_id': '',  # 群发id，注意不唯一，因为同一次群发多个消息，而群发id一致
                'datetime': '',  # 群发datatime
                'type': '',  # 消息类型，均是49，表示图文
                'main': 0,  # 是否是一次群发的第一次消息
                'title': '',  # 文章标题
                'abstract': '',  # 摘要
                'fileid': '',  #
                'content_url': '',  # 文章链接
                'source_url': '',  # 阅读原文的链接
                'cover': '',  # 封面图
                'author': '',  # 作者
                'copyright_stat': '',  # 文章类型，例如：原创啊
            }

        """
        if article_json is None:
            article_json = find_article_json_re.findall(text)
            if not article_json:
                return []
            article_json = article_json[0] + '}}]}'
            article_json = json.loads(article_json)

        items = list()

        for listdic in article_json['list']:
            if str(listdic['comm_msg_info'].get('type', '')) != '49':
                continue

            comm_msg_info = listdic['comm_msg_info']
            app_msg_ext_info = listdic['app_msg_ext_info']
            send_id = comm_msg_info.get('id', '')
            msg_datetime = comm_msg_info.get('datetime', '')
            msg_type = str(comm_msg_info.get('type', ''))

            items.append({
                'send_id': send_id,
                'datetime': msg_datetime,
                'type': msg_type,
                'main': 1, 'title': app_msg_ext_info.get('title', ''),
                'abstract': app_msg_ext_info.get('digest', ''),
                'fileid': app_msg_ext_info.get('fileid', ''),
                'content_url': WechatSogouStructuring.__handle_content_url(app_msg_ext_info.get('content_url')),
                'source_url': app_msg_ext_info.get('source_url', ''),
                'cover': app_msg_ext_info.get('cover', ''),
                'author': app_msg_ext_info.get('author', ''),
                'copyright_stat': app_msg_ext_info.get('copyright_stat', '')
            })

            if app_msg_ext_info.get('is_multi', 0) == 1:
                for multi_dict in app_msg_ext_info['multi_app_msg_item_list']:
                    items.append({
                        'send_id': send_id,
                        'datetime': msg_datetime,
                        'type': msg_type,
                        'main': 0, 'title': multi_dict.get('title', ''),
                        'abstract': multi_dict.get('digest', ''),
                        'fileid': multi_dict.get('fileid', ''),
                        'content_url': WechatSogouStructuring.__handle_content_url(multi_dict.get('content_url')),
                        'source_url': multi_dict.get('source_url', ''),
                        'cover': multi_dict.get('cover', ''),
                        'author': multi_dict.get('author', ''),
                        'copyright_stat': multi_dict.get('copyright_stat', '')
                    })

        return list(filter(lambda x: x['content_url'], items))  # 删除搜狗本身携带的空数据

    @staticmethod
    def get_gzh_info_and_article_by_history(self, text):
        """从 历史消息页的文本 提取公众号信息 和 文章列表信息

        Parameters
        ----------
        text : str or unicode
            历史消息页的文本

        Returns
        -------
        dict
            {
                'gzh': {
                    'wechat_name': '',  # 名称
                    'wechat_id': '',  # 微信id
                    'introduction': '',  # 描述
                    'authentication': '',  # 认证
                    'headimage': ''  # 头像
                },
                'article': [
                    {
                        'send_id': '',  # 群发id，注意不唯一，因为同一次群发多个消息，而群发id一致
                        'datetime': '',  # 群发datatime
                        'type': '',  # 消息类型，均是49，表示图文
                        'main': 0,  # 是否是一次群发的第一次消息
                        'title': '',  # 文章标题
                        'abstract': '',  # 摘要
                        'fileid': '',  #
                        'content_url': '',  # 文章链接
                        'source_url': '',  # 阅读原文的链接
                        'cover': '',  # 封面图
                        'author': '',  # 作者
                        'copyright_stat': '',  # 文章类型，例如：原创啊
                    },
                    ...
                ]
            }
        """
        return {
            'gzh': WechatSogouStructuring.get_gzh_info_by_history(text),
            'article': WechatSogouStructuring.get_article_by_history_json(text)
        }

    def get_gzh_article_by_hot(self, text):
        """从 首页热门搜索 提取公众号信息 和 文章列表信息

        Parameters
        ----------
        text : str or unicode
            首页热门搜索 页 中 某一页 的文本

        Returns
        -------
        list[dict]
            {
                'gzh': {
                    'headimage': str,  # 公众号头像
                    'wechat_name': str,  # 公众号名称
                },
                'article': {
                    'url': str,  # 文章临时链接
                    'title': str,  # 文章标题
                    'abstract': str,  # 文章摘要
                    'time': int,  # 推送时间，10位时间戳
                    'open_id': str,  # open id
                    'main_img': str  # 封面图片
                }
            }
        """
        page = etree.HTML(text)
        lis = page.xpath('/html/body/li')
        gzh_article_list = []
        for li in lis:
            url = self.get_first_of_element(li, 'div[1]/h4/a/@href')
            title = self.get_first_of_element(li, 'div[1]/h4/a/div/text()')
            abstract = self.get_first_of_element(li, 'div[1]/p[1]/text()')
            xpath_time = self.get_first_of_element(li, 'div[1]/p[2]')
            open_id = self.get_first_of_element(xpath_time, 'span/@data-openid')
            headimage = self.get_first_of_element(xpath_time, 'span/@data-headimage')
            gzh_name = self.get_first_of_element(xpath_time, 'span/text()')
            send_time = xpath_time.xpath('a/span/@data-lastmodified')
            main_img = self.get_first_of_element(li, 'div[2]/a/img/@src')

            try:
                send_time = int(send_time[0])
            except ValueError:
                send_time = send_time[0]

            gzh_article_list.append({
                'gzh': {
                    'headimage': headimage,
                    'wechat_name': gzh_name,
                },
                'article': {
                    'url': url,
                    'title': title,
                    'abstract': abstract,
                    'time': send_time,
                    'open_id': open_id,
                    'main_img': main_img
                }
            })

        return gzh_article_list

    def format_image_url(self, url):
        if isinstance(url, list):
            return [self.format_image_url(i) for i in url]

        if url.startswith('//'):
            url = 'https:{}'.format(url)
        return url

    def get_article_detail(self, text, del_music=True, del_voice=True):
        """根据微信文章的临时链接获取明细

        1. 获取文本中所有的图片链接列表
        2. 获取微信文章的html内容页面(去除标题等信息)

        Parameters
        ----------
        text : str or unicode
            一篇微信文章的文本
        del_qqmusic: bool
            删除文章中的qq音乐
        del_voice: bool
            删除文章中的语音内容

        Returns
        -------
        dict
        {
            'content_html': str # 微信文本内容
            'content_img_list': list[img_url1, img_url2, ...] # 微信文本中图片列表

        }
        :param del_music:
        :param voice:
        :param qqmusic:
        :param delvoice2:
        :param delqqmusic2:
        :param del_voice:
        :param del_qqmusic:
        :param text:
        :param self:
        """
        # 1. 获取微信文本content
        # print(text)
        html_obj = BeautifulSoup(text, "lxml")
        content_text = html_obj.find('div', {'class': 'rich_media_content', 'id': 'js_content'})
        if content_text is None:
            print("+--+--+--+--+--+--+content_text is None, 等待 60 秒后继续+--+--+--+--+--+--+")
            time.sleep(60)
            return {
                'content_html': "content_html",
                'content_img_list': []
            }


        # 2. 删除部分标签
        if del_music:
            try:
                qqmusic = content_text.find_all('qqmusic') or []
                for music in qqmusic:
                    music.parent.decompose()
            except AttributeError as e:
                print(str(e))

        if del_voice:
            try:
                # voice是一个p标签下的mpvoice标签以及class为'js_audio_frame db'的span构成，所以将父标签删除
                voices = content_text.find_all('mpvoice') or []
                for voice in voices:
                    voice.parent.decompose()
            except AttributeError as e:
                print(str(e))

        # 3. 获取所有的图片 [img标签，和style中的background-image]
        all_img_set = set()
        all_img_element = content_text.find_all('img') or []
        # print(all_img_element)
        # ------------------------------------------------------------------------

        for ele in all_img_element:

            if 'data-src' not in ele.attrs.keys():
                continue

            img_url = self.format_image_url(ele.attrs['data-src'])
            del ele.attrs['data-src']
            ele.attrs['src'] = img_url
            if not img_url.startswith('http'):
                continue
                # raise WechatSogouException('img_url [{}] 不合法'.format(img_url))
            all_img_set.add(img_url)

        backgroud_image = content_text.find_all(style=re.compile("background-image")) or []
        for ele in backgroud_image:
            # 删除部分属性
            if ele.attrs.get('data-src'):
                del ele.attrs['data-src']

            if ele.attrs.get('data-wxurl'):
                del ele.attrs['data-wxurl']
            img_url = re.findall(backgroud_image_p, str(ele))
            if not img_url:
                continue
            all_img_set.add(img_url[0])

        # 4. 处理iframe
        all_img_element = content_text.find_all('iframe') or []
        for ele in all_img_element:
            # 删除部分属性
            if 'data-src' not in ele.attrs:
                continue
            img_url = ele.attrs['data-src']
            del ele.attrs['data-src']
            ele.attrs['src'] = img_url

        # 5. 返回数据
        all_img_list = list(all_img_set)
        content_html = content_text.prettify()
        # 去除div[id=js_content]
        content_html = re.findall(js_content, content_html)[0][0]
        return {
            'content_html': content_html,
            'content_img_list': all_img_list
        }


# 类名-公众号文章处理类
class WechatSogouClass():
    # wechatsogou报错，可以复用其中的处理函数
    # ws_api = wechatsogou.WechatSogouAPI()
    # content_info = ws_api.get_article_content(bizArticle['link'])

    def __init__(self, captcha_break_time=1, header=None, **kwargs):
        """初始化参数

        Parameters
        ----------
        captcha_break_time : int
            验证码输入错误重试次数
        proxies : dict
            代理
        timeout : float
            超时时间
        """
        assert isinstance(captcha_break_time, int) and 0 < captcha_break_time < 20

        self.captcha_break_times = captcha_break_time
        self.requests_kwargs = kwargs
        self.headers = header
        if self.headers:
            self.headers['User-Agent'] = random.choice(agents)
        else:
            self.headers = {'User-Agent': random.choice(agents)}

    def __get(self, url, session, headers):
        h = {}
        if headers:
            for k, v in headers.items():
                h[k] = v
        if self.headers:
            for k, v in self.headers.items():
                h[k] = v
        resp = session.get(url, headers=h, **self.requests_kwargs)

        if not resp.ok:
            raise WechatSogouRequestsException('WechatSogouAPI get error', resp)

        return resp

    @staticmethod
    def __set_cookie(suv=None, snuid=None, referer=None):
        suv = "test"
        snuid = "test"
        _headers = {'Cookie': 'SUV={};SNUID={};'.format(suv, snuid)}
        if referer is not None:
            _headers['Referer'] = referer
        return _headers

    @staticmethod
    def unlock_weixin_callback_example(self, url, req, resp, img, identify_image_callback):
        """手动打码解锁

        Parameters
        ----------
        url : str or unicode
            验证码页面 之前的 url
        req : requests.sessions.Session
            requests.Session() 供调用解锁
        resp : requests.models.Response
            requests 访问页面返回的，已经跳转了
        img : bytes
            验证码图片二进制数据
        identify_image_callback : callable
            处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example

        Returns
        -------
        dict
            {
                'ret': '',
                'errmsg': '',
                'cookie_count': '',
            }
        """
        # no use resp

        unlock_url = 'https://mp.weixin.qq.com/mp/verifycode'
        data = {
            'cert': time.time() * 1000,
            'input': identify_image_callback(img)
        }
        headers = {
            'Host': 'mp.weixin.qq.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': url
        }
        r_unlock = req.post(unlock_url, data, headers=headers)
        if not r_unlock.ok:
            raise WechatSogouVcodeOcrException(
                'unlock[{}] failed: {}[{}]'.format(unlock_url, r_unlock.text, r_unlock.status_code))

        return r_unlock.json()

    def __unlock_wechat(self, url, resp, session, unlock_callback=None, identify_image_callback=None):
        if unlock_callback is None:
            unlock_callback = self.unlock_weixin_callback_example

        r_captcha = session.get('https://mp.weixin.qq.com/mp/verifycode?cert={}'.format(time.time() * 1000))
        if not r_captcha.ok:
            raise WechatSogouRequestsException('WechatSogouAPI unlock_history get img', resp)

        r_unlock = unlock_callback(url, session, resp, r_captcha.content, identify_image_callback)

        if r_unlock['ret'] != 0:
            raise WechatSogouVcodeOcrException(
                '[WechatSogouAPI identify image] code: {ret}, msg: {errmsg}, cookie_count: {cookie_count}'.format(
                    ret=r_unlock.get('ret'), errmsg=r_unlock.get('errmsg'), cookie_count=r_unlock.get('cookie_count')))

    @staticmethod
    def __hosting_wechat_img(content_info_result, hosting_callback):
        """将微信明细中图片托管到云端，同时将html页面中的对应图片替换

        Parameters
        ----------
        content_info : dict 微信文章明细字典
            {
                'content_img_list': [], # 从微信文章解析出的原始图片列表
                'content_html': '', # 从微信文章解析出文章的内容
            }
        hosting_callback : callable
            托管回调函数，传入单个图片链接，返回托管后的图片链接

        Returns
        -------
        dict
            {
                'content_img_list': '', # 托管后的图片列表
                'content_html': '',  # 图片链接为托管后的图片链接内容
            }
        """
        assert callable(hosting_callback)

        content_img_list = content_info_result.pop("content_img_list")
        content_html = content_info_result.pop("content_html")
        for idx, img_url in enumerate(content_img_list):
            hosting_img_url = hosting_callback(img_url)
            if not hosting_img_url:
                # todo 定义标准异常
                raise Exception()
            content_img_list[idx] = hosting_img_url
            content_html = content_html.replace(img_url, hosting_img_url)

        return dict(content_img_list=content_img_list, content_html=content_html)

    @staticmethod
    def __readimg(content):
        f = tempfile.TemporaryFile()
        f.write(content)
        return Image.open(f)

    def identify_image_callback_by_hand(self, img):
        """识别二维码

        Parameters
        ----------
        img : bytes
            验证码图片二进制数据

        Returns
        -------
        str
            验证码文字
        """
        im = self.__readimg(img)
        im.show()
        return input("please input code: ")

    def __get_by_unlock(self, url, referer=None, unlock_platform=None, unlock_callback=None,
                        identify_image_callback=None, session=None):
        assert unlock_platform is None or callable(unlock_platform)

        if identify_image_callback is None:
            identify_image_callback = self.identify_image_callback_by_hand
        assert unlock_callback is None or callable(unlock_callback)
        assert callable(identify_image_callback)

        if not session:
            session = requests.session()
        resp = self.__get(url, session, headers=self.__set_cookie(referer=referer))
        resp.encoding = 'utf-8'
        if 'antispider' in resp.url or '请输入验证码' in resp.text:
            for i in range(self.captcha_break_times):
                try:
                    unlock_platform(url=url, resp=resp, session=session, unlock_callback=unlock_callback,
                                    identify_image_callback=identify_image_callback)
                    break
                except WechatSogouVcodeOcrException as e:
                    if i == self.captcha_break_times - 1:
                        raise WechatSogouVcodeOcrException(e)

            if '请输入验证码' in resp.text:
                resp = session.get(url)
                resp.encoding = 'utf-8'
            else:
                headers = self.__set_cookie(referer=referer)
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                resp = self.__get(url, session, headers)
                resp.encoding = 'utf-8'

        return resp

    # 该函数为wechatsogou.WechatSogouAPI.get_article_content
    def get_article_content(self, url, del_music=True, del_voice=True, unlock_callback=None,
                            identify_image_callback=None, hosting_callback=None, raw=False):
        """获取文章原文，避免临时链接失效

        Parameters
        ----------
        url : str or unicode
            原文链接，临时链接
        raw : bool
            True: 返回原始html
            False: 返回处理后的html
        del_qqmusic: bool
            True:微信原文中有插入的qq音乐，则删除
            False:微信源文中有插入的qq音乐，则保留
        del_mpvoice: bool
            True:微信原文中有插入的语音消息，则删除
            False:微信源文中有插入的语音消息，则保留
        unlock_callback : callable
            处理 文章明细 的时候出现验证码的函数，参见 unlock_callback_example
        identify_image_callback : callable
            处理 文章明细 的时候处理验证码函数，输入验证码二进制数据，输出文字，参见 identify_image_callback_example
        hosting_callback: callable
            将微信采集的文章托管到7牛或者阿里云回调函数，输入微信图片源地址，返回托管后地址

        Returns
        -------
        content_html
            原文内容
        content_img_list
            文章中图片列表

        Raises
        ------
        WechatSogouRequestsException
        :param raw:
        :param url:
        :param del_voice:
        :param del_music:
        :param voice:
        :param qqmusic:
        :param hosting_callback:
        :param identify_image_callback:
        :param unlock_callback:
        :param delVoice:
        :param delQqmusic:
        """

        resp = self.__get_by_unlock(url,
                                    unlock_platform=self.__unlock_wechat,
                                    unlock_callback=unlock_callback,
                                    identify_image_callback=identify_image_callback)

        resp.encoding = 'utf-8'
        if '链接已过期' in resp.text:
            raise WechatSogouException('get_article_content 链接 [{}] 已过期'.format(url))
        if raw:
            return resp.text

        structure_obj = WechatSogouStructuring()
        content_info_result = structure_obj.get_article_detail(resp.text, del_music=del_music, del_voice=del_voice)

        if hosting_callback:
            content_info_result = self.__hosting_wechat_img(content_info_result, hosting_callback)
        return content_info_result


if __name__ == '__main__':
    """
    1. 由于微信官方的限制,公众号每天最大访问量1000个请求,且每小时也有最大访问量限制,访问频率过快就会被封号24小时
    2. bizNameLists 是要访问的公众号列表
    3. 账号密码是自己注册的微信公众号平台,注册地址是 https://mp.weixin.qq.com/
    4. 启动此脚本需要使用与本机浏览器适配的 dirve,比如chrome drive,或者Firefox drive, https://mirrors.huaweicloud.com/chromedriver/
    """


    # 设置 requests 请求的参数
    session = requests.Session()
    session.keep_alive = False  # 保持长连接 = False
    session.adapters.DEFAULT_RETRIES = 5  # 重试 5 次

    # 登录微信公众号，获取登录之后的cookies
    loginName = "ronin769@163.com"
    loginPass = "sun826203..."

    # 要访问的公众号列表
    bizNameLists = ["sec-redclub", "moon_sec"]



    # 类名-登录获取 cookie 和 token, 以下方法二选一
    qrLoginObj = QRLogin(loginName, loginPass)

    print("\n--------------------------------------------------------------\
    获取Cookie-------------------------------------------------------------------")
    # # # # # 登录获取,第一次登录的时候
    qrCookie = qrLoginObj.wechatLogin()
    f = open("cookie.txt", "w")
    f.write(str(qrCookie))
    f.close()

    # # # # # 文件读取, cookie有效的时候登录
    # fopen = open("cookie.txt", "r")
    # qrCookieStr = fopen.readlines()
    # fopen.close()
    # qrCookie = eval(qrCookieStr[0])
    # print("qrcookie: ", qrCookie)

    print("\n--------------------------------------------------------------\
    获取token-------------------------------------------------------------------")
    qrToken = qrLoginObj.getToken(qrCookie)
    # print("qrToken", qrToken)




    headers = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    for bizName in bizNameLists:

        try:

            print("++--++--++--++--++--++--++--++--++--bizName: %s++--++--++--++--++--++--++--++--++--++--++--++--" % bizName)

            print("\n+--+--+--+--+--+--+--+--+等待 13 秒后继续，获取 bizName 查询到的公众号列表+--+--+--+--+--+--+--+--+")
            time.sleep(13)

            # 类名-通过微信ID搜索公众号名和该公众号下的文章总数和文章列表
            bizNameObj = GetBizDetail(qrCookie, qrToken, bizName, headers, session)
            bizNameLists = bizNameObj.getBizNameLists()
            for bizNameLine in bizNameLists:
                print("\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+通过微信号搜索到的公众号名称，开始获取每个公众号发布的文章个数及文章列表+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")

                # print(bizNameLine)
                # exit()
                print("公众号fakeid:", bizNameLine['fakeid'])
                print("公众号nickname:", bizNameLine['nickname'])

                # 创建的目录，目录名是公众号名，不存在则创建
                bizNameToPath = bizNameLine['nickname']
                if not os.path.exists(bizNameToPath):
                    os.mkdir(bizNameToPath)

                # pageLimit = 10 # 每页显示文章数，最大为10
                # for pageNum in range(0, bizArticleNum, pageLimit):

                # 获该公众号里的文章总数
                print("\n+--+--+--+--+--+--+--+--+等待 13 秒后继续，获取公众号文章总数的接口+--+--+--+--+--+--+--+--+")
                time.sleep(13)
                bizArticleNum, bizArticleList = bizNameObj.getBizArticle(bizNameLine['fakeid'], 0, 20)
                print("该 “%s” 公众号共有 %s 篇文章" % (bizNameLine['nickname'], bizArticleNum))

                # print("\n+--+--+--+--+--+--+--+--+等待 13 秒后继续，获取公众号每页列表的文章数+--+--+--+--+--+--+--+--+")
                # time.sleep(13)
                # temp2, bizArticleList = bizNameObj.getBizArticle(bizNameLine['fakeid'], 0, 5)

                # 获该公众号里的文章列表， 每次获取十个，直到全部获取
                pageLimit = int((len(bizArticleList) + 5) / 2)  # 每页显示文章数(也就是步进个数)，最大为5
                # print((bizArticleNum // pageLimit) + 1)
                # exit()
                # 第一次循环：从0页开始，每页5个
                # 第二次循环：从0＋５开始，每页5个
                # 第三次循环：从0＋５＋５开始，每页5个
                for pageNum in range(0, bizArticleNum, pageLimit):
                    print(
                        "+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+开始处理 %s 第 %s 页的 %s 篇文章+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+" % (
                            bizName,
                            pageNum // pageLimit + 1, pageLimit))

                    print("\n+--+--+--+--+--+--+--+--+等待 13 秒后继续，获取公众号文章列表的接口+--+--+--+--+--+--+--+--+")
                    time.sleep(13)

                    temp2, bizArticleList = bizNameObj.getBizArticle(bizNameLine['fakeid'], pageNum, pageLimit)

                    print("\n该 “%s” 公众号第 %s 页的 %s 篇文章列表：\n %s" % (
                        bizNameLine['nickname'], pageNum // pageLimit + 1, pageLimit, str(bizArticleList)))
                    # if pageNum + 1 == 3:
                    #     exit()
                    for num in range(len(bizArticleList)):
                        print(
                            "\n+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+处理 %s 第 %s 页的 第 %s 篇文章(都减一)，公众号标题：%s+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+" % (
                                bizName, (pageNum // pageLimit) + 1, num + 1, bizArticleList[num]['title']))
                        bizArticle = bizArticleList[num]

                        # 更新时间 换格式
                        updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(bizArticle['update_time']))

                        # print("bizArticle", bizArticle)
                        # print(bizArticle.keys())
                        print("公众号ID:", bizArticle['aid'])
                        print("文章ID:", bizArticle['appmsgid'])
                        print("图标URL:", bizArticle['cover'])
                        print("更新时间:", updateTime)
                        print("链接:", bizArticle['link'])
                        print("标题:", bizArticle['title'])
                        print("摘要:", bizArticle['digest'])
                        with open("wechat_spider.log", "a") as file_tmp:
                            file_tmp.write(
                                "\n+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+处理 %s 第 %s 页的 第 %s 篇文章(都减一)，公众号标题：%s+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+" % (
                                    bizName, (pageNum // pageLimit) + 1, num + 1, bizArticleList[num]['title']))
                            file_tmp.write("公众号ID :" + str(bizArticle['aid']))
                            file_tmp.write("文章ID: " + str(bizArticle['appmsgid']))
                            file_tmp.write("图标URL: " + str(bizArticle['cover']))
                            file_tmp.write("更新时间: " + str(updateTime))
                            file_tmp.write("链接: " + str(bizArticle['link']))
                            file_tmp.write("标题: " + str(bizArticle['title']))
                            file_tmp.write("摘要: " + str(bizArticle['digest']))

                        # 保存文件的名称
                        # filename = str(bizArticle['title']) + "_" + bizNameLine['nickname'] + "_" + str(updateTime) + ".pdf"
                        filename = str(bizArticle['title'])[:40] + "_" + str(updateTime) + ".pdf"
                        filename = filename.replace("/", "-")
                        filename = filename.replace("\\", "-")
                        filename = filename.replace("<", "-")
                        filename = filename.replace(">", "-")
                        filename = filename.replace("*", "-")
                        filename = filename.replace("?", "-")

                        filepath = bizNameToPath + "/" + filename

                        # 已经存在的文章就不用单独请求了，节省 13 秒延时
                        if os.path.exists(filepath):
                            continue

                        # html = htmlHander(bizArticle['link'])

                        # ws_api = wechatsogou.WechatSogouAPI()
                        # content_info = ws_api.get_article_content(bizArticle['link'])

                        # 类名-公众号文章处理类
                        wechatObj = WechatSogouClass()

                        print("\n+--+--+--+--+--+--+--+--+等待 13 秒后继续，获取公众号文章内容的接口+--+--+--+--+--+--+--+--+")
                        time.sleep(13)

                        # 访问页面并获取处理之后的响应数据，删除qq音乐和语音 <class 'dict'>
                        bizArticleData = wechatObj.get_article_content(bizArticle['link'], del_music=True,
                                                                       del_voice=True)
                        # print(bizArticleData['content_html'])

                        html = f'''
                                        <!DOCTYPE html>
                                        <html lang="en">
                                        <head>
                                            <meta charset="UTF-8">
                                            <title>{bizArticle['title']}</title>

                                        </head>
                                        <body>
                                        <h1 style="text-align: center;font-weight: 400;">{bizArticle['title']}</h1>
                                        </br>
                                        {bizArticleData['content_html']}
                                        </body>
                                        </html>
                                        '''

                        options = {
                            'page-size': 'A4',
                            'margin-top': '3mm',
                            'margin-right': '10mm',
                            'margin-bottom': '3mm',
                            'margin-left': '10mm',
                            # 'orientation':'Landscape',#横向
                            'encoding': "UTF-8",
                            'no-outline': None,
                            # 'footer-right':'[page]' 设置页码
                        }

                        # print(html)
                        try:
                            pdfkit.from_string(html, filepath, options=options)
                            print("\n+------------------------+文章保存成功! +------------------------+")
                        except Exception as e:
                            with open(filepath, "w") as f:
                                f.write(html)
                            print(str(e))
                            print("\n+------------------------+文章保存失败, 等待 60 秒后继续 +------------------------+")
                    #     time.sleep(60)
                    # try:
                    #     pdfkit.from_string(html, filepath, options=options)
                    #     print("\n+------------------------+文章保存成功! +------------------------+")
                    # except Exception as e:
                    #     print(str(e))
                    #     print("\n+------------------------+文章保存失败, 等待 60 秒后继续 +------------------------+")
                    #     time.sleep(60)



        except Exception as e:
            print("x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x", str(e), "bizName: ", bizName)
            print("\n+------------------------+等待 60 秒后继续 +------------------------+")
            time.sleep(60)
            continue
