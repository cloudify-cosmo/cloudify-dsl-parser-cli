import logging
import sys
import os

info_logger = None
error_logger = None
cli_logger = None


def init():
    global info_logger
    global error_logger
    global cli_logger

    info_logger = logging.getLogger('info-logger')
    error_logger = logging.getLogger('error-logger')
    cli_logger = logging.getLogger('dsl-cli')

    info_handler = logging.StreamHandler(sys.stdout)
    error_handler = logging.StreamHandler(sys.stderr)
    verbose_handler = logging.FileHandler(os.getenv('CLI_LOGGER_FILE',
                                                    'cli-debug.log'))

    clean_format = logging.Formatter('%(message)s')
    verbose_format = logging.Formatter('%(asctime)s - %(name)s '
                                       '- %(levelname)s - %(message)s')

    info_handler.setFormatter(clean_format)
    error_handler.setFormatter(clean_format)
    verbose_handler.setFormatter(verbose_format)

    info_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    verbose_handler.setLevel(logging.DEBUG)

    info_logger.setLevel(logging.INFO)
    error_logger.setLevel(logging.ERROR)
    cli_logger.setLevel(logging.DEBUG)

    info_logger.addHandler(info_handler)
    error_logger.addHandler(error_handler)
    cli_logger.addHandler(verbose_handler)


def info(*args, **kwargs):
    info_logger.info(*args, **kwargs)
    cli_logger.info(*args, **kwargs)


def error(*args, **kwargs):
    error_logger.error(*args, **kwargs)
    cli_logger.error(*args, **kwargs)


def exception(*args, **kwargs):
    error_logger.exception(*args, **kwargs)
    cli_logger.exception(*args, **kwargs)


def debug(*args, **kwargs):
    cli_logger.debug(*args, **kwargs)


if __name__ == '__main__':
    init()
    debug('this is a debug message')
    error('this is a error message')
    info('this is an info message')
