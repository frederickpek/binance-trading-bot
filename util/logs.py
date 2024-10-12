import logging
from util.lark import send_lark_msg


def setup_logger(log_file_name: str="main"):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(f"data/{log_file_name}.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    original_info = logger.info
    original_error = logger.error
    original_exception = logger.exception
    def info_with_lark(msg, *args, send_lark=False, **kwargs):
        original_info(msg, *args, **kwargs)
        if send_lark: send_lark_msg(msg)
    def error_with_lark(msg, *args, send_lark=False, **kwargs):
        original_error(msg, *args, **kwargs)
        if send_lark: send_lark_msg(msg)
    def exception_with_lark(msg, *args, send_lark=False, **kwargs):
        original_exception(msg, *args, **kwargs)
        if send_lark: send_lark_msg(msg)
    logger.info = info_with_lark
    logger.error = error_with_lark
    logger.exception = exception_with_lark

setup_logger()

