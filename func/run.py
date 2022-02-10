# -*- coding: utf-8 -*-
import argparse
from func.log import add_log

def ap():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--mode", required = True, choices = ["id", "page", "update", "copyright"], help = "运行模式，id：通过ID下载 / page：通过页码下载 / update：更新脚本")
    ap.add_argument("-s", "--start", required = False, type = int, default = 1, help = "开始ID")
    ap.add_argument("-e", "--end", required = False, type = int, default = 1, help = "结束ID，-1表示下载到最新一张图/下载到最后一页")
    ap.add_argument("-l", "--limit", required = False, type = int, default = 1000, help = "每页的图片数量，取值范围：1-1000")
    ap.add_argument("-t", "--tags", required = False, default = "", help = "搜索(tagname)/排除(-tagname)指定tags，使用“+”连接多个tag，例：angel+-tagme+tail+-ass")
    ap.add_argument("-T", "--thread", required = False, type = int, default = 5, help = "线程数")
    ap.add_argument("-p", "--path", required = False, default = "./img", help = "文件保存路径")
    ap.add_argument("-P", "--proxy", required = False, default = "", help = "http(s)代理地址，格式：协议://用户名:密码@IP:端口")
    args = vars(ap.parse_args())
    if args['start'] == 0: # 避免重复请求和下载
        args['start'] = 1
    if (args['start'] > args['end']) and (args['end'] != -1):
        print(add_log("开始ID： %s 不能大于结束ID： %s" % (args['start'], args['end']), args['path'], 'Error'))
        exit()
    if args['start'] < 0:
        print(add_log("start参数取值范围不正确", args['path'], 'Error'))
        exit()
    if args['limit'] not in range(1, 1001):
        print(add_log("limit参数取值范围不正确", args['path'], 'Error'))
        exit()
    return args
