# -*- coding: utf-8 -*-
import os.path
from os import makedirs
from time import localtime, strftime

def add_log(text,path,type=None):
    datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    date = strftime("%Y%m%d", localtime())
    log_file_path = "%s/logs/%s/" % (path, date)
    # log_file_name = "success.log" if type != "Error" else "error.log"
    log_file_name = "log.log"
    log_content = "%s|%s|%s" % (datetime, type, text)
    if not os.path.exists(log_file_path): # 验证下载目录是否存在，不存在则创建
        makedirs(log_file_path)
    with open(log_file_path + log_file_name, 'a', encoding='utf8') as l:
        l.write(log_content + "\n")
    if type == "Error": # 如果日志类型为Error就再向error.log写一份
        log_file_name = "error.log"
        with open(log_file_path + log_file_name, 'a', encoding='utf8') as l:
            l.write(log_content + "\n")
    return log_content