# -*- coding: utf-8 -*-

from func.fileio import file_mkdir
from time import localtime, strftime
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, getLogger, FileHandler, Formatter, StreamHandler
from colorlog import ColoredFormatter

def construct(path, set_log_level = "Info", no_print_log = False):
    global logger, handler, console

    log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'bold_red',
    'CRITICAL': 'red',
    }

    if set_log_level == "Debug":
        set_log_level = DEBUG
    elif set_log_level == "Info":
        set_log_level = INFO
    elif set_log_level == "Warn":
        set_log_level = WARNING
    elif set_log_level == "Error":
        set_log_level = ERROR
    elif set_log_level == "None":
        set_log_level = CRITICAL
    else:
        set_log_level = INFO

    logger = getLogger(__name__)

    logger.setLevel(level = set_log_level)
    date = strftime("%Y%m%d", localtime())
    log_file_path = "%s/logs/%s/" % (path, date)
    log_file_name = "log.log"
    file_mkdir(log_file_path)

    handler = FileHandler(log_file_path + log_file_name, encoding="utf-8", mode="a")
    handler.setLevel(set_log_level)
    # formatter = Formatter('%(asctime)s|%(levelname)s|%(message)s|%(name)s')
    formatter = Formatter('%(asctime)s|%(levelname)s|%(message)s')
    handler.setFormatter(formatter)

    console_log_level = set_log_level if not no_print_log else CRITICAL
    console = StreamHandler()
    console.setLevel(console_log_level)
    color_formatter = ColoredFormatter('%(log_color)s%(asctime)s|%(levelname)s|%(message)s', log_colors = log_colors_config) # 彩色日志输出格式
    console.setFormatter(color_formatter)

    logger.addHandler(handler)
    logger.addHandler(console)

def reconstruct(path, set_log_level = "Info", no_print_log = False):
    global logger, handler, console
    logger.removeHandler(handler)
    logger.removeHandler(console)
    construct(path, set_log_level, no_print_log)

def add_log(text, type = None, debug_info = ""):
    global logger
    text = text if logger.level != DEBUG else "%s|%s" % (debug_info, text)
    if type == None or type == "Info":
        logger.info(text)
    elif type == "Debug":
        logger.debug(text)
    elif type == "Warn":
        logger.warning(text)
    elif type == "Error":
        logger.error(text)
    elif type == "None":
        pass
    else:
        logger.info(text)
    return text