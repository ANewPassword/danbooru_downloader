# -*- coding: utf-8 -*-
from requests import get
from requests.packages import urllib3
from func.fileio import file_mkdir, file_delete, file_copy
from func.http import check_update
from func.download import update_download

def u_check(version, proxy_address = ""):
    return check_update(version, proxy_address)

def u_delete(path, type = None):
    return file_delete(path, type)

def u_mkdir(path):
    return file_mkdir(path)

def u_copy(path, to):
    return file_copy(path, to)

def u_download(url, dir, filename, proxy_address = ""):
    return update_download(url, dir, filename, proxy_address)