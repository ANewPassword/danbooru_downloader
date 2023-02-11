# -*- coding: utf-8 -*-

from requests import get
from requests.packages import urllib3
from func.log import add_log
from os import _exit

def yande_get_list(retry_max, page = 1, limit = 1000, tags = "", proxy_address = ""):
    proxy = proxy_address
    url = "https://yande.re/post.json?page=" + str(page) + "&limit=" + str(limit) + "&tags=" + tags # yande.re图片列表接口
    urllib3.disable_warnings() # 关闭提示
    err_count = 0
    while True:
        try:
            response = get(url, proxies = proxy, verify = False) # 发送GET请求，不验证ssl证书
            break
        except Exception as e:
            err_count += 1
            if err_count > retry_max and retry_max != -1:
                add_log("%s: %s" % (e.__class__.__name__, e), 'Error')
                _exit(1)
            else:
                add_log("%s: %s ，正在第 %s 次重试" % (e.__class__.__name__, e, err_count), 'Warn')
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