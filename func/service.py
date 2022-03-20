# -*- coding: utf-8 -*-
from func.post import request
from func.read import read_json
from func.download import download, start_down
from func.log import add_log
from func.update import *

class service():
    def __init__(self, VERSION, AUTHOR, LAST_REVISE_TIME, update_path, mode = None, start = None, end = None, limit = None, tags = None, thread = None, path = None, proxy = None):
        self.VERSION = VERSION
        self.AUTHOR = AUTHOR
        self.LAST_REVISE_TIME = LAST_REVISE_TIME
        self.update_path = update_path
        self.mode = mode
        self.start = start
        self.end = end
        self.limit = limit
        self.tags = tags
        self.thread = thread
        self.path = path
        self.proxy = proxy

    def hello(self):
        print(add_log("欢迎使用 yande.re 图片下载工具 %s" % self.VERSION, self.path, 'Info'))

    def copyright(self):
        print(add_log("版本： %s" % self.VERSION, self.path, 'Info'))
        print(add_log("作者： %s" % self.AUTHOR, self.path, 'Info'))
        print(add_log("最后修改时间： %s" % self.LAST_REVISE_TIME, self.path, 'Info'))
        print(add_log("Powered By %s. Some Rights Reserved." % self.AUTHOR, self.path, 'Info'))
    
    def update(self):
        print(add_log("正在检测更新", self.path, 'Info'))
        update_data = u_check(self.VERSION, self.proxy)
        update_data = read_json(update_data, self.path)
        if 'status' in update_data and int(update_data['status']) == 1:
            update_data = update_data['data']
            if self.VERSION != update_data['version']:
                print(add_log("获取更新信息成功，当前版本： %s ，最新版本： %s" % (self.VERSION, update_data['version']), self.path, 'Info'))
                confirm_update = input("是否确认更新？（y/n）")
                if confirm_update not in ['', None] and confirm_update[0] in ['y', 'Y']:
                    print(add_log("开始自动更新", self.path, 'Info'))
                    tmp_dir = self.update_path + "/" + ".tmp/"
                    print(add_log("创建临时目录", self.path, 'Info'))
                    u_mkdir(tmp_dir) # 创建临时文件夹
                    update_data = update_data['op']
                    for i in update_data['add']:
                        print(add_log("从 %s 下载更新" % i['source'] , self.path, 'Info'))
                        u_download(i['source'], tmp_dir + i['dir'], i['name'], self.path, self.proxy)
                    for i in update_data['del']['dir']:
                        print(add_log("删除目录 %s" % i, self.path, 'Info'))
                        u_delete(self.update_path + "/" + i, 'dir')
                    for i in update_data['del']['file']:
                        print(add_log("删除文件 %s" % i, self.path, 'Info'))
                        u_delete(self.update_path + "/" + i)
                    print(add_log("从临时目录复制到 %s" % self.update_path, self.path, 'Info'))
                    u_copy(tmp_dir, self.update_path)
                    print(add_log("删除临时目录", self.path, 'Info'))
                    u_delete(tmp_dir, 'dir')
                else:
                    print(add_log("用户取消更新", self.path, 'Info'))
            else:
                print(add_log("已经是最新版本", self.path, 'Info'))
        else:
            print(add_log("获取更新信息失败或暂停更新，请尝试手动更新", self.path, 'Warn'))

    def page(self):
        print(add_log("根据页码下载", self.path, 'Info'))
        if self.end == -1: # 下载到最后一页
            print(add_log("下载到最后一页", self.path, 'Info'))
            page_count = self.start # 初始化页码计数器
            while True:
                print(add_log("正在获取第 %s 页" % page_count, self.path, 'Info'))
                requests = request(page_count, self.limit, self.tags, self.proxy)
                if requests == "[]": # 判断是否已无图片可供下载
                    print(add_log("已无图片可供下载", self.path, 'Warn'))
                    break
                requests = read_json(requests, self.path) # json2list
                get_img = []
                for i in requests: # 将图片链接添加到列表
                    if "file_url" in i: 
                        get_img.append(i['file_url'])
                start_down(get_img,self.thread,self.path,self.proxy) # 传给下载器接口
                page_count += 1 # 页码计数器+1
        elif self.end >= self.start: # 下载部分页码
            print(add_log("下载部分页码，从第 %s 页下载到第 %s 页" % (self.start, self.end), self.path, 'Info'))
            for i in range(self.start, self.end + 1):
                print(add_log("正在获取第 %s 页" % i, self.path, 'Info'))
                requests = request(i, self.limit, self.tags, self.proxy)
                if requests == "[]":
                    print(add_log("已无图片可供下载", self.path, 'Warn'))
                    break
                requests = read_json(requests, self.path)
                get_img = []
                for i in requests:
                    if "file_url" in i: 
                        get_img.append(i['file_url'])
                start_down(get_img,self.thread,self.path,self.proxy)
    
    def id(self):
        print(add_log("根据图片ID下载", self.path, 'Info'))
        if self.end == -1: # 下载到最新一张图
            print(add_log("下载到最新一张图", self.path, 'Info'))
            page_count = 1
            end_point = False # 退出循环标记
            while True:
                if end_point == True: # 当标记为true则退出循环
                    break
                print(add_log("正在获取第 %s 页" % page_count, self.path, 'Info'))
                requests = request(page_count, 1000, self.tags, self.proxy)
                if requests == "[]":
                    print(add_log("已无图片可供下载", self.path, 'Warn'))
                    break
                requests = read_json(requests, self.path)
                page_start_id = requests[0]['id']
                page_end_id = requests[-1]['id']
                if self.start > page_start_id and page_count == 1: # 判断指定的开始ID是否大于第一页的第一个ID，出现这种错误很显然是ID写错了，例如最新一张图的ID是8000，开始ID写成了80000
                    print(add_log("指定的开始ID： %s 大于最新ID： %s" % (self.start, page_start_id), self.path, 'Error'))
                    break
                get_img = []
                for i in requests:
                    if i['id'] >= self.start: # 如果本次迭代的图片ID在设定的范围中则将图片链接添加到列表
                        if "file_url" in i: 
                            get_img.append(i['file_url'])
                    else: # 否则结束迭代并标记
                        end_point = True
                        break
                start_down(get_img,self.thread,self.path,self.proxy)
                page_count += 1
        elif self.end >= self.start: # 根据图片ID区间下载
            print(add_log("根据图片ID区间下载，从图片ID： %s 下载到图片ID： %s " % (self.start, self.end), self.path, 'Info'))
            loop_count = 1
            end_point = False
            while True:
                if end_point == True: # 当标记为true则退出循环
                    break
                echo_comparator = "小于等于" if loop_count == 1 else "小于"
                echo_id = self.end if loop_count == 1 else page_end_id
                print(add_log("正在获取图片ID%s %s 的图片列表" % (echo_comparator, echo_id), self.path, 'Info'))
                id_tag = "id:<" + str(self.end + 1) if loop_count == 1 else "id:<" + str(page_end_id)
                requests = request(1, 1000, id_tag + "+" + self.tags, self.proxy)
                if requests == "[]":
                    print(add_log("已无图片可供下载", self.path, 'Warn'))
                    break
                requests = read_json(requests, self.path)
                page_start_id = requests[0]['id'] if requests else 0 # 获取当页第一个ID，如果返回的列表为空则设为0
                page_end_id = requests[-1]['id'] if requests else 0 # 获取当页最后一个ID，如果返回的列表为空则设为0
                if self.start > page_start_id and loop_count == 1: # 判断指定的开始ID是否大于第一页的第一个ID
                    print(add_log("指定的开始ID： %s 大于最新ID： %s" % (self.start, self.end, page_start_id), self.path, 'Error'))
                    break
                if self.start >= page_end_id: # 当开始ID大于等于当页最后一个ID（代表最后一张要下载的图片在当前页）则标记结束循环，进行最后一次遍历
                    end_point = True
                get_img = []
                for i in requests:
                    if i['id'] <= self.end and i['id'] >= self.start: # 如果本次迭代的图片ID在设定的范围中则将图片链接添加到列表
                        if "file_url" in i: 
                            get_img.append(i['file_url'])
                    else: # 否则略过
                        pass
                start_down(get_img,self.thread,self.path,self.proxy)
                loop_count += 1

    def bye(self):
        print(add_log("脚本运行结束", self.path, 'Info'))