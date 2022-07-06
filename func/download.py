# -*- coding: utf-8 -*-
from os import _exit
from asyncio import exceptions
import requests
from requests.packages import urllib3
from urllib.parse import unquote
import queue
import threading
from time import sleep
from random import uniform
from func.fileio import file_mkdir, file_is_exist, file_write_binary, file_delete
from func.log import add_log
from func.chksum import md5sum
from core.constant import *
urllib3.disable_warnings()

download_count = 0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

class download(threading.Thread):
    def __init__(self, que, path, proxy_address, options, retry_max):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True # 守护进程
        self.que = que
        self.path = path
        self.proxy = proxy_address
        self.options = options
        self.retry_max = retry_max

    def run(self):
        global download_count
        while True:
            if not self.que.empty():
                # sleep(uniform(0.2, 0.5)) # 防止写入日志出错
                file_mkdir(self.path)
                get_img = self.que.get() #取出一个图片
                get_img_url = get_img['url']
                get_img_hash = get_img['hash']
                file_name = get_img_url.split("/")
                file_name = unquote(file_name[-1]) # 获取图片名称
                for char in file_name: # 判断图片名称是否包含以上字符，如果包含则替换为空字符
                    if char in unsupported_file_name:
                        file_name = file_name.replace(char, '')
                if file_is_exist(self.path + '/' + file_name): # 根据文件名判断图片是否已经下载，此处存在一个问题：如果文件tags被修改会造成图片重复
                    add_log("%s 已存在" % file_name, 'Warn')
                    download_count += 1
                    continue
                add_log("正在下载 %s" % file_name, 'Info')
                try:
                    res = requests.get(get_img_url, proxies = self.proxy, verify = False) # 下载
                except Exception as e:
                    add_log("%s: %s" % (e.__class__.__name__, e), 'Error')
                    _exit(1)
                err_count = 0
                while res.status_code != 200 and (err_count < self.retry_max or self.retry_max == -1): # 下载失败且失败次数不大于指定次数则重新下载
                    err_count += 1
                    add_log("%s 下载失败，HTTP错误码： %s ，正在第 %s 次重试" % (file_name, res.status_code, err_count), 'Warn')
                    file_delete(self.path + '/' + file_name)
                    try:
                        res = requests.get(get_img_url, proxies = self.proxy, headers=headers, verify = False) # 重新下载
                    except Exception as e:
                        add_log("%s: %s" % (e.__class__.__name__, e), 'Error')
                        _exit(1)
                else:
                    if res.status_code != 200:
                        add_log("%s 下载失败，HTTP错误码： %s ，超过最大重试次数" % (file_name, res.status_code), 'Error')
                        file_delete(self.path + '/' + file_name)
                        download_count += 1
                        continue
                if res.status_code == 200:
                    err_count = 0
                    file_write_binary('{}{}{}'.format(self.path, '/', file_name), res.content) # 写入文件
                    if chksums_str in self.options:
                        add_log("%s 下载成功，正在校验文件完整性" % file_name, 'Info')
                        chksum_res = md5sum('{}{}{}'.format(self.path, '/', file_name), get_img_hash)
                        if chksum_res == True:
                            add_log("%s 校验成功，%s -> %s 匹配" % (file_name, get_img_hash, get_img_hash), 'Info')
                        else:
                            while chksum_res != True and (err_count < self.retry_max or self.retry_max == -1):
                                err_count += 1
                                add_log("%s 校验失败，%s -> %s 不匹配，正在第 %s 次重试" % (file_name, chksum_res, get_img_hash, err_count), 'Warn')
                                file_delete(self.path + '/' + file_name)
                                try:
                                    res = requests.get(get_img_url, proxies = self.proxy, headers=headers, verify = False) # 重新下载
                                except Exception as e:
                                    add_log("%s: %s" % (e.__class__.__name__, e), 'Error')
                                    _exit(1)
                                file_write_binary('{}{}{}'.format(self.path, '/', file_name), res.content)
                                add_log("%s 下载成功，正在校验文件完整性" % file_name, 'Info')
                                chksum_res = md5sum('{}{}{}'.format(self.path, '/', file_name), get_img_hash)
                            else:
                                if chksum_res == True:
                                    add_log("%s 校验成功，%s -> %s 匹配" % (file_name, get_img_hash, get_img_hash), 'Info')
                                    add_log("%s 下载成功" % file_name, 'Info')
                                if err_count >= self.retry_max and self.retry_max != -1:
                                    file_delete(self.path + '/' + file_name)
                                    add_log("%s 校验失败，%s -> %s 不匹配，超过最大重试次数" % (file_name, chksum_res, get_img_hash), 'Error')
                    else:
                        add_log("%s 下载成功" % file_name, 'Info')
                    download_count += 1
            else:
                return True
 
def start_download(list, num, path, proxy_address, options, retry_max): # 下载器接口
    global download_count
    add_log("开始本次下载任务", 'Info')
    decoding = 'utf8'
    num = num if num <= len(list) else len(list)
    que = queue.Queue()
    for l in list:
        que.put(l)
    for i in range(num):
        d=download(que, path, proxy_address, options, retry_max)
        d.start()
    while True: # hold
        if que.empty() and len(list) <= download_count:
            add_log("本次下载任务完成", 'Info')
            download_count = 0
            break
        sleep(1)

def update_download(url, dir, filename, proxy_address):
    proxy = proxy_address
    urllib3.disable_warnings()
    response = requests.get(url, proxies = proxy, verify = False) # 发送GET请求，不验证ssl证书
    err_count = 0
    while response.status_code != 200 and err_count < 5: # 下载失败且失败次数不大于五次则重新下载
        err_count += 1
        add_log("%s 下载失败，HTTP错误码： %s ，正在第 %s 次重试" % (url, response.status_code, err_count), 'Warn')
        response = requests.get(url, proxies = proxy, verify = False) # 重新下载
    else:
        if response.status_code != 200:
            add_log("%s 下载失败，HTTP错误码： %s ，超过最大重试次数" % (url, response.status_code), 'Error')
            add_log("自动更新失败，请尝试手动更新", 'Error')
            exit()
    file_mkdir(dir)
    file_write_binary(dir + "/" + filename, response.content, mode = 'wb') # 写入文件
    add_log("%s 下载成功" % url, 'Info')
    return True