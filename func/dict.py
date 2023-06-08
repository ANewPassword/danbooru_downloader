# -*- coding: utf-8 -*-

def traverse_dict(d, result = None, position_handler = None):
    if result == None:
        result = []
    if position_handler == None:
        position_handler = []
    for key, value in d.items():
        position = ''
        position_list = position_handler + [key]
        if isinstance(value, str):
            for i in position_list:
                if position != '':
                    position = position + '.' + i
                else:
                    position = i
            result.append((key, value, position, position_list))
        elif isinstance(value, dict):
            traverse_dict(value, result, position_list)
    return result

def get_dict_value_by_position_list(d, position_list):
    v = d
    for k in position_list:
            v = v[k]
    return v

def deep_update(base_dict, update_dict):
    for k, v in update_dict.items():
        if isinstance(v, dict):
            base_dict[k] = deep_update(base_dict.get(k, {}), v)
        elif isinstance(v, list):
            base_dict[k] = base_dict.get(k, []) + v
        else:
            base_dict[k] = v
    return base_dict