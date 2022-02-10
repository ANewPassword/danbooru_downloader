# -*- coding: utf-8 -*-
from json import decoder, loads
from func.log import add_log

def read_json(json, path):
    try:
        json = loads(json)
        return json
    except decoder.JSONDecodeError as e:
        print(add_log("%s: 解析“%s”时发生错误: %s" % (e.__class__.__name__, json, e), path, 'Error'))
        exit()