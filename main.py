# -*- coding: utf-8 -*-
try:
    from sys import path as getpath
    from func.run import ap
    from func.service import service
    from func.log import add_log

    VERSION = "V1.2.5"
    AUTHOR = "MoCha"
    LAST_REVISE_TIME = "2022-03-20 16:13:20"

    args = ap()
    get_path = getpath[0] + "/"
    # args['path'] = get_path + "/" + args['path']

    main = service(VERSION, AUTHOR, LAST_REVISE_TIME, get_path, args['mode'], args['start'], args['end'], args['limit'], args['tags'], args['thread'], args['path'], args['proxy'])
    main.hello()

    if args['mode'] == "copyright": # 显示版权信息
        main.copyright()
    elif args['mode'] == "update": # 更新脚本
        main.update()
    elif args['mode'] == "page": # 根据页码下载
        main.page()
    elif args['mode'] == "id": # 根据图片ID下载
        main.id()

    main.bye()

except Exception as e:
    print(add_log("%s: %s" % (e.__class__.__name__, e), args['path'], 'Error'))
    exit()
except KeyboardInterrupt:
    print(add_log("用户手动退出", args['path'], 'Warn'))