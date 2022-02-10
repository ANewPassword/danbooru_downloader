# -*- coding: utf-8 -*-
try:
    from sys import path as getpath
    from func.run import ap
    from func.post import request
    from func.read import read_json
    from func.download import download, start_down
    from func.log import add_log
    from func.update import *

    VERSION = "V1.2.0"
    AUTHOR = "MoCha"
    LAST_REVISE_TIME = "2022-02-10 16:24:17"

    args = ap()
    get_path = getpath[0] + "/"
    # args['path'] = get_path + "/" + args['path']

    print(add_log("欢迎使用 yande.re 图片下载工具 %s" % VERSION, args['path'], 'Info'))

    if args['mode'] == "copyright": # 显示版权信息
        print(add_log("版本： %s" % VERSION, args['path'], 'Info'))
        print(add_log("作者： %s" % AUTHOR, args['path'], 'Info'))
        print(add_log("最后修改时间： %s" % LAST_REVISE_TIME, args['path'], 'Info'))
        print(add_log("Powered By %s. Some Rights Reserved." % AUTHOR, args['path'], 'Info'))

    elif args['mode'] == "update": # 更新脚本
        print(add_log("正在检测更新", args['path'], 'Info'))
        update_data = u_check(VERSION, args['proxy'])
        update_data = read_json(update_data, args['path'])
        if 'status' in update_data and int(update_data['status']) == 1:
            update_data = update_data['data']
            if VERSION != update_data['version']:
                print(add_log("获取更新信息成功，当前版本： %s ，最新版本： %s" % (VERSION, update_data['version']), args['path'], 'Info'))
                confirm_update = input("是否确认更新？（y/n）")
                if confirm_update not in ['', None] and confirm_update[0] in ['y', 'Y']:
                    print(add_log("开始自动更新", args['path'], 'Info'))
                    tmp_dir = get_path + "/" + ".tmp/"
                    print(add_log("创建临时目录", args['path'], 'Info'))
                    u_mkdir(tmp_dir) # 创建临时文件夹
                    update_data = update_data['op']
                    for i in update_data['add']:
                        print(add_log("从 %s 下载更新" % i['source'] , args['path'], 'Info'))
                        u_download(i['source'], tmp_dir + i['dir'], i['name'], args['path'], args['proxy'])
                    for i in update_data['del']['dir']:
                        print(add_log("删除目录 %s" % i, args['path'], 'Info'))
                        u_delete(get_path + "/" + i, 'dir')
                    for i in update_data['del']['file']:
                        print(add_log("删除文件 %s" % i, args['path'], 'Info'))
                        u_delete(get_path + "/" + i)
                    print(add_log("从临时目录复制到 %s" % get_path, args['path'], 'Info'))
                    u_copy(tmp_dir, get_path)
                    print(add_log("删除临时目录", args['path'], 'Info'))
                    u_delete(tmp_dir, 'dir')
                else:
                    print(add_log("用户取消更新", args['path'], 'Info'))
            else:
                print(add_log("已经是最新版本", args['path'], 'Info'))
        else:
            print(add_log("获取更新信息失败或暂停更新，请尝试手动更新", args['path'], 'Warn'))

    elif args['mode'] == "page": # 根据页码下载
        print(add_log("根据页码下载", args['path'], 'Info'))
        if args['end'] == -1: # 下载到最后一页
            print(add_log("下载到最后一页", args['path'], 'Info'))
            page_count = args['start'] # 初始化页码计数器
            while True:
                print(add_log("正在获取第 %s 页" % page_count, args['path'], 'Info'))
                requests = request(page_count, args['limit'], args['tags'], args['proxy'])
                if requests == "[]": # 判断是否已无图片可供下载
                    print(add_log("已无图片可供下载", args['path'], 'Warn'))
                    break
                requests = read_json(requests, args['path']) # json2list
                get_img = []
                for i in requests: # 将图片链接添加到列表
                    if "file_url" in i: 
                        get_img.append(i['file_url'])
                start_down(get_img,args['thread'],args['path'],args['proxy']) # 传给下载器接口
                page_count += 1 # 页码计数器+1
        elif args['end'] >= args['start']: # 下载部分页码
            print(add_log("下载部分页码，从第 %s 页下载到第 %s 页" % (args['start'], args['end']), args['path'], 'Info'))
            for i in range(args['start'], args['end'] + 1):
                print(add_log("正在获取第 %s 页" % i, args['path'], 'Info'))
                requests = request(i, args['limit'], args['tags'], args['proxy'])
                if requests == "[]":
                    print(add_log("已无图片可供下载", args['path'], 'Warn'))
                    break
                requests = read_json(requests, args['path'])
                get_img = []
                for i in requests:
                    if "file_url" in i: 
                        get_img.append(i['file_url'])
                start_down(get_img,args['thread'],args['path'],args['proxy'])

    elif args['mode'] == "id": # 根据图片ID下载
        print(add_log("根据图片ID下载", args['path'], 'Info'))
        if args['end'] == -1: # 下载到最新一张图
            print(add_log("下载到最新一张图", args['path'], 'Info'))
            page_count = 1
            end_point = False # 退出循环标记
            while True:
                if end_point == True: # 当标记为true则退出循环
                    break
                print(add_log("正在获取第 %s 页" % page_count, args['path'], 'Info'))
                requests = request(page_count, 1000, args['tags'], args['proxy'])
                if requests == "[]":
                    print(add_log("已无图片可供下载", args['path'], 'Warn'))
                    break
                requests = read_json(requests, args['path'])
                page_start_id = requests[0]['id']
                page_end_id = requests[-1]['id']
                if args['start'] > page_start_id and page_count == 1: # 判断指定的开始ID是否大于第一页的第一个ID，出现这种错误很显然是ID写错了，例如最新一张图的ID是8000，开始ID写成了80000
                    print(add_log("指定的开始ID： %s 大于最新ID： %s" % (args['start'], page_start_id), args['path'], 'Error'))
                    break
                get_img = []
                for i in requests:
                    if i['id'] >= args['start']: # 如果本次迭代的图片ID在设定的范围中则将图片链接添加到列表
                        if "file_url" in i: 
                            get_img.append(i['file_url'])
                    else: # 否则结束迭代并标记
                        end_point = True
                        break
                start_down(get_img,args['thread'],args['path'],args['proxy'])
                page_count += 1
        elif args['end'] >= args['start']: # 根据图片ID区间下载
            print(add_log("根据图片ID区间下载，从图片ID： %s 下载到图片ID： %s " % (args['start'], args['end']), args['path'], 'Info'))
            loop_count = 1
            end_point = False
            while True:
                if end_point == True: # 当标记为true则退出循环
                    break
                echo_comparator = "小于等于" if loop_count == 1 else "小于"
                echo_id = args['end'] if loop_count == 1 else page_end_id
                print(add_log("正在获取图片ID%s %s 的图片列表" % (echo_comparator, echo_id), args['path'], 'Info'))
                id_tag = "id:<" + str(args['end'] + 1) if loop_count == 1 else "id:<" + str(page_end_id)
                requests = request(1, 1000, id_tag + "+" + args['tags'], args['proxy'])
                if requests == "[]":
                    print(add_log("已无图片可供下载", args['path'], 'Warn'))
                    break
                requests = read_json(requests, args['path'])
                page_start_id = requests[0]['id'] if requests else 0 # 获取当页第一个ID，如果返回的列表为空则设为0
                page_end_id = requests[-1]['id'] if requests else 0 # 获取当页最后一个ID，如果返回的列表为空则设为0
                if args['start'] > page_start_id and loop_count == 1: # 判断指定的开始ID是否大于第一页的第一个ID
                    print(add_log("指定的开始ID： %s 大于最新ID： %s" % (args['start'], args['end'], page_start_id), args['path'], 'Error'))
                    break
                if args['start'] >= page_end_id: # 当开始ID大于等于当页最后一个ID（代表最后一张要下载的图片在当前页）则标记结束循环，进行最后一次遍历
                    end_point = True
                get_img = []
                for i in requests:
                    if i['id'] <= args['end'] and i['id'] >= args['start']: # 如果本次迭代的图片ID在设定的范围中则将图片链接添加到列表
                        if "file_url" in i: 
                            get_img.append(i['file_url'])
                    else: # 否则略过
                        pass
                start_down(get_img,args['thread'],args['path'],args['proxy'])
                loop_count += 1

    print(add_log("脚本运行结束", args['path'], 'Info'))

except Exception as e:
    print(add_log("%s: %s" % (e.__class__.__name__, e), args['path'], 'Error'))
    exit()
except KeyboardInterrupt:
    print(add_log("用户手动退出", args['path'], 'Warn'))