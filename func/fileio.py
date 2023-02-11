# -*- coding: utf-8 -*-

import os.path
from shutil import rmtree, copytree
from os import remove, makedirs

def file_mkdir(path):
    try:
        if not os.path.exists(path): # 验证下载目录是否存在，不存在则创建
            makedirs(path)
        return True
    except:
        return False

def file_delete(path, type = None):
    try:
        if type == 'dir':
            rmtree(path)
        else:
            remove(path)
        return True
    except:
        return False

def file_copy(path, to):
    copytree(path, to, dirs_exist_ok = True)
    return True

def file_is_exist(path):
    if os.path.exists(path):
        return True
    else:
        return False

def file_write_binary(path, content, mode = 'wb'):
    with open(path, mode) as f:
        f.write(content)
        return True

def file_write(path, content, mode = 'w'):
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)
        return True

def file_read(path, mode = 'r'):
    with open(path, mode) as f:
        return f.read()