# -*- coding: utf-8 -*-
import requests
from requests.packages import urllib3
from urllib.parse import unquote
import queue
import threading
import os.path
from os import makedirs
from time import sleep
from random import uniform
from func.log import add_log

urllib3.disable_warnings()

download_count = 0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

class download(threading.Thread):
    def __init__(self,que,path,proxy_address):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        self.que=que
        self.path=path
        if proxy_address != "":
            self.proxy = {
                "http":proxy_address,
                "https":proxy_address,
            }
        else:
            self.proxy = {
                "http":None,
                "https":None,
            }
    def run(self):
        global download_count
        while True:
            if not self.que.empty():
                # sleep(uniform(0.2, 0.5)) # 防止写入日志出错
                if not os.path.exists(self.path): # 验证下载目录是否存在，不存在则创建
                    makedirs(self.path)
                get_img_url = self.que.get() #取出一个图片链接
                file_name = get_img_url.split("/") 
                file_name = unquote(file_name[-1]) # 获取图片名称
                unsupported_file_name = ['/', '\\', ':', '*', '?', '"', '<', '>', '|'] #Windows不支持文件名中包含此列表的字符
                for char in file_name: # 判断图片名称是否包含以上字符，如果包含则替换为空字符
                    if char in unsupported_file_name:
                        file_name = file_name.replace(char, '')
                if os.path.exists(self.path + '/' + file_name): # 根据文件名判断图片是否已经下载，此处存在一个问题：如果文件tags被修改会造成图片重复
                    print(add_log("%s 已存在" % file_name, self.path, 'Warn'))
                    download_count += 1
                    continue
                print(add_log("正在下载 %s" % file_name, self.path, 'Info'))
                res = requests.get(get_img_url, proxies = self.proxy, verify = False) # 下载
                err_count = 0
                while res.status_code != 200 and err_count < 5: # 下载失败且失败次数不大于五次则重新下载
                    err_count += 1
                    print(add_log("%s 下载失败，HTTP错误码： %s ，正在第 %s 次重试" % (file_name, res.status_code, err_count), self.path, 'Warn'))
                    res = requests.get(get_img_url, proxies = self.proxy, headers=headers, verify = False) # 重新下载
                else:
                    if res.status_code != 200:
                        print(add_log("%s 下载失败，HTTP错误码： %s ，超过最大重试次数" % (file_name, res.status_code), self.path, 'Error'))
                        download_count += 1
                        continue
                if res.status_code == 200:
                    print(add_log("%s 下载成功" % file_name, self.path, 'Info'))
                    with open('{}{}{}'.format(self.path, '/', file_name), 'wb') as f: # 写入文件
                        f.write(res.content)
                    download_count += 1
            else:
                return True
 
def start_down(url,num,path,proxy_address): # 下载器接口
    global download_count
    print(add_log("开始本次下载任务", path, 'Info'))
    decoding='utf8'
    link=url
    num=num if num <= len(link) else len(link)
    que=queue.Queue()
    for l in link:
        que.put(l)
    for i in range(num):
        d=download(que,path,proxy_address)
        d.start()
    while True:
        if que.empty() and len(link) <= download_count:
            print(add_log("本次下载任务完成", path, 'Info'))
            download_count = 0
            break
        sleep(1)