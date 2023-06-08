# -*- coding: utf-8 -*-

try:
    from sys import path as getpath
    from core.constant import *
    from core.service import Service
    from func.args import ap
    from func.log import add_log
    from func.debug import debug_info

    args = ap()
    get_path = getpath[0] + "/"
    # args['path'] = get_path + "/" + args['path']

    args_dict = {
        "VERSION": VERSION,
        "AUTHOR": AUTHOR,
        "LAST_REVISE_TIME": LAST_REVISE_TIME,
        "program_path": get_path,
        "mode": args['mode'],
        "template": args['template'],
        "start": args['start'],
        "end": args['end'],
        "tags": args['tags'],
        "path": args['path'],
        "proxy": args['proxy'],
        "thread": args['thread'],
        "file_config_path": args['file_config_path'],
        "retry_max": args['retry_max'],
        "log_level": args['log_level'],
        "deduplication": args['deduplication'],
        "chksums": args['chksums'],
        "with_metadata": args['with_metadata'],
        "make_config": args['make_config'],
        "no_print_log": args['no_print_log'],
        "allow_mode_after_process_file": allow_mode_after_process_file,
        "allow_template_root": allow_template_root,
        "allow_template_mode": allow_template_mode,
        "allow_template_mode_page": allow_template_mode_page,
        "allow_template_mode_page_method": allow_template_mode_page_method,
        "allow_template_mode_page_download": allow_template_mode_page_download,
        "allow_template_mode_id": allow_template_mode_id,
        "allow_template_mode_id_method": allow_template_mode_id_method,
        "allow_template_mode_id_download": allow_template_mode_id_download,
        "allow_template_mode_id_op_symbol": allow_template_mode_id_op_symbol,
        "allow_template_advanced": allow_template_advanced,
        "template_preset_variables": template_preset_variables,
        "template_delimiter_map": template_delimiter_map,
        "template_acl": template_acl,
        "null_list": null_list,
        "unsupported_file_name": unsupported_file_name,
        "template_dirname": template_dirname,
        "args_list": list(args.keys())
    }

    main = Service(args_dict)

    if args['mode'] != "file": # file模式下仍先行初始化日志模块会导致创建一个多余的文件
        main.log_construct()
        add_log("日志模块初始化完成，开始记录日志", 'Debug', debug_info())
    main.args_check() # 参数检查
    main.template_check() # 模板检查
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
    elif args['mode'] == "_exit": # 保留的退出标记
        pass
    else:
        add_log("指定的模式有误：%s " % args['mode'], 'Error', debug_info())
        exit()

    main.bye()

except Exception as e:
    add_log("%s: %s" % (e.__class__.__name__, e), 'Error', debug_info())
    add_log("请检查上方堆栈跟踪信息，此跟踪信息不会写入到日志", 'Error', debug_info(True))
    exit()
except KeyboardInterrupt:
    add_log("用户手动退出", 'Warn', debug_info())