# -*- coding: utf-8 -*-

import sys
import os
import traceback

def debug_info(print_exc = False):
    result = traceback.extract_stack()
    caller = result[len(result)-2]
    # 获取调用函数的模块文件绝对路径
    file_path_of_caller = str(caller).split(',')[0].lstrip('<FrameSummary file ')
    # 调用函数的模块文件名
    file_name_of_caller = os.path.basename(file_path_of_caller)
    # 获取函数被调用时所处模块的代码行
    code_line_when_called = sys._getframe().f_back.f_lineno

    if print_exc:
        traceback.print_exc()
    return "%s:%s" % (file_name_of_caller, code_line_when_called)
