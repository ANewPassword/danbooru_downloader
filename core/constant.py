# -*- coding: utf-8 -*-

# 全局常量
VERSION = "V1.5.2"
AUTHOR = "MoCha"
LAST_REVISE_TIME = "2023-02-07 13:42:33"

# 部分参数取值范围
allow_mode = ["id", "page", "file", "update", "copyright"]
allow_mode_after_process_file = ["id", "page", "update", "copyright"]
allow_options = ['', 'chksums', 'make-config']
allow_limit_range = range(1, 1001)

# 常用变量
null_list = ["", None]
unsupported_file_name = ['/', '\\', ':', '*', '?', '"', '<', '>', '|'] # Windows不支持文件名中包含此列表的字符
chksums_str = "chksums"
make_config_str = "make-config"

# 各种默认值
default_start = 1
default_end = 1
default_limit = 1000
default_tags = ""
default_thread = 5
default_path = "./img"
default_proxy = ""
default_options = ""
default_file_config_path = "./config.json"
default_retry_max = 5

# 帮助文本
script_description = "此脚本可通过yande.re公开 API 获取帖子列表以多线程的方式批量下载图片，可选择根据页面ID/图片ID区间下载两种下载模式，另支持自定义设置每页帖子数量、搜索/排除的标签、线程数、文件保存路径、http代理、校验文件完整性等。"

mode_help = "运行模式\r\nid：通过ID下载\r\npage：通过页码下载\r\nfile：使用json格式的配置文件运行，同时需要指定file-config-path\r\nupdate：更新脚本"
start_help = "开始ID"
end_help = "结束ID\r\n-1表示下载到最新一张图/下载到最后一页"
limit_help = "每页的图片数量\r\n取值范围：1-1000"
tags_help = "搜索(tagname)/排除(-tagname)指定标签，使用“+”连接多个标签\r\n例：angel+-tagme+tail+-ass"
thread_help = "线程数"
path_help = "文件保存路径"
proxy_help = "http代理地址\r\n格式：http://用户名:密码@IP:端口"
options_help = "附加操作，使用“+”连接多个参数\r\nchksums：下载后进行文件完整性校验\r\nmake-config：生成一个空白的配置文件，此时file-config-path将视为配置文件生成路径"
file_config_path_help = "配置文件路径，只在运行模式为file时生效"
retry_max_help = "最大网络请求重试次数\r\n-1表示重试直到下载成功"