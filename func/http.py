# -*- coding: utf-8 -*-

from requests import get, post
from requests.packages import urllib3
from func.log import add_log
from func.debug import debug_info
from os import _exit

def simple_http_api_request(api, method, retry_max, header = None, data = None, proxy_address = ""):
    url = api # 接口
    if len(header) == 0:
        header = None
    if data == '':
        data = None
    proxy = proxy_address
    urllib3.disable_warnings() # 关闭提示
    err_count = 0
    while True:
        try:
            # 发送请求，不验证ssl证书
            if method == 'GET':
                response = get(url, headers = header, proxies = proxy, verify = False)
            elif method == 'POST':
                response = post(url, headers = header, data = data, proxies = proxy, verify = False)
            else:
                return False
            break
        except Exception as e:
            err_count += 1
            if err_count > retry_max and retry_max != -1:
                add_log("%s: %s" % (e.__class__.__name__, e), 'Error', debug_info())
                _exit(1)
            else:
                add_log("%s: %s ，正在第 %s 次重试" % (e.__class__.__name__, e, err_count), 'Warn', debug_info())
    response.encoding = response.apparent_encoding # 防止中文乱码（似乎也没有中文）
    return response.text

def check_update(version, proxy_address = "", update_api = None):
    proxy = proxy_address
    if update_api == None:
        url = "http://mocha.cf/update/yande_re_downloader/?v=%s" % version # 默认更新接口
    else:
        url = update_api
    urllib3.disable_warnings() # 关闭提示
    response = get(url, proxies = proxy, verify = False) # 发送GET请求，不验证ssl证书
    response.encoding = response.apparent_encoding # 防止中文乱码
    return response.text