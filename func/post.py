# -*- coding: utf-8 -*-
from requests import get
from requests.packages import urllib3

def request(page = 1, limit = 1000, tags = "", proxy_address = ""):
        if proxy_address != "": # 使用代理
            proxy = {
                "http":proxy_address,
                "https":proxy_address,
            }
        else: # 不使用代理
            proxy = {
                "http":None,
                "https":None,
            }
        url = "https://yande.re/post.json?page=" + str(page) + "&limit=" + str(limit) + "&tags=" + tags # yande.re图片列表接口
        urllib3.disable_warnings() # 关闭提示
        response = get(url, proxies = proxy, verify = False) # 发送GET请求，不验证ssl证书
        response.encoding = response.apparent_encoding # 防止中文乱码（似乎也没有中文）
        return response.text
