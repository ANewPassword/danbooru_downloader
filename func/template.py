# -*- coding: utf-8 -*-

from string import Template
from re import finditer, match
from sys import setrecursionlimit
from copy import deepcopy
from func.dict import get_dict_value_by_position_list
from func.log import add_log
from func.debug import debug_info
import ast

setrecursionlimit(114)

def list_template_string_include(template_str, template_delimiter = "$", with_delimiter = True):
    variables = []
    pattern = '(\%s+)\{([a-zA-Z_][a-zA-Z0-9_]*)\}' % template_delimiter
    for match in finditer(pattern, template_str):
        delimiter_signs = match.group(1)
        variable_name = match.group(2)
        if len(delimiter_signs) % 2 != 0:
            if variable_name not in variables:
                variables.append(variable_name if not with_delimiter else template_delimiter + variable_name)
    return variables

def check_template_variable_name(variable_name, template_delimiter = "$"):
    if len(variable_name) == 0:
        return False
    if variable_name[:1] != template_delimiter:
        return False
    if not match(r'^[a-zA-Z_]', variable_name[1:2]):
        return False
    if not match(r'^[a-zA-Z0-9_]+$', variable_name[2:]) and variable_name[2:] != '':
        return False
    return True

def detect_template_include_loop(template_advanced_dict, template_target_kv, delimiter_map, return_list = False, include_map = None, position_handler = None, root_position = None):
    if include_map is None:
        include_map = {'k': {}, 'v': {}}
    if position_handler is None:
        position_handler = {'k': ['k'], 'v': ['v']}
    if root_position is None:
        root_position = {'k': 'k', 'v': 'v'}
    def update_include_map(include_map, position, new_include):
        # position = position.split(".")
        if len(position) == 1:
            include_map[position[0]].update(new_include)
            return True
        update_include_map(include_map[position[0]], position[1:], new_include)
        return True
    def map_to_list(map, delimiter_map, lst = None):
        if lst == None:
            lst = {}
        for k, v in map.items():
            for kk, vv in delimiter_map.items():
                if k[:1] == vv:
                    if kk not in lst:
                        lst.update({kk: []})
                    lst[kk].append(k)
            if isinstance(v, dict):
                lst = map_to_list(v, delimiter_map, lst)
        for k, v in lst.items():
            lst[k] = list(set(v))
        return lst
    def detect_loop(d, visited_keys = None):
        if visited_keys is None:
            visited_keys = set()
        for key, value in d.items():
            if key in visited_keys:
                return True
            visited_keys.add(key)
            if isinstance(value, dict):
                if detect_loop(value, visited_keys):
                    return True
            visited_keys.remove(key)
        return False
    def key_part(template_advanced_dict, key_template_target_kv, delimiter_map, include_map = None, position_handler = None, root_position = None, first_call = True):
        k, v = next(iter(key_template_target_kv.items()))
        for kk, vv in delimiter_map.items():
            k_string_include = list_template_string_include(k if first_call else v, vv, False)
            if k_string_include != []:
                for i in k_string_include:
                    if root_position['k'] == 'k':
                        position_handler['k'] = ['k']
                        root_position['k'] = vv + i
                    update_include_map(include_map, position_handler['k'], {vv + i: {}})
                    position_handler['k'].append(vv + i)
                    if detect_loop(include_map):
                        return True
                    if key_part(template_advanced_dict, {vv + i: template_advanced_dict[kk][vv + i]}, delimiter_map, include_map, position_handler, root_position, False) == True:
                        return True
                    else:
                        root_position['k'] = position_handler['k'][-2]
                        position_handler['k'].pop()
    def value_part(template_advanced_dict, value_template_target_kv, delimiter_map, include_map = None, position_handler = None, root_position = None):
        k, v = next(iter(value_template_target_kv.items()))
        for kk, vv in delimiter_map.items():
            # v
            v_string_include = list_template_string_include(v, vv, False)
            if v_string_include != []:
                for i in v_string_include:
                    if root_position['v'] == 'v':
                        position_handler['v'] = ['v']
                        root_position['v'] = vv + i
                    update_include_map(include_map, position_handler['v'], {vv + i: {}})
                    position_handler['v'].append(vv + i)
                    if detect_loop(include_map):
                        return True
                    if value_part(template_advanced_dict, {vv + i: template_advanced_dict[kk][vv + i]}, delimiter_map, include_map, position_handler, root_position) == True:
                        return True
                    else:
                        root_position['v'] = position_handler['v'][-2]
                        position_handler['v'].pop()
    if key_part(template_advanced_dict, template_target_kv, delimiter_map, include_map, position_handler, root_position) == True:
        return True
    if value_part(template_advanced_dict, template_target_kv, delimiter_map, include_map, position_handler, root_position) == True:
        return True

    if return_list == True:
        res = {'k': map_to_list(include_map['k'], delimiter_map), 'v': map_to_list(include_map['v'], delimiter_map)}
    else:
        res = include_map
    return res

class TemplateReader:
    def __init__(self, template_cfg, delimiter_map):
        self.template_cfg = template_cfg
        self.delimiter_map = delimiter_map

    def read(self, position_list = None, target_value = None, is_positioner = False, is_variable = False):
        if position_list != None:
            target_value = get_dict_value_by_position_list(self.template_cfg, position_list)
        if isinstance(target_value, str):
            if is_variable:
                variable_env = {}
            for k,v in self.delimiter_map.items():
                target_value_include = list_template_string_include(target_value, v, False)
                template_var = {}
                if k == 'preset' and len(target_value_include) != 0:
                    for i in target_value_include:
                        if is_variable:
                            variable_env.update({'_' + k + '_' + i: self.template_cfg['advanced']['preset'][v + i] if self.template_cfg['advanced']['preset'][v + i] != None else ''})
                            template_var.update({i: '_' + k + '_' + i})
                        else:
                            template_var.update({i: self.template_cfg['advanced']['preset'][v + i] if self.template_cfg['advanced']['preset'][v + i] != None else ''})
                elif k == 'positioner' and len(target_value_include) != 0:
                    for i in target_value_include:
                        if is_variable:
                            variable_env.update({'_' + k + '_' + i: self.read(target_value = self.template_cfg['advanced']['positioner'][v + i], is_positioner = True)})
                            template_var.update({i: '_' + k + '_' + i})
                        else:
                            template_var.update({i: self.read(target_value = self.template_cfg['advanced']['positioner'][v + i], is_positioner = True)})
                elif k == 'constant' and len(target_value_include) != 0:
                    for i in target_value_include:
                        if is_variable:
                            variable_env.update({'_' + k + '_' + i: self.template_cfg['advanced']['constant'][v + i]})
                            template_var.update({i: '_' + k + '_' + i})
                        else:
                            template_var.update({i: self.template_cfg['advanced']['constant'][v + i]})
                elif k == 'variable' and len(target_value_include) != 0:
                    for i in target_value_include:
                        if is_variable:
                            variable_env.update({'_' + k + '_' + i: self.read(target_value = self.template_cfg['advanced']['variable'][v + i], is_variable = True)})
                            template_var.update({i: '_' + k + '_' + i})
                        else:
                            template_var.update({i: self.read(target_value = self.template_cfg['advanced']['variable'][v + i], is_variable = True)})
                try:
                    target_value = self.substitute(target_value, template_var, v)
                except Exception as e:
                    add_log("替换模板字符串时出现错误，尝试在安全替换模式下重新执行，但这可能导致部分定位器、常量或变量替换不正确", 'Debug', debug_info())
                    target_value = self.substitute(target_value, template_var, v, True)
                    add_log("在安全替换模式下执行成功", 'Debug', debug_info())
            if is_positioner == True:
                target_value = self.positioner_sandbox(self.template_cfg['advanced']['runtime']['scrap_result'], target_value)
            if is_variable == True:
                target_value = self.variable_sandbox(target_value, variable_env)
            return target_value
        elif isinstance(target_value, dict):
            target_value = deepcopy(target_value)
            for i in list(target_value.keys()):
                k = i
                v = target_value[i]
                k = self.read(target_value = i)
                if isinstance(v, dict):
                    v = self.read(target_value = v)
                else:
                    v = self.read(target_value = v)
                target_value.pop(i)
                target_value.update({k: v})
            return target_value
        elif isinstance(target_value, int) or isinstance(target_value, float):
            return target_value
        else:
            return target_value

    def substitute(self, template_str, template_var, template_delimiter = "$", safe_substitute = False):
        class CustomTemplateDelimiter(Template):
            delimiter = template_delimiter
        template_str = CustomTemplateDelimiter(template_str)
        template_res = template_str.safe_substitute(template_var) if safe_substitute else template_str.substitute(template_var)
        return template_res

    def positioner_sandbox(self, scrap_result, positioner):
        var_namespace = {'scrap_result': scrap_result}
        try:
            exec("exec_result = scrap_result%s" % positioner, var_namespace)
        except Exception as e:
            add_log("执行定位器时出现错误： %s: %s" % (e.__class__.__name__, e), 'Warn', debug_info())
            return ''
        return var_namespace['exec_result']

    def variable_sandbox(self, code, env = None):
        if env == None:
            var_namespace = {}
        else:
            var_namespace = env
        try:
            exec(code, var_namespace)
        except Exception as e:
            add_log("执行变量时出现错误： %s: %s" % (e.__class__.__name__, e), 'Warn', debug_info())
            return ''
        return var_namespace['exec_result']