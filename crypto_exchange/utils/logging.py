import logging
import coloredlogs


def get_logger(name: str, level: str = "DEBUG"):
    """彩色日志

    :param name:
    :param level:
    :return:
    """
    logger = logging.getLogger(name)
    coloredlogs.install(level=level, logger=logger)
    return logger
