# -*- coding: utf-8 -*-

import argparse
from core.constant import *

def ap():
    ap = argparse.ArgumentParser(description=script_description, formatter_class = argparse.RawTextHelpFormatter)
    ap.add_argument("-m", "--mode", required = True, choices = allow_mode, help = mode_help)
    ap.add_argument("-s", "--start", required = False, type = int, default = default_start, help = start_help)
    ap.add_argument("-e", "--end", required = False, type = int, default = default_end, help = end_help)
    ap.add_argument("-l", "--limit", required = False, type = int, default = default_limit, help = limit_help)
    ap.add_argument("-t", "--tags", required = False, default = default_tags, help = tags_help)
    ap.add_argument("-T", "--thread", required = False, type = int, default = default_thread, help = thread_help)
    ap.add_argument("-p", "--path", required = False, default = default_path, help = path_help)
    ap.add_argument("-P", "--proxy", required = False, default = default_proxy, help = proxy_help)
    ap.add_argument("-o", "--options", required = False, default = default_options, help = options_help)
    ap.add_argument("--file-config-path", required = False, default = default_file_config_path, help = file_config_path_help)
    ap.add_argument("--retry-max", required = False, type = int, default = default_retry_max, help = retry_max_help)
    args = vars(ap.parse_args())

    return args