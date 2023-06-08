# -*- coding: utf-8 -*-

from copy import deepcopy
from func.http import simple_http_api_request
from func.json import json_decode, json_encode, json_encode_with_format
from func.download import start_download
from func.log import construct, reconstruct, add_log
from func.update import u_check, u_delete, u_mkdir, u_copy, u_download
from func.fileio import file_read, file_write, file_splitext, dir_list
from func.template import list_template_string_include, check_template_variable_name, detect_template_include_loop, TemplateReader
from func.dict import traverse_dict, get_dict_value_by_position_list, deep_update
from func.debug import debug_info

class Service:
    def __init__(self, kwargs):
        self.VERSION = kwargs['VERSION']
        self.AUTHOR = kwargs['AUTHOR']
        self.LAST_REVISE_TIME = kwargs['LAST_REVISE_TIME']

        self.program_path = kwargs['program_path']

        self.mode = kwargs['mode']
        self.template = kwargs['template']
        self.start = kwargs['start']
        self.end = kwargs['end']
        self.tags = kwargs['tags']
        self.path = kwargs['path']
        self.proxy = kwargs['proxy']
        self.thread = kwargs['thread']
        self.file_config_path = kwargs['file_config_path']
        self.retry_max = kwargs['retry_max']
        self.log_level = kwargs['log_level']
        self.deduplication = kwargs['deduplication']
        self.chksums = kwargs['chksums']
        self.with_metadata = kwargs['with_metadata']
        self.make_config = kwargs['make_config']
        self.no_print_log = kwargs['no_print_log']

        self.allow_mode_after_process_file = kwargs['allow_mode_after_process_file']

        self.allow_template_root = kwargs['allow_template_root']
        self.allow_template_mode = kwargs['allow_template_mode']
        self.allow_template_mode_page = kwargs['allow_template_mode_page']
        self.allow_template_mode_page_method = kwargs['allow_template_mode_page_method']
        self.allow_template_mode_page_download = kwargs['allow_template_mode_page_download']
        self.allow_template_mode_id = kwargs['allow_template_mode_id']
        self.allow_template_mode_id_method = kwargs['allow_template_mode_id_method']
        self.allow_template_mode_id_download = kwargs['allow_template_mode_id_download']
        self.allow_template_mode_id_op_symbol = kwargs['allow_template_mode_id_op_symbol']
        self.allow_template_advanced = kwargs['allow_template_advanced']
        self.template_preset_variables = kwargs['template_preset_variables']
        self.template_delimiter_map = kwargs['template_delimiter_map']
        self.template_acl = kwargs['template_acl']

        self.null_list = kwargs['null_list']
        self.unsupported_file_name = kwargs['unsupported_file_name']
        self.template_dirname = kwargs['template_dirname']

        self.args_list = kwargs['args_list']

    def log_construct(self):
        construct(self.path, self.log_level, self.no_print_log)

    def log_reconstruct(self):
        reconstruct(self.path, self.log_level, self.no_print_log)

    def args_check(self):
        if self.mode == "file":
            if self.make_config:
                self.log_construct()
                add_log("日志模块初始化完成，开始记录日志", 'Debug', debug_info())
                self.hello()
                default_config_json = {"args": {}}
                for i in self.args_list:
                    default_config_json['args'].update({i: ""})
                default_config_json = json_encode_with_format(default_config_json)
                file_write(self.file_config_path, default_config_json, mode="w")
                add_log("成功创建空白配置文件到 %s" % self.file_config_path, 'Info', debug_info())
                self.bye()
                exit()
            else:
                try:
                    file_cfg = json_decode(file_read(self.file_config_path))['args']
                    self.mode = file_cfg['mode'] if 'mode' in file_cfg else "" # mode参数在有误的情况下赋原值会造成错误，因为原值通常仍然是file
                    self.template = file_cfg['template'] if 'template' in file_cfg and file_cfg['template'] not in self.null_list else self.template
                    self.start = int(file_cfg['start']) if 'start' in file_cfg and file_cfg['start'] not in self.null_list else self.start
                    self.end = int(file_cfg['end']) if 'end' in file_cfg and file_cfg['end'] not in self.null_list else self.end
                    self.tags = file_cfg['tags'] if 'tags' in file_cfg and file_cfg['tags'] not in self.null_list else self.tags
                    self.path = file_cfg['path'] if 'path' in file_cfg and file_cfg['path'] not in self.null_list else self.path
                    self.proxy = file_cfg['proxy'] if 'proxy' in file_cfg and file_cfg['proxy'] not in self.null_list else self.proxy
                    self.thread = int(file_cfg['thread']) if 'thread' in file_cfg and file_cfg['thread'] not in self.null_list else self.thread
                    self.retry_max = int(file_cfg['retry_max']) if 'retry_max' in file_cfg and file_cfg['retry_max'] not in self.null_list else self.retry_max
                    self.log_level = file_cfg['log_level'] if 'log_level' in file_cfg and file_cfg['log_level'] not in self.null_list else self.log_level
                    self.deduplication = file_cfg['deduplication'] if 'deduplication' in file_cfg and file_cfg['deduplication'] not in self.null_list else self.deduplication
                    self.chksums = bool(file_cfg['chksums']) if 'chksums' in file_cfg and file_cfg['chksums'] not in self.null_list else self.chksums
                    self.with_metadata = bool(file_cfg['with_metadata']) if 'with_metadata' in file_cfg and file_cfg['with_metadata'] not in self.null_list else self.with_metadata
                    self.make_config = bool(file_cfg['make_config']) if 'make_config' in file_cfg and file_cfg['make_config'] not in self.null_list else self.make_config
                    self.no_print_log = bool(file_cfg['no_print_log']) if 'no_print_log' in file_cfg and file_cfg['no_print_log'] not in self.null_list else self.no_print_log
                except Exception as e:
                    self.log_construct()
                    add_log("日志模块初始化完成，开始记录日志", 'Debug', debug_info())
                    raise e
                self.log_construct()
                add_log("日志模块初始化完成，开始记录日志", 'Debug', debug_info())

        add_log("运行参数： %s" % json_encode(self.__dict__), 'Debug', debug_info())
        add_log("开始运行参数预检查", 'Debug', debug_info())
        add_log("检查运行模式设置", 'Debug', debug_info())
        if self.mode not in self.allow_mode_after_process_file: # 因为之前已经对file模式进行了处理，所以file模式自此处开始不再是可接受的模式
            add_log("指定的模式有误： %s " % self.mode, 'Error', debug_info())
            exit()
        add_log("检查运行模板设置", 'Debug', debug_info())
        add_log("获取可用模板", 'Debug', debug_info())
        template_list = self.get_available_template()
        add_log("可用模板： %s" % json_encode(template_list), 'Debug', debug_info())
        if self.template not in template_list:
            add_log("指定的模板有误： %s ，模板不在可用模板列表中" % self.template, 'Error', debug_info())
            exit()
        add_log("检查下载范围设置", 'Debug', debug_info())
        if self.start == 0: # 避免重复请求和下载
            self.start = 1
            add_log("start参数有误，为避免重复请求和下载，已修正为 1", 'Warn', debug_info())
        if (self.start > self.end) and (self.end != -1):
            add_log("开始ID： %s 不能大于结束ID： %s" % (self.start, self.end), 'Error', debug_info())
            exit()
        if self.start < 0:
            add_log("start参数取值不正确，参数取值范围为非负整数", 'Error', debug_info(), debug_info())
            exit()
        add_log("格式化代理设置", 'Debug', debug_info())
        if self.proxy != "":
            self.proxy = {
                "http": self.proxy,
                "https": self.proxy,
            }
        else:
            self.proxy = {
                "http": None,
                "https": None,
            }
        add_log("代理设置： %s" % json_encode(self.proxy), 'Debug', debug_info())
        add_log("检查最大网络请求重试次数设置", 'Debug', debug_info())
        if self.retry_max < -1:
            add_log("retry-max 参数取值不正确，参数取值范围为整数且大于等于 -1", 'Error', debug_info())
            exit()
        add_log("运行参数预检查通过", 'Debug', debug_info())

    def template_check(self):
        add_log("将 %s 与基础模板合并" % self.template, 'Debug', debug_info())
        self.template_cfg = deep_update(json_decode(file_read(self.program_path + self.template_dirname + "/" + "_base" + ".json")), json_decode(file_read(self.program_path + self.template_dirname + "/" + self.template + ".json")))
        add_log("模板参数： %s" % json_encode(self.template_cfg), 'Debug', debug_info())
        add_log("开始模板预检查", 'Debug', debug_info())
        add_log("检查模板结构", 'Debug', debug_info())
        if list(self.template_cfg.keys()) != self.allow_template_root:
            add_log("模板 %s 节点结构有误，当前为： %s ，应该为： %s" % ('_root', json_encode(list(self.template_cfg.keys())), json_encode(self.allow_template_root)), 'Error', debug_info())
            exit()
        elif list(self.template_cfg['mode'].keys()) != self.allow_template_mode:
            add_log("模板 %s 节点结构有误，当前为： %s ，应该为： %s" % ('mode', json_encode(list(self.template_cfg['mode'].keys())), json_encode(self.allow_template_mode)), 'Error', debug_info())
            exit()
        # page
        elif list(self.template_cfg['mode']['page'].keys()) != self.allow_template_mode_page:
            add_log("模板 %s 节点结构有误，当前为： %s ，应该为： %s" % ('mode.page', json_encode(list(self.template_cfg['mode']['page'].keys())), json_encode(self.allow_template_mode_page)), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['page']['api']) != str or self.template_cfg['mode']['page']['api'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.page.api', type(self.template_cfg['mode']['page']['api']), str), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['page']['header']) != dict:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('mode.page.header', type(self.template_cfg['mode']['page']['header']), dict), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['page']['method']) != str or self.template_cfg['mode']['page']['method'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.page.method', type(self.template_cfg['mode']['page']['method']), str), 'Error', debug_info())
            exit()
        elif self.template_cfg['mode']['page']['method'] not in self.allow_template_mode_page_method:
            add_log("模板 %s 节点取值有误，当前为： %s ，取值范围为： %s" % ('mode.page.method', self.template_cfg['mode']['page']['method'], json_encode(self.allow_template_mode_page_method)), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['page']['data']) != str and self.template_cfg['mode']['page']['data'] != None:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s 或 %s" % ('mode.page.data', type(self.template_cfg['mode']['page']['data']), str, None), 'Error', debug_info())
            exit()
        elif list(self.template_cfg['mode']['page']['download'].keys()) != self.allow_template_mode_page_download:
            add_log("模板 %s 节点结构有误，当前为： %s ，应该为： %s" % ('mode.page.download', json_encode(list(self.template_cfg['mode']['page']['download'].keys())), json_encode(self.allow_template_mode_page_download)), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['page']['download']['metadata']) != str:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('mode.page.download.metadata', type(self.template_cfg['mode']['page']['download']['metadata']), str), 'Error', debug_info())
            exit()
        elif self.template_cfg['mode']['page']['download']['metadata'] in self.null_list and self.with_metadata:
            add_log("当记录元数据时，模板 %s 节点不能为空" % ('mode.page.download.metadata'), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['page']['download']['filename']) != str or self.template_cfg['mode']['page']['download']['filename'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.page.download.filename', type(self.template_cfg['mode']['page']['download']['filename']), str), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['page']['download']['metadata_filename']) != str:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('mode.page.download.metadata_filename', type(self.template_cfg['mode']['page']['download']['metadata_filename']), str), 'Error', debug_info())
            exit()
        elif self.template_cfg['mode']['page']['download']['metadata_filename'] in self.null_list and self.with_metadata:
            add_log("当记录元数据时，模板 %s 节点不能为空" % ('mode.page.download.metadata_filename'), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['page']['download']['header']) != dict:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('mode.page.download.header', type(self.template_cfg['mode']['page']['download']['header']), dict), 'Error', debug_info())
            exit()
        # id
        elif list(self.template_cfg['mode']['id'].keys()) != self.allow_template_mode_id:
            add_log("模板 %s 节点结构有误，当前为： %s ，应该为： %s" % ('mode.id', json_encode(list(self.template_cfg['mode']['id'].keys())), json_encode(self.allow_template_mode_id)), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['api']) != str or self.template_cfg['mode']['id']['api'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.id.api', type(self.template_cfg['mode']['id']['api']), str), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['header']) != dict:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('mode.id.header', type(self.template_cfg['mode']['id']['header']), dict), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['method']) != str or self.template_cfg['mode']['id']['method'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.id.method', type(self.template_cfg['mode']['id']['method']), str), 'Error', debug_info())
            exit()
        elif self.template_cfg['mode']['id']['method'] not in self.allow_template_mode_id_method:
            add_log("模板 %s 节点取值有误，当前为： %s ，取值范围为： %s" % ('mode.id.method', self.template_cfg['mode']['id']['method'], json_encode(self.allow_template_mode_id_method)), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['data']) != str and self.template_cfg['mode']['page']['data'] != None:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s 或 %s" % ('mode.id.data', type(self.template_cfg['mode']['id']['data']), str, None), 'Error', debug_info())
            exit()
        elif list(self.template_cfg['mode']['id']['download'].keys()) != self.allow_template_mode_id_download:
            add_log("模板 %s 节点结构有误，当前为： %s ，应该为： %s" % ('mode.id.download', json_encode(list(self.template_cfg['mode']['id']['download'].keys())), json_encode(self.allow_template_mode_id_download)), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['download']['metadata']) != str:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('mode.id.download.metadata', type(self.template_cfg['mode']['id']['download']['metadata']), str), 'Error', debug_info())
            exit()
        elif self.template_cfg['mode']['id']['download']['metadata'] in self.null_list and self.with_metadata:
            add_log("当记录元数据时，模板 %s 节点不能为空" % ('mode.id.download.metadata'), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['download']['filename']) != str  or self.template_cfg['mode']['id']['download']['filename'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.id.download.filename', type(self.template_cfg['mode']['id']['download']['filename']), str), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['download']['metadata_filename']) != str:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('mode.id.download.metadata_filename', type(self.template_cfg['mode']['id']['download']['metadata_filename']), str), 'Error', debug_info())
            exit()
        elif self.template_cfg['mode']['id']['download']['metadata_filename'] in self.null_list and self.with_metadata:
            add_log("当记录元数据时，模板 %s 节点不能为空" % ('mode.id.download.metadata_filename'), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['download']['header']) != dict:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('mode.id.download.header', type(self.template_cfg['mode']['id']['download']['header']), dict), 'Error', debug_info())
            exit()
        elif list(self.template_cfg['mode']['id']['op_symbol'].keys()) != self.allow_template_mode_id_op_symbol:
            add_log("模板 %s 节点结构有误，当前为： %s ，应该为： %s" % ('mode.id.op_symbol', json_encode(list(self.template_cfg['mode']['id']['op_symbol'].keys())), json_encode(self.allow_template_mode_id_op_symbol)), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['op_symbol']['id']) != str or self.template_cfg['mode']['id']['op_symbol']['id'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.id.op_symbol.id', type(self.template_cfg['mode']['id']['op_symbol']['id']), str), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['op_symbol']['id_range']) != str or self.template_cfg['mode']['id']['op_symbol']['id_range'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.id.op_symbol.id_range', type(self.template_cfg['mode']['id']['op_symbol']['id_range']), str), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['op_symbol']['eq']) != str or self.template_cfg['mode']['id']['op_symbol']['eq'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.id.op_symbol.eq', type(self.template_cfg['mode']['id']['op_symbol']['eq']), str), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['op_symbol']['lt']) != str or self.template_cfg['mode']['id']['op_symbol']['lt'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.id.op_symbol.lt', type(self.template_cfg['mode']['id']['op_symbol']['lt']), str), 'Error', debug_info())
            exit()
        elif type(self.template_cfg['mode']['id']['op_symbol']['gt']) != str or self.template_cfg['mode']['id']['op_symbol']['gt'] in self.null_list:
            add_log("模板 %s 节点数据类型有误或为空，当前类型为： %s ，应该为： %s" % ('mode.id.op_symbol.gt', type(self.template_cfg['mode']['id']['op_symbol']['gt']), str), 'Error', debug_info())
            exit()
        elif list(self.template_cfg['advanced'].keys()) != self.allow_template_advanced:
            add_log("模板 %s 节点结构有误，当前为： %s ，应该为： %s" % ('advanced', json_encode(list(self.template_cfg['advanced'].keys())), json_encode(self.allow_template_advanced)), 'Error', debug_info())
            exit()
        # positioner
        elif type(self.template_cfg['advanced']['positioner']) != dict:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('advanced.positioner', type(self.template_cfg['advanced']['positioner']), dict), 'Error', debug_info())
            exit()
        elif '#root' not in self.template_cfg['advanced']['positioner'] or type(self.template_cfg['advanced']['positioner']['#root']) != str:
            add_log("模板 %s 节点中不包含必要的参数 %s ，也可能是 %s 的数据类型有误，类型应该为： %s" % ('advanced.positioner', '#root','advanced.positioner.#root', str), 'Error', debug_info())
            exit()
        elif '#id' not in self.template_cfg['advanced']['positioner'] or type(self.template_cfg['advanced']['positioner']['#id']) != str or self.template_cfg['advanced']['positioner']['#id'] in self.null_list:
            add_log("模板 %s 节点中不包含必要的参数 %s ，也可能是 %s 的数据类型有误或为空，类型应该为： %s" % ('advanced.positioner', '#id','advanced.positioner.#id', str), 'Error', debug_info())
            exit()
        elif '#md5' not in self.template_cfg['advanced']['positioner'] or type(self.template_cfg['advanced']['positioner']['#md5']) != str or self.template_cfg['advanced']['positioner']['#md5'] in self.null_list:
            add_log("模板 %s 节点中不包含必要的参数 %s ，也可能是 %s 的数据类型有误或为空，类型应该为： %s" % ('advanced.positioner', '#md5','advanced.positioner.#md5', str), 'Error', debug_info())
            exit()
        elif '#file_url' not in self.template_cfg['advanced']['positioner'] or type(self.template_cfg['advanced']['positioner']['#file_url']) != str or self.template_cfg['advanced']['positioner']['#file_url'] in self.null_list:
            add_log("模板 %s 节点中不包含必要的参数 %s ，也可能是 %s 的数据类型有误或为空，类型应该为： %s" % ('advanced.positioner', '#file_url','advanced.positioner.#file_url', str), 'Error', debug_info())
            exit()
        # constant
        elif type(self.template_cfg['advanced']['constant']) != dict:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('advanced.constant', type(self.template_cfg['advanced']['constant']), dict), 'Error', debug_info())
            exit()
        # variable
        elif type(self.template_cfg['advanced']['variable']) != dict:
            add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('advanced.variable', type(self.template_cfg['advanced']['variable']), dict), 'Error', debug_info())
            exit()
        add_log("添加预设变量： %s" % json_encode(self.template_preset_variables), 'Debug', debug_info())
        self.template_cfg['advanced'].update({'preset':{}})
        for i in self.template_preset_variables:
            self.template_cfg['advanced']['preset'].update({'$' + i: ''})
        add_log("检查定位器、常量和变量的命名是否正确", 'Debug', debug_info())
        for i in self.template_cfg['advanced']:
            if (len(self.template_cfg['advanced'][i]) != len(set(self.template_cfg['advanced'][i]))):
                add_log("模板 %s 节点上有重复的定位器、常量或变量" % 'advanced.' + i, 'Error', debug_info())
                exit()
            for j in self.template_cfg['advanced'][i]:
                if not check_template_variable_name(j, self.template_delimiter_map[i]):
                    add_log("模板 %s 节点不符合命名规范：第一个字符应为 %s ，第二个字符应为英文大小写字母或下划线，其余字符应为英文大小写字母、下划线或数字，字符串不短于 2 位" % ('advanced.' + i + '.' + j, self.template_delimiter_map[i]), 'Error', debug_info())
                    exit()
                if type(self.template_cfg['advanced'][i][j]) != str:
                    add_log("模板 %s 节点数据类型有误，当前类型为： %s ，应该为： %s" % ('advanced.' + i + '.' + j, type(self.template_cfg['advanced'][i][j]), str), 'Error', debug_info())
                    exit()
        add_log("检查是否引用了不存在的定位器、常量或变量", 'Debug', debug_info())
        traverse_res = traverse_dict(self.template_cfg)
        for i in traverse_res:
            for j in range(0, 2):
                for k in self.template_delimiter_map:
                    str_include = list_template_string_include(i[j], self.template_delimiter_map[k], True)
                    if str_include != [] and not set(str_include).issubset(set(self.template_cfg['advanced'][k])):
                        add_log("模板 %s 节点引用了不存在的定位器、常量或变量： %s" % (i[2], json_encode(list(set(str_include) - set(self.template_cfg['advanced'][k])))), 'Error', debug_info())
                        exit()
        add_log("检查是否存在死循环引用或受引用控制策略限制", 'Debug', debug_info())
        for i in traverse_res:
            detect_res = detect_template_include_loop(self.template_cfg['advanced'], {i[0]: i[1]}, self.template_delimiter_map, True)
            if detect_res == True:
                add_log("在模板 %s 节点上检查到了死循环引用" % i[2], 'Error', debug_info())
                exit()
            else:
                acl_check_seq = ["_root"] + i[3]
                acl_position = deepcopy(self.template_acl)
                for j in acl_check_seq:
                    if j == "_root":
                        default_acl_rule = acl_position["_default_global_policy"]
                        acl_rule = acl_position["_policy"]
                    elif j in acl_position:
                        acl_position = acl_position[j]
                        acl_rule = acl_position["_policy"]
                    elif j in acl_rule:
                        acl_rule = acl_rule[j]
                    else:
                        acl_rule['key'] = acl_rule['sub_key']
                        acl_rule['value'] = acl_rule['sub_value']
                        acl_rule['sub_key'] = None
                        acl_rule['sub_value'] = None
                for j in list(acl_rule.keys()):
                    if acl_rule[j] == None:
                        acl_rule[j] = default_acl_rule[j]
                    if j not in ['key', 'value']:
                        acl_rule.pop(j)
                for j in detect_res['k']:
                    if len(detect_res['k'][j]) != 0 and acl_rule['key'][j] != True:
                        add_log("根据模板引用策略，以下定位器、常量或变量不能在模板 %s 节点上引用： %s ，引用策略对此节点的限制为： %s" % (i[2], json_encode(detect_res['k'][j]), json_encode(acl_rule['key'])), 'Error', debug_info())
                        exit()
                for j in detect_res['v']:
                    if len(detect_res['v'][j]) != 0 and acl_rule['value'][j] != True:
                        add_log("根据模板引用策略，以下定位器、常量或变量不能在模板 %s 节点上引用： %s ，引用策略对此节点的限制为： %s" % (i[2], json_encode(detect_res['v'][j]), json_encode(acl_rule['value'])), 'Error', debug_info())
                        exit()
        add_log("添加运行时内部变量", 'Debug', debug_info())
        self.template_cfg['advanced'].update({'runtime': {'scrap_result': '', 'template_name': self.template}})
        add_log("更新预设变量", 'Debug', debug_info())
        self.set_template_preset_variable('tags', self.tags)
        self.set_template_preset_variable('page', self.start)
        self.set_template_preset_variable('proxy', self.proxy['http'])
        self.set_template_preset_variable('index', 0)
        self.template_reader = TemplateReader(self.template_cfg, self.template_delimiter_map)
        add_log("模板检查通过", 'Debug', debug_info())

    def set_template_preset_variable(self, variable_name, value):
        if '$' + variable_name in self.template_cfg['advanced']['preset']:
            self.set_template_config('["advanced"]["preset"]["$' + variable_name + '"]', value)
            # self.template_cfg['advanced']['preset']['$' + variable_name] = value
        else:
            return False
        return True

    def set_template_runtime_variable(self, variable_name, value):
        if variable_name in self.template_cfg['advanced']['runtime']:
            self.set_template_config('["advanced"]["runtime"]["' + variable_name + '"]', value)
        else:
            return False
        return True

    def set_template_config(self, target, value):
        exec('self.template_cfg' + target + ' = value')
        self.template_reader = TemplateReader(self.template_cfg, self.template_delimiter_map)
        return True

    def get_mode(self):
        return self.mode

    def get_available_template(self):
        template_list = dir_list(self.program_path + self.template_dirname, False, False)
        available_template = []
        for i in range(0, len(template_list)):
            if template_list[i][:1] != "_":
                available_template.append(file_splitext(template_list[i])[0])
        return available_template

    def hello(self):
        add_log("欢迎使用 danbooru 图片下载工具 %s" % self.VERSION, 'Info', debug_info())

    def copyright(self):
        add_log("版本： %s" % self.VERSION, 'Info', debug_info())
        add_log("作者： %s" % self.AUTHOR, 'Info', debug_info())
        add_log("最后修改时间： %s" % self.LAST_REVISE_TIME, 'Info', debug_info())
        add_log("Powered By %s. Some Rights Reserved." % self.AUTHOR, 'Info', debug_info())
    
    def update(self):
        add_log("正在检测更新", 'Info', debug_info())
        update_data = u_check(self.VERSION, self.proxy)
        update_data = json_decode(update_data)
        if 'status' in update_data and int(update_data['status']) == 1:
            update_data = update_data['data']
            if self.VERSION != update_data['version']:
                add_log("获取更新信息成功，当前版本： %s ，最新版本： %s" % (self.VERSION, update_data['version']), 'Info', debug_info())
                confirm_update = input("是否确认更新？（y/n）")
                if confirm_update not in ['', None] and confirm_update[0] in ['y', 'Y']:
                    add_log("开始自动更新", 'Info', debug_info())
                    tmp_dir = self.program_path + "/" + ".tmp/"
                    add_log("创建临时目录", 'Info', debug_info())
                    u_mkdir(tmp_dir) # 创建临时文件夹
                    update_data = update_data['op']
                    for i in update_data['add']:
                        add_log("从 %s 下载更新" % i['source'] , 'Info', debug_info())
                        u_download(i['source'], tmp_dir + i['dir'], i['name'], self.proxy)
                    for i in update_data['del']['dir']:
                        add_log("删除目录 %s" % i, 'Info', debug_info())
                        u_delete(self.program_path + "/" + i, 'dir')
                    for i in update_data['del']['file']:
                        add_log("删除文件 %s" % i, 'Info', debug_info())
                        u_delete(self.program_path + "/" + i)
                    add_log("从临时目录复制到 %s" % self.program_path, 'Info', debug_info())
                    u_copy(tmp_dir, self.program_path)
                    add_log("删除临时目录", 'Info', debug_info())
                    u_delete(tmp_dir, 'dir')
                else:
                    add_log("用户取消更新", 'Info', debug_info())
            else:
                add_log("已经是最新版本", 'Info', debug_info())
        else:
            add_log("获取更新信息失败，请尝试手动更新", 'Warn', debug_info())

    def page(self):
        add_log("根据页面ID下载", 'Info', debug_info())
        if self.end == -1: # 下载到最后一页
            add_log("下载到最后一页", 'Info', debug_info())
            page_count = self.start # 初始化页码计数器
            while True:
                add_log("正在获取第 %s 页图片列表" % page_count, 'Info', debug_info())
                self.set_template_preset_variable('page', page_count)
                request_api = self.template_reader.read(['mode', 'page', 'api'])
                request_method = self.template_reader.read(['mode', 'page', 'method'])
                request_header = self.template_reader.read(['mode', 'page', 'header'])
                request_data = self.template_reader.read(['mode', 'page', 'data'])
                request_result = simple_http_api_request(request_api, request_method, self.retry_max, request_header, request_data, self.proxy)
                request_result = json_decode(request_result) # json2list
                add_log("第 %s 页图片列表获取成功" % page_count, 'Info', debug_info())
                self.set_template_runtime_variable('scrap_result', request_result)
                request_result = self.template_reader.read(['advanced', 'positioner', '#root'], is_positioner = True)
                if len(request_result) == 0: # 判断是否已无图片可供下载
                    add_log("已无图片可供下载", 'Warn', debug_info())
                    break
                add_log("正在解析图片列表", 'Info', debug_info())
                download_info = []
                for i in range(0, len(request_result)): # 将图片链接添加到列表
                    self.set_template_preset_variable('index', i)
                    if self.template_reader.read(['advanced', 'positioner', '#file_url'], is_positioner = True):
                        download_info.append({
                                'positioner': {
                                    'id': self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True),
                                    'md5': self.template_reader.read(['advanced', 'positioner', '#md5'], is_positioner = True),
                                    'file_url': self.template_reader.read(['advanced', 'positioner', '#file_url'], is_positioner = True)
                                    },
                                'download': {
                                    'metadata': self.template_reader.read(['mode', 'page', 'download', 'metadata']),
                                    'filename': self.template_reader.read(['mode', 'page', 'download', 'filename']),
                                    'metadata_filename': self.template_reader.read(['mode', 'page', 'download', 'metadata_filename']),
                                    'header': self.template_reader.read(['mode', 'page', 'download', 'header'])
                                    }
                                })
                    else:
                        add_log("已跳过一个未提供下载链接的文件", 'Warn', debug_info())
                add_log("解析成功", 'Info', debug_info())
                start_download(download_info, self.thread, self.path, self.proxy, self.retry_max, self.deduplication, self.chksums, self.with_metadata, self.program_path, self.template_reader.read(['advanced', 'runtime', 'template_name'])) # 传给下载器接口
                page_count += 1 # 页码计数器+1
        elif self.end >= self.start: # 下载部分页码
            add_log("下载部分页码，从第 %s 页下载到第 %s 页" % (self.start, self.end), 'Info', debug_info())
            for i in range(self.start, self.end + 1):
                add_log("正在获取第 %s 页图片列表" % i, 'Info', debug_info())
                self.set_template_preset_variable('page', i)
                request_api = self.template_reader.read(['mode', 'page', 'api'])
                request_method = self.template_reader.read(['mode', 'page', 'method'])
                request_header = self.template_reader.read(['mode', 'page', 'header'])
                request_data = self.template_reader.read(['mode', 'page', 'data'])
                request_result = simple_http_api_request(request_api, request_method, self.retry_max, request_header, request_data, self.proxy)
                request_result = json_decode(request_result)
                add_log("第 %s 页图片列表获取成功" % i, 'Info', debug_info())
                self.set_template_runtime_variable('scrap_result', request_result)
                request_result = self.template_reader.read(['advanced', 'positioner', '#root'], is_positioner = True)
                if len(request_result) == 0:
                    add_log("已无图片可供下载", 'Warn', debug_info())
                    break
                add_log("正在解析图片列表", 'Info', debug_info())
                download_info = []
                for j in range(0, len(request_result)):
                    self.set_template_preset_variable('index', j)
                    if self.template_reader.read(['advanced', 'positioner', '#file_url'], is_positioner = True):
                        download_info.append({
                                'positioner': {
                                    'id': self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True),
                                    'md5': self.template_reader.read(['advanced', 'positioner', '#md5'], is_positioner = True),
                                    'file_url': self.template_reader.read(['advanced', 'positioner', '#file_url'], is_positioner = True)
                                    },
                                'download': {
                                    'metadata': self.template_reader.read(['mode', 'page', 'download', 'metadata']),
                                    'filename': self.template_reader.read(['mode', 'page', 'download', 'filename']),
                                    'metadata_filename': self.template_reader.read(['mode', 'page', 'download', 'metadata_filename']),
                                    'header': self.template_reader.read(['mode', 'page', 'download', 'header'])
                                    }
                                })
                    else:
                        add_log("已跳过一个未提供下载链接的文件", 'Warn', debug_info())
                add_log("解析成功", 'Info', debug_info())
                start_download(download_info, self.thread, self.path, self.proxy, self.retry_max, self.deduplication, self.chksums, self.with_metadata, self.program_path, self.template_reader.read(['advanced', 'runtime', 'template_name']))

    def id(self):
        add_log("根据图片ID下载", 'Info', debug_info())
        if self.end == -1: # 下载到最新一张图
            add_log("下载到最新一张图", 'Info', debug_info())
            page_count = 1
            end_point = False # 退出循环标记
            while True:
                if end_point == True: # 当标记为true则退出循环
                    break
                add_log("正在获取第 %s 页图片列表" % page_count, 'Info', debug_info())
                self.set_template_preset_variable('page', page_count)
                request_api = self.template_reader.read(['mode', 'id', 'api'])
                request_method = self.template_reader.read(['mode', 'id', 'method'])
                request_header = self.template_reader.read(['mode', 'id', 'header'])
                request_data = self.template_reader.read(['mode', 'id', 'data'])
                request_op_symbol = self.template_reader.read(['mode', 'id', 'op_symbol'])
                request_result = simple_http_api_request(request_api, request_method, self.retry_max, request_header, request_data, self.proxy)
                request_result = json_decode(request_result)
                add_log("第 %s 页图片列表获取成功" % page_count, 'Info', debug_info())
                self.set_template_runtime_variable('scrap_result', request_result)
                request_result = self.template_reader.read(['advanced', 'positioner', '#root'], is_positioner = True)
                if len(request_result) == 0:
                    add_log("已无图片可供下载", 'Warn', debug_info())
                    break
                add_log("正在解析图片列表", 'Info', debug_info())
                self.set_template_preset_variable('index', 0)
                page_start_id = self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True)
                self.set_template_preset_variable('index', -1)
                page_end_id = self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True)
                if self.start > page_start_id and page_count == 1: # 判断指定的开始ID是否大于第一页的第一个ID，出现这种错误很显然是ID写错了，例如网站中最新一张图的ID是8000，开始ID写成了80000
                    add_log("指定的开始ID： %s 大于最新ID： %s" % (self.start, page_start_id), 'Error', debug_info())
                    break
                download_info = []
                for i in range(0, len(request_result)):
                    self.set_template_preset_variable('index', i)
                    if self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True) >= self.start: # 如果本次迭代的图片ID在设定的范围中则将图片链接添加到列表
                        if self.template_reader.read(['advanced', 'positioner', '#file_url'], is_positioner = True):
                            download_info.append({
                                    'positioner': {
                                        'id': self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True),
                                        'md5': self.template_reader.read(['advanced', 'positioner', '#md5'], is_positioner = True),
                                        'file_url': self.template_reader.read(['advanced', 'positioner', '#file_url'], is_positioner = True)
                                        },
                                    'download': {
                                        'metadata': self.template_reader.read(['mode', 'page', 'download', 'metadata']),
                                        'filename': self.template_reader.read(['mode', 'page', 'download', 'filename']),
                                        'metadata_filename': self.template_reader.read(['mode', 'page', 'download', 'metadata_filename']),
                                        'header': self.template_reader.read(['mode', 'page', 'download', 'header'])
                                        }
                                    })
                        else:
                            add_log("已跳过一个未提供下载链接的文件", 'Warn', debug_info())
                    else: # 否则结束迭代并标记
                        end_point = True
                        break
                add_log("解析成功", 'Info', debug_info())
                start_download(download_info, self.thread, self.path, self.proxy, self.retry_max, self.deduplication, self.chksums, self.with_metadata, self.program_path, self.template_reader.read(['advanced', 'runtime', 'template_name']))
                page_count += 1
        elif self.end >= self.start: # 根据图片ID区间下载
            add_log("从图片ID： %s 下载到图片ID： %s " % (self.start, self.end), 'Info', debug_info())
            loop_count = 1
            end_point = False
            while True:
                if end_point == True: # 当标记为true则退出循环
                    break
                echo_op_symbol = "小于等于" if loop_count == 1 else "小于"
                echo_id = self.end if loop_count == 1 else page_end_id
                add_log("正在获取图片ID %s %s 的图片列表" % (echo_op_symbol, echo_id), 'Info', debug_info())
                request_op_symbol = self.template_reader.read(['mode', 'id', 'op_symbol'])
                id_tag = request_op_symbol['id_range'] + request_op_symbol['lt'] + (str(self.end + 1) if loop_count == 1 else str(page_end_id))
                self.set_template_preset_variable('page', 1)
                self.set_template_preset_variable('tags', self.tags + "+" + id_tag if self.tags not in self.null_list else id_tag)
                request_api = self.template_reader.read(['mode', 'id', 'api'])
                request_method = self.template_reader.read(['mode', 'id', 'method'])
                request_header = self.template_reader.read(['mode', 'id', 'header'])
                request_data = self.template_reader.read(['mode', 'id', 'data'])
                request_result = simple_http_api_request(request_api, request_method, self.retry_max, request_header, request_data, self.proxy)
                request_result = json_decode(request_result)
                add_log("图片列表获取成功", 'Info', debug_info())
                self.set_template_runtime_variable('scrap_result', request_result)
                request_result = self.template_reader.read(['advanced', 'positioner', '#root'], is_positioner = True)
                if len(request_result) == 0:
                    add_log("已无图片可供下载", 'Warn', debug_info())
                    break
                add_log("正在解析图片列表", 'Info', debug_info())
                self.set_template_preset_variable('index', 0)
                page_start_id = self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True) if request_result else 0 # 获取当页第一个ID，如果返回的列表为空则设为0
                self.set_template_preset_variable('index', -1)
                page_end_id = self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True) if request_result else 0 # 获取当页最后一个ID，如果返回的列表为空则设为0
                if self.start > page_start_id and loop_count == 1: # 判断指定的开始ID是否大于第一页的第一个ID
                    add_log("指定的开始ID： %s 大于可获取到的最新ID： %s" % (self.start, page_start_id), 'Error', debug_info())
                    break
                if self.start >= page_end_id: # 当开始ID大于等于当页最后一个ID（代表最后一张要下载的图片在当前页）则标记结束循环，进行最后一次遍历
                    end_point = True
                download_info = []
                for i in range(0, len(request_result)):
                    self.set_template_preset_variable('index', i)
                    if self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True) <= self.end and self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True) >= self.start: # 如果本次迭代的图片ID在设定的范围中则将图片链接添加到列表
                        if self.template_reader.read(['advanced', 'positioner', '#file_url'], is_positioner = True):
                            download_info.append({
                                    'positioner': {
                                        'id': self.template_reader.read(['advanced', 'positioner', '#id'], is_positioner = True),
                                        'md5': self.template_reader.read(['advanced', 'positioner', '#md5'], is_positioner = True),
                                        'file_url': self.template_reader.read(['advanced', 'positioner', '#file_url'], is_positioner = True)
                                        },
                                    'download': {
                                        'metadata': self.template_reader.read(['mode', 'page', 'download', 'metadata']),
                                        'filename': self.template_reader.read(['mode', 'page', 'download', 'filename']),
                                        'metadata_filename': self.template_reader.read(['mode', 'page', 'download', 'metadata_filename']),
                                        'header': self.template_reader.read(['mode', 'page', 'download', 'header'])
                                        }
                                    })
                        else:
                            add_log("已跳过一个未提供下载链接的文件", 'Warn', debug_info())
                    else: # 否则略过
                        pass
                add_log("解析成功", 'Info', debug_info())
                start_download(download_info, self.thread, self.path, self.proxy, self.retry_max, self.deduplication, self.chksums, self.with_metadata, self.program_path, self.template_reader.read(['advanced', 'runtime', 'template_name']))
                loop_count += 1

    def bye(self):
        add_log("所有下载任务完成", 'Info', debug_info())
        add_log("脚本正常退出", 'Info', debug_info())