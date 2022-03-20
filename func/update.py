# -*- coding: utf-8 -*-
from shutil import rmtree, copytree
from os import remove, makedirs
from requests import get
from requests.packages import urllib3
from func.log import add_log

def u_check(version, proxy_address = ""):
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
    url = "http://mocha.cf/update/yande_re_downloader/?v=%s" % version # 更新接口
    urllib3.disable_warnings() # 关闭提示
    response = get(url, proxies = proxy, verify = False) # 发送GET请求，不验证ssl证书
    response.encoding = response.apparent_encoding # 防止中文乱码
    return response.text

def u_delete(path, type = None):
    try:
        if type == 'dir':
            rmtree(path)
        else:
            remove(path)
        return True
    except:
        return False

def u_mkdir(path):
    try:
        makedirs(path)
        return True
    except:
        return False

def u_copy(path,to):
    copytree(path, to, dirs_exist_ok = True)
    return True

def u_download(url, dir, filename, log_path, proxy_address = ""):
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
    urllib3.disable_warnings()
    response = get(url, proxies = proxy, verify = False) # 发送GET请求，不验证ssl证书
    err_count = 0
    while response.status_code != 200 and err_count < 5: # 下载失败且失败次数不大于五次则重新下载
        err_count += 1
        print(add_log("%s 下载失败，HTTP错误码： %s ，正在第 %s 次重试" % (url, response.status_code, err_count), log_path, 'Warn'))
        response = get(url, proxies = proxy, verify = False) # 重新下载
    else:
        if response.status_code != 200:
            print(add_log("%s 下载失败，HTTP错误码： %s ，超过最大重试次数" % (url, response.status_code), log_path, 'Error'))
            print(add_log("自动更新失败，请尝试手动更新", log_path, 'Error'))
            exit()
    u_mkdir(dir)
    with open(dir + "/" + filename, 'wb') as f: # 写入文件
        f.write(response.content)
    print(add_log("%s 下载成功" % url, log_path, 'Info'))
    return True