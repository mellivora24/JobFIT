import logging


logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def print_log(level, message):
    """
    In log khi ứng dụng hoạt động
    :param level: Mức độ log ("debug", "info", "warning", "error")
    :param message: Nội dung log
    """
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    else:
        logging.debug(message)

# Đã kiểm thử
