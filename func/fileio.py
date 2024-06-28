# -*- coding: utf-8 -*-

import os.path
from shutil import rmtree, copytree
from os import remove, makedirs, listdir, walk
from os.path import getsize
from time import time

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

def file_write_stream(path, stream: any, timeout = 600, chunk_size = 1048576, mode = 'wb'):
    start_time = time()
    with open(path, mode) as f:
        for chunk in stream.iter_content(chunk_size = chunk_size):
            elapsed_time = time() - start_time
            if elapsed_time >= timeout and timeout != -1:
                stream.close()
                return False
            if chunk:
                f.write(chunk)
    return True

def file_write(path, content, mode = 'w'):
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)
        return True

def file_read(path, mode = 'r'):
    with open(path, mode, encoding="utf-8") as f:
        return f.read()

def file_splitext(path):
    return os.path.splitext(path)

def file_size(path):
    return getsize(path)

def dir_tree(path, build_tree = True, full_path = False):
    if build_tree:
        tree = {}
        for name in listdir(path):
            abs_path = os.path.join(path, name)
            if full_path:
                record_name = abs_path
            else:
                record_name = name
            if os.path.isfile(abs_path):
                tree[record_name] = None
            elif os.path.isdir(abs_path):
                tree[record_name] = dir_tree(abs_path, True, full_path)
    else:
        tree = []
        for dirpath, dirs, files in walk(path):
            for name in files:
                if full_path:
                    record_name = os.path.join(path, os.path.join(dirpath, name))
                else:
                    record_name = os.path.relpath(os.path.join(dirpath, name), path)
                tree.append(record_name)
    return tree

def dir_list(path, include_sub_dir = True, full_path = False):
    lst = listdir(path) if include_sub_dir else [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    if full_path:
        for i in range(0, len(lst)):
            lst[i] = os.path.join(path, lst[i])

    return lst