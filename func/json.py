# -*- coding: utf-8 -*-

from json import decoder, loads, dumps
from func.log import add_log
from func.debug import debug_info

def json_decode(json):
    # try:
        json = loads(json)
        return json
    # except decoder.JSONDecodeError as e:
    #     add_log("%s: 解析“%s”时发生错误: %s" % (e.__class__.__name__, json, e), 'Error', debug_info())
    #     exit()

def json_encode(text, ensure_ascii = False):
    json = dumps(text, ensure_ascii = ensure_ascii)
    return json

def json_encode_with_format(text):
    json = dumps(text, indent = 4, separators=(',', ': '), ensure_ascii = False)
    return json