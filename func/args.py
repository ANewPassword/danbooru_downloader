# -*- coding: utf-8 -*-

import argparse
from core.constant import *

def ap():
    ap = argparse.ArgumentParser(description=script_description, formatter_class = argparse.RawTextHelpFormatter)
    ap.add_argument("-m", "--mode", required = True, choices = allow_mode, help = mode_help)
    ap.add_argument("-t", "--template", required = False, default = default_template, help = template_help)
    ap.add_argument("-s", "--start", required = False, type = int, default = default_start, help = start_help)
    ap.add_argument("-e", "--end", required = False, type = int, default = default_end, help = end_help)
    ap.add_argument("-T", "--tags", required = False, default = default_tags, help = tags_help)
    ap.add_argument("-p", "--path", required = False, default = default_path, help = path_help)
    ap.add_argument("-P", "--proxy", required = False, default = default_proxy, help = proxy_help)
    ap.add_argument("--thread", required = False, type = int, default = default_thread, help = thread_help)
    ap.add_argument("--file-config-path", required = False, default = default_file_config_path, help = file_config_path_help)
    ap.add_argument("--retry-max", required = False, type = int, default = default_retry_max, help = retry_max_help)
    ap.add_argument("--log-level", required = False, choices = allow_log_mode, default = default_log_level, help = log_level_help)
    ap.add_argument("--deduplication", required = False, choices = allow_deduplication_mode, default = default_deduplication, help = deduplication_help)
    ap.add_argument("--chksums", required = False, action='store_true', default = default_chksums, help = chksums_help)
    ap.add_argument("--with-metadata", required = False, action='store_true', default = default_with_metadata, help = with_metadata_help)
    ap.add_argument("--make-config", required = False, action='store_true', default = default_make_config, help = make_config_help)
    ap.add_argument("--no-print-log", required = False, action='store_true', default = default_no_print_log, help = no_print_log_help)

    args = vars(ap.parse_args())

    return args