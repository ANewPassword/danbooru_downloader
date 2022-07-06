# -*- coding: utf-8 -*-
from requests import get
from requests.packages import urllib3

def yande_get_list(page = 1, limit = 1000, tags = "", proxy_address = ""):
    proxy = proxy_address
    url = "https://yande.re/post.json?page=" + str(page) + "&limit=" + str(limit) + "&tags=" + tags # yande.re图片列表接口
    urllib3.disable_warnings() # 关闭提示
    response = get(url, proxies = proxy, verify = False) # 发送GET请求，不验证ssl证书
    response.encoding = response.apparent_encoding # 防止中文乱码（似乎也没有中文）
    return response.text

def check_update(version, proxy_address = "", host = None):
    proxy = proxy_address
    if host == None:
        url = "http://mocha.cf/update/yande_re_downloader/?v=%s" % version # 默认更新接口
    else:
        url = host
    urllib3.disable_warnings() # 关闭提示
    response = get(url, proxies = proxy, verify = False) # 发送GET请求，不验证ssl证书
    response.encoding = response.apparent_encoding # 防止中文乱码
    return response.text