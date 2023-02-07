# -*- coding: utf-8 -*-

from func.http import yande_get_list
from func.json import json_decode, json_encode_with_format
from func.download import download, start_download
from func.log import construct, reconstruct, add_log
from func.update import u_check, u_delete, u_mkdir, u_copy, u_download
from func.fileio import file_read, file_write

class service():
    def __init__(self, kwargs):
        self.VERSION = kwargs['VERSION']
        self.AUTHOR = kwargs['AUTHOR']
        self.LAST_REVISE_TIME = kwargs['LAST_REVISE_TIME']

        self.update_path = kwargs['update_path']

        self.mode = kwargs['mode']
        self.start = kwargs['start']
        self.end = kwargs['end']
        self.limit = kwargs['limit']
        self.tags = kwargs['tags']
        self.thread = kwargs['thread']
        self.path = kwargs['path']
        self.proxy = kwargs['proxy']
        self.options = kwargs['options']
        self.file_config_path = kwargs['file_config_path']
        self.retry_max = kwargs['retry_max']

        self.allow_mode_after_process_file = kwargs['allow_mode_after_process_file']
        self.allow_options = kwargs['allow_options']
        self.allow_limit_range = kwargs['allow_limit_range']
        self.null_list = kwargs['null_list']
        self.make_config_str = kwargs['make_config_str']

        self.args_list = kwargs['args_list']

    def log_construct(self):
        construct(self.path)

    def log_reconstruct(self):
        reconstruct(self.path)

    def args_check(self):
        if self.mode == "file":
            if self.make_config_str in self.options:
                self.log_construct()
                self.hello()
                default_config_json = {"args": {}}
                for i in self.args_list:
                    default_config_json['args'].update({i: ""})
                default_config_json = json_encode_with_format(default_config_json)
                file_write(self.file_config_path, default_config_json, mode="w")
                add_log("成功创建默认配置文件到 %s" % self.file_config_path, 'Info')
                self.bye()
                exit()
            else:
                try:
                    file_cfg = json_decode(file_read(self.file_config_path))['args']
                    self.mode = file_cfg['mode'] if 'mode' in file_cfg else "" # mode参数在有误的情况下赋原值会造成错误，因为原值通常都是file
                    self.start = int(file_cfg['start']) if 'start' in file_cfg and file_cfg['start'] not in self.null_list else self.start
                    self.end = int(file_cfg['end']) if 'end' in file_cfg and file_cfg['end'] not in self.null_list else self.end
                    self.limit = int(file_cfg['limit']) if 'limit' in file_cfg and file_cfg['limit'] not in self.null_list else self.limit
                    self.tags = file_cfg['tags'] if 'tags' in file_cfg and file_cfg['tags'] not in self.null_list else self.tags
                    self.thread = int(file_cfg['thread']) if 'thread' in file_cfg and file_cfg['thread'] not in self.null_list else self.thread
                    self.path = file_cfg['path'] if 'path' in file_cfg and file_cfg['path'] not in self.null_list else self.path
                    self.proxy = file_cfg['proxy'] if 'proxy' in file_cfg and file_cfg['proxy'] not in self.null_list else self.proxy
                    self.options = file_cfg['options'] if 'options' in file_cfg and file_cfg['options'] not in self.null_list else self.options
                    self.retry_max = int(file_cfg['retry_max']) if 'retry_max' in file_cfg and file_cfg['retry_max'] not in self.null_list else self.retry_max
                except Exception as e:
                    self.log_construct()
                    raise e
                self.log_construct()

        if self.mode not in self.allow_mode_after_process_file: # 因为之前已经对file模式进行了处理，所以file模式自此处开始不再是可接受的模式
            add_log("指定的模式有误：%s " % self.mode, 'Error')
            exit()
        if self.start == 0: # 避免重复请求和下载
            self.start = 1
        if self.proxy != "":
            self.proxy = {
                "http":self.proxy,
                "https":self.proxy,
            }
        else:
            self.proxy = {
                "http":None,
                "https":None,
            }
        if (self.start > self.end) and (self.end != -1):
            add_log("开始ID： %s 不能大于结束ID： %s" % (self.start, self.end), 'Error')
            exit()
        if self.start < 0:
            add_log("start参数取值不正确，参数不能为负数", 'Error')
            exit()
        if self.limit not in self.allow_limit_range:
            add_log("limit参数取值不正确[1,1000]", 'Error')
            exit()
        self.options = str.split(self.options, '+') # 格式化options
        for i in self.options:
            if i not in self.allow_options:
                add_log("未知的可选参数： %s" % i, 'Error')
                exit()
        if self.retry_max < -1:
            add_log("retry-max参数取值不正确，参数应大于-2", 'Error')
            exit()

    def get_mode(self):
        return self.mode

    def hello(self):
        add_log("欢迎使用 yande.re 图片下载工具 %s" % self.VERSION, 'Info')

    def copyright(self):
        add_log("版本： %s" % self.VERSION, 'Info')
        add_log("作者： %s" % self.AUTHOR, 'Info')
        add_log("最后修改时间： %s" % self.LAST_REVISE_TIME, 'Info')
        add_log("Powered By %s. Some Rights Reserved." % self.AUTHOR, 'Info')
    
    def update(self):
        add_log("正在检测更新", 'Info')
        update_data = u_check(self.VERSION, self.proxy)
        update_data = json_decode(update_data)
        if 'status' in update_data and int(update_data['status']) == 1:
            update_data = update_data['data']
            if self.VERSION != update_data['version']:
                add_log("获取更新信息成功，当前版本： %s ，最新版本： %s" % (self.VERSION, update_data['version']), 'Info')
                confirm_update = input("是否确认更新？（y/n）")
                if confirm_update not in ['', None] and confirm_update[0] in ['y', 'Y']:
                    add_log("开始自动更新", 'Info')
                    tmp_dir = self.update_path + "/" + ".tmp/"
                    add_log("创建临时目录", 'Info')
                    u_mkdir(tmp_dir) # 创建临时文件夹
                    update_data = update_data['op']
                    for i in update_data['add']:
                        add_log("从 %s 下载更新" % i['source'] , 'Info')
                        u_download(i['source'], tmp_dir + i['dir'], i['name'], self.proxy)
                    for i in update_data['del']['dir']:
                        add_log("删除目录 %s" % i, 'Info')
                        u_delete(self.update_path + "/" + i, 'dir')
                    for i in update_data['del']['file']:
                        add_log("删除文件 %s" % i, 'Info')
                        u_delete(self.update_path + "/" + i)
                    add_log("从临时目录复制到 %s" % self.update_path, 'Info')
                    u_copy(tmp_dir, self.update_path)
                    add_log("删除临时目录", 'Info')
                    u_delete(tmp_dir, 'dir')
                else:
                    add_log("用户取消更新", 'Info')
            else:
                add_log("已经是最新版本", 'Info')
        else:
            add_log("获取更新信息失败或暂停更新，请尝试手动更新", 'Warn')

    def page(self):
        add_log("根据页码下载", 'Info')
        if self.end == -1: # 下载到最后一页
            add_log("下载到最后一页，每页 %s 项" % self.limit, 'Info')
            page_count = self.start # 初始化页码计数器
            while True:
                add_log("正在获取第 %s 页" % page_count, 'Info')
                requests = yande_get_list(self.retry_max, page_count, self.limit, self.tags, self.proxy)
                if requests == "[]": # 判断是否已无图片可供下载
                    add_log("已无图片可供下载", 'Warn')
                    break
                requests = json_decode(requests) # json2list
                get_img = []
                for i in requests: # 将图片链接添加到列表
                    if "file_url" in i: 
                        get_img.append({'url':i['file_url'], 'hash':i['md5']})
                start_download(get_img, self.thread, self.path, self.proxy, self.options, self.retry_max) # 传给下载器接口
                page_count += 1 # 页码计数器+1
        elif self.end >= self.start: # 下载部分页码
            add_log("下载部分页码，从第 %s 页下载到第 %s 页，每页 %s 项" % (self.start, self.end, self.limit), 'Info')
            for i in range(self.start, self.end + 1):
                add_log("正在获取第 %s 页" % i, 'Info')
                requests = yande_get_list(self.retry_max, i, self.limit, self.tags, self.proxy)
                if requests == "[]":
                    add_log("已无图片可供下载", 'Warn')
                    break
                requests = json_decode(requests)
                get_img = []
                for i in requests:
                    if "file_url" in i: 
                        get_img.append({'url':i['file_url'], 'hash':i['md5']})
                start_download(get_img, self.thread, self.path, self.proxy, self.options, self.retry_max)
    
    def id(self):
        add_log("根据图片ID下载", 'Info')
        if self.end == -1: # 下载到最新一张图
            add_log("下载到最新一张图", 'Info')
            page_count = 1
            end_point = False # 退出循环标记
            while True:
                if end_point == True: # 当标记为true则退出循环
                    break
                add_log("正在获取第 %s 页" % page_count, 'Info')
                requests = yande_get_list(self.retry_max, page_count, 1000, self.tags, self.proxy)
                if requests == "[]":
                    add_log("已无图片可供下载", 'Warn')
                    break
                requests = json_decode(requests)
                page_start_id = requests[0]['id']
                page_end_id = requests[-1]['id']
                if self.start > page_start_id and page_count == 1: # 判断指定的开始ID是否大于第一页的第一个ID，出现这种错误很显然是ID写错了，例如最新一张图的ID是8000，开始ID写成了80000
                    add_log("指定的开始ID： %s 大于最新ID： %s" % (self.start, page_start_id), 'Error')
                    break
                get_img = []
                for i in requests:
                    if i['id'] >= self.start: # 如果本次迭代的图片ID在设定的范围中则将图片链接添加到列表
                        if "file_url" in i: 
                            get_img.append({'url':i['file_url'], 'hash':i['md5']})
                    else: # 否则结束迭代并标记
                        end_point = True
                        break
                start_download(get_img, self.thread, self.path, self.proxy, self.options, self.retry_max)
                page_count += 1
        elif self.end >= self.start: # 根据图片ID区间下载
            add_log("根据图片ID区间下载，从图片ID： %s 下载到图片ID： %s " % (self.start, self.end), 'Info')
            loop_count = 1
            end_point = False
            while True:
                if end_point == True: # 当标记为true则退出循环
                    break
                echo_comparator = "小于等于" if loop_count == 1 else "小于"
                echo_id = self.end if loop_count == 1 else page_end_id
                add_log("正在获取图片ID%s %s 的图片列表" % (echo_comparator, echo_id), 'Info')
                id_tag = "id:<" + str(self.end + 1) if loop_count == 1 else "id:<" + str(page_end_id)
                requests = yande_get_list(self.retry_max, 1, 1000, id_tag + "+" + self.tags, self.proxy)
                if requests == "[]":
                    add_log("已无图片可供下载", 'Warn')
                    break
                requests = json_decode(requests)
                page_start_id = requests[0]['id'] if requests else 0 # 获取当页第一个ID，如果返回的列表为空则设为0
                page_end_id = requests[-1]['id'] if requests else 0 # 获取当页最后一个ID，如果返回的列表为空则设为0
                if self.start > page_start_id and loop_count == 1: # 判断指定的开始ID是否大于第一页的第一个ID
                    add_log("指定的开始ID： %s 大于可获取到的最新ID： %s" % (self.start, page_start_id), 'Error')
                    break
                if self.start >= page_end_id: # 当开始ID大于等于当页最后一个ID（代表最后一张要下载的图片在当前页）则标记结束循环，进行最后一次遍历
                    end_point = True
                get_img = []
                for i in requests:
                    if i['id'] <= self.end and i['id'] >= self.start: # 如果本次迭代的图片ID在设定的范围中则将图片链接添加到列表
                        if "file_url" in i: 
                            get_img.append({'url':i['file_url'], 'hash':i['md5']})
                    else: # 否则略过
                        pass
                start_download(get_img, self.thread, self.path, self.proxy, self.options, self.retry_max)
                loop_count += 1

    def bye(self):
        add_log("脚本正常退出", 'Info')