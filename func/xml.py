# -*- coding: utf-8 -*-

from xmltodict import parse
from func.log import add_log
from func.debug import debug_info

def xml_decode(xml):
    return parse(xml)