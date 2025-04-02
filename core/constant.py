# -*- coding: utf-8 -*-

# 全局常量
VERSION = "V2.0.4"
AUTHOR = "MoCha"
LAST_REVISE_TIME = "2025-04-02 16:19:01"

# 部分参数取值范围
allow_mode = ["id", "page", "file", "copyright"]
allow_log_mode = ["Debug", "Info", "Warn", "Error", "None"]
allow_deduplication_mode = ["strict", "sloppy", "none"]

allow_mode_after_process_file = ["id", "page", "copyright"]

# 模板模块 部分模板结构列表和引用策略
allow_template_root = ['mode', 'advanced']
allow_template_mode = ['page', 'id']
allow_template_mode_page = ['api', 'header', 'method', 'data', 'download']
allow_template_mode_page_method = ['GET', 'POST']
allow_template_mode_page_download = ['metadata', 'filename', 'metadata_filename', 'header']
allow_template_mode_id = ['api', 'header', 'method', 'data', 'download', 'op_symbol']
allow_template_mode_id_method = ['GET', 'POST']
allow_template_mode_id_download = ['metadata', 'filename', 'metadata_filename', 'header']
allow_template_mode_id_op_symbol = ['id', 'id_range', 'eq', 'lt', 'gt']
allow_template_advanced = ['positioner', 'constant', 'variable']
template_preset_variables = ['tags', 'page', 'proxy', 'index']
template_delimiter_map = {"preset": "$", "positioner": "#", "constant": "@", "variable": "!"}
template_acl = {
    "mode": {
        "page": {
            "download": {
                "_policy": {
                    "metadata": {
                        "key": {
                            "preset": False,
                            "positioner": False,
                            "constant": False,
                            "variable": False
                        },
                        "value": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        },
                        "sub_key": None,
                        "sub_value": None
                    },
                    "filename": {
                        "key": {
                            "preset": False,
                            "positioner": False,
                            "constant": False,
                            "variable": False
                        },
                        "value": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        },
                        "sub_key": None,
                        "sub_value": None
                    },
                    "metadata_filename": {
                        "key": {
                            "preset": False,
                            "positioner": False,
                            "constant": False,
                            "variable": False
                        },
                        "value": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        },
                        "sub_key": None,
                        "sub_value": None
                    },
                    "header": {
                        "key": None,
                        "value": None,
                        "sub_key": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        },
                        "sub_value": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        }
                    }
                }
            },
            "_policy": {
                "api": {
                    "key": None,
                    "value": {
                        "preset": True,
                        "positioner": False,
                        "constant": True,
                        "variable": True
                    },
                    "sub_key": None,
                    "sub_value": None
                },
                "header": {
                    "key": None,
                    "value": None,
                    "sub_key": {
                        "preset": True,
                        "positioner": False,
                        "constant": True,
                        "variable": True
                        },
                    "sub_value": {
                        "preset": True,
                        "positioner": False,
                        "constant": True,
                        "variable": True
                    }
                },
                "method": {
                    "key": None,
                    "value": None,
                    "sub_key": None,
                    "sub_value": None
                },
                "data":{
                    "key": None,
                    "value": {
                        "preset": True,
                        "positioner": False,
                        "constant": True,
                        "variable": True
                    },
                    "sub_key": None,
                    "sub_value": None
                },
                "download": {
                    "key": None,
                    "value": None,
                    "sub_key": None,
                    "sub_value": None,
                }
            }
        },
        "id": {
            "download": {
                "_policy": {
                    "metadata": {
                        "key": {
                            "preset": False,
                            "positioner": False,
                            "constant": False,
                            "variable": False
                        },
                        "value": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        },
                        "sub_key": None,
                        "sub_value": None
                    },
                    "filename": {
                        "key": {
                            "preset": False,
                            "positioner": False,
                            "constant": False,
                            "variable": False
                        },
                        "value": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        },
                        "sub_key": None,
                        "sub_value": None
                    },
                    "metadata_filename": {
                        "key": {
                            "preset": False,
                            "positioner": False,
                            "constant": False,
                            "variable": False
                        },
                        "value": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        },
                        "sub_key": None,
                        "sub_value": None
                    },
                    "header": {
                        "key": None,
                        "value": None,
                        "sub_key": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        },
                        "sub_value": {
                            "preset": True,
                            "positioner": True,
                            "constant": True,
                            "variable": True
                        }
                    }
                }
            },
            "_policy": {
                "api": {
                    "key": None,
                    "value": {
                        "preset": True,
                        "positioner": False,
                        "constant": True,
                        "variable": True
                    },
                    "sub_key": None,
                    "sub_value": None
                },
                "header": {
                    "key": None,
                    "value": None,
                    "sub_key": {
                        "preset": True,
                        "positioner": False,
                        "constant": True,
                        "variable": True
                        },
                    "sub_value": {
                        "preset": True,
                        "positioner": False,
                        "constant": True,
                        "variable": True
                    }
                },
                "method": {
                    "key": None,
                    "value": None,
                    "sub_key": None,
                    "sub_value": None
                },
                "data":{
                    "key": None,
                    "value": {
                        "preset": True,
                        "positioner": False,
                        "constant": True,
                        "variable": True
                    },
                    "sub_key": None,
                    "sub_value": None
                },
                "download": {
                    "key": None,
                    "value": None,
                    "sub_key": None,
                    "sub_value": None,
                },
                "op_symbol": {
                    "key": None,
                    "value": None,
                    "sub_key": None,
                    "sub_value": None
                }
            }
        },
        "_policy": {
            "page": {
                "key": None,
                "value": None,
                "sub_key": None,
                "sub_value": None
            },
            "id": {
                "key": None,
                "value": None,
                "sub_key": None,
                "sub_value": None
            }
        }
    },
    "advanced": {
        "_policy": {
            "preset": {
                "key": None,
                "value": None,
                "sub_key": None,
                "sub_value": None
            },
            "positioner": {
                "key": None,
                "value": None,
                "sub_key": None,
                "sub_value": {
                    "preset": True,
                    "positioner": True,
                    "constant": True,
                    "variable": True
                }
            },
            "constant": {
                "key": None,
                "value": None,
                "sub_key": None,
                "sub_value": None,
            },
            "variable": {
                "key": None,
                "value": None,
                "sub_key": None,
                "sub_value": {
                    "preset": True,
                    "positioner": True,
                    "constant": True,
                    "variable": True
                }
            }
        }
    },
    "_policy": {
        "mode": {
            "key": None,
            "value": None,
            "sub_key": None,
            "sub_value": None
        },
        "advanced": {
            "key": None,
            "value": None,
            "sub_key": None,
            "sub_value": None
        }
    },
    "_default_global_policy": {
        "key": {
            "preset": False,
            "positioner": False,
            "constant": False,
            "variable": False
        },
        "value": {
            "preset": False,
            "positioner": False,
            "constant": False,
            "variable": False
        },
        "sub_key": {
            "preset": False,
            "positioner": False,
            "constant": False,
            "variable": False
        },
        "sub_value": {
            "preset": False,
            "positioner": False,
            "constant": False,
            "variable": False
        }
    }
}

# 常用变量
null_list = ["", None]
unsupported_file_name = ['/', '\\', ':', '*', '?', '"', '<', '>', '|'] # Windows不支持文件名中包含此列表的字符
template_dirname = "template"

# 各种默认值
default_template = "yandere"
default_start = 1
default_end = 1
default_tags = ""
default_path = "./img"
default_proxy = ""
default_thread = 5
default_file_config_path = "./config.json"
default_retry_max = 5
default_log_level = "Info"
default_deduplication = "strict"
default_chksums = True
default_with_metadata = False
default_make_config = False
default_no_print_log = False

# 帮助文本
script_description = "此脚本可通过 danbooru API 获取图片列表并以多线程的方式批量下载图片、动图和视频，可选择根据页面ID/图片ID区间下载两种下载模式，脚本预设了danbooru/gelbooru/yande.re/konachan/rule34/sankakucomplex等常见的基于danbooru和gelbooru程序搭建的图库的网站爬虫模板，另支持自定义设置下载模板、搜索/排除标签、线程数、自定义保存路径、http代理、下载查重、校验文件完整性、保存元数据等强大功能。"

mode_help = "运行模式\r\n取值范围：\r\nid：通过ID下载\r\npage：通过页码下载\r\nfile：使用json格式的配置文件运行，同时需要指定file-config-path\r\ncopyright：输出版权信息"
template_help = "运行模板"
start_help = "起始ID"
end_help = "结束ID\r\n-1表示下载到最新一张图/下载到最后一页"
tags_help = "搜索(tagname)/排除(-tagname)指定标签，使用“+”连接多个标签\r\n例：angel+-tagme+tail+-ass"
path_help = "文件保存路径"
proxy_help = "http代理地址\r\n格式：http://用户名:密码@IP:端口"
thread_help = "线程数"
file_config_path_help = "配置文件路径，只在运行模式为file时生效"
retry_max_help = "最大网络请求重试次数\r\n-1表示重试直到下载成功"
log_level_help = "更改日志记录等级\r\n取值范围：['Debug', 'Info', 'Warn', 'Error', 'None']\r\n日志等级依次升高，信息量依次减少"
deduplication_help = "去重模式\r\n取值范围：\r\nstrict：严格模式，通过ID+MD5验证\r\nsloppy：宽松模式，通过ID验证\r\nnone：不验证"
chksums_help = "下载后进行文件完整性校验（标志性参数）"
with_metadata_help = "保存每个图片的元数据（标志性参数）"
make_config_help = "生成一个空白的配置文件，此时file-config-path将视为配置文件生成路径（标志性参数）"
no_print_log_help = "不打印日志到标准输出流（标志性参数）"