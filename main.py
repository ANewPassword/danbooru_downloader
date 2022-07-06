# -*- coding: utf-8 -*-
try:
    from sys import path as getpath
    from core.constant import *
    from core.service import service
    from func.args import ap
    from func.log import add_log

    args = ap()
    get_path = getpath[0] + "/"
    # args['path'] = get_path + "/" + args['path']

    args_dict = {
        "VERSION": VERSION,
        "AUTHOR": AUTHOR,
        "LAST_REVISE_TIME": LAST_REVISE_TIME,
        "allow_mode_after_process_file": allow_mode_after_process_file,
        "allow_options": allow_options,
        "allow_limit_range": allow_limit_range,
        "null_list": null_list,
        "make_config_str": make_config_str, 
        "update_path": get_path,
        "mode": args['mode'],
        "start": args['start'],
        "end": args['end'],
        "limit": args['limit'],
        "tags": args['tags'],
        "thread": args['thread'],
        "path": args['path'],
        "proxy": args['proxy'],
        "options": args['options'],
        "file_config_path": args['file_config_path'],
        "retry_max": args['retry_max'],
        "args_list": list(args.keys())
    }

    main = service(args_dict)

    if args['mode'] != "file": # file模式下仍先行初始化日志模块会导致创建一个多余的文件
        main.log_construct()
    main.args_check() # 参数检查
    main.hello()

    if args['mode'] == "file": # 在参数检查时已经处理了配置文件，此处获取真正的运行模式
        args['mode'] = main.get_mode()

    if args['mode'] == "copyright": # 显示版权信息
        main.copyright()
    elif args['mode'] == "update": # 更新脚本
        main.update()
    elif args['mode'] == "page": # 根据页码下载
        main.page()
    elif args['mode'] == "id": # 根据图片ID下载
        main.id()
    elif args['mode'] == "!exit": # 程序保留的退出标记
        pass
    else:
        add_log("指定的模式有误：%s " % args['mode'], 'Error')
        exit()

    main.bye()

except Exception as e:
    add_log("%s: %s" % (e.__class__.__name__, e), 'Error')
    exit()
except KeyboardInterrupt:
    add_log("用户手动退出", 'Warn')