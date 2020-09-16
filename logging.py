'''
This plugin allows the user to use 'logging-enable' to start logging the vd.status (warning, debug etc.) to a file (set in options.log_path).
It can also be used within other plugins with 'logging.enable_logging()'.
'''

__author__ = 'Geekscrapy'
__version__ = '1.0'

from visidata import *
import logging, sys

option(name='log_path', default='vd.log', helpstr='location and filename to save the log file')
option(name='log_logger_root', default='vd', helpstr='logging.getLogger root')
option(name='log_verbose_fmt', default='{asctime} {name}@{lineno} {levelname} {message}', helpstr='verbose format for use with options.debug')
option(name='log_status_fmt', default='{message}', helpstr='minimal vd (original) format')
option(name='log_verbose_datefmt', default='%H:%M:%S', helpstr='date format to be used')

class vd_log_handler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno == logging.CRITICAL:
            vd.oldstatus(self.format(record), priority=3)
        elif record.levelno == logging.ERROR:
            vd.oldstatus(self.format(record), priority=2)
        elif record.levelno == logging.WARNING:
            vd.oldstatus(self.format(record), priority=1)
        elif record.levelno == logging.INFO:
            vd.oldstatus(self.format(record), priority=0)
        else:
            vd.oldstatus(self.format(record))


def logging_status(*args, **kwargs):

    priority = kwargs.get('priority')

    if priority == 3:
        priority = logging.CRITICAL
    elif priority == 2:
        priority = logging.ERROR
    elif priority == 1:
        priority = logging.WARNING
    elif priority == 0:
        priority = logging.INFO
    else:
        priority = logging.INFO

    str_args = list(filter(lambda x: isinstance(x, str),args))
    if not str_args:
        return True

    frame_records = inspect.stack()[1]
    func_name = inspect.stack()[1][3]
    calling_module = inspect.getmodulename(frame_records[1])

    logger = logging.getLogger(f'{options.log_logger_root}.{calling_module}.{func_name}')

    if options.debug:
        logger.setLevel(logging.DEBUG)

    if sys.version_info >= (3,8,0):     # stacklevel available
        logger.log(level=priority, msg=''.join(str_args), stacklevel=2)
    else:                               # be grateful, update Python :P
        logger.log(level=priority, msg=''.join(str_args))

    return True

@VisiData.api
def is_logging_enabled(*args, **kwargs):
    if getattr(vd, 'oldstatus', None):
        return True
    else:
        return False

@VisiData.api
def enable_logging(*args, **kwargs):

    if is_logging_enabled():
        warning(f'already enabled, logging to {options.log_path}')
        return

    verbose_fmt = logging.Formatter(options.log_verbose_fmt, datefmt=options.log_verbose_datefmt, style='{')
    status_fmt = logging.Formatter(options.log_status_fmt, style='{')

    logger = logging.getLogger(options.log_logger_root)

    # file logger
    file_handler = logging.FileHandler(options.log_path)
    file_handler.setFormatter(verbose_fmt)
    logger.addHandler(file_handler)

    # vd.status logger
    vd_handler = vd_log_handler()
    if options.debug:
        vd_handler.setFormatter(verbose_fmt)
        logger.setLevel(logging.DEBUG)
    else:
        vd_handler.setFormatter(status_fmt)
        logger.setLevel(logging.INFO)
    logger.addHandler(vd_handler)

    # replace vd.status
    vd.oldstatus = vd.status
    vd.status = logging_status

    status(f'logging to {options.log_path}', priority=2)

@VisiData.api
def disable_logging(*args, **kwargs):

    if not is_logging_enabled():
        warning("already disabled")
        return

    vd.status = vd.oldstatus
    vd.oldstatus = None

    status(f'logging disabled', priority=2)

Sheet.addCommand(None, 'logging-enable', 'enable_logging()', helpstr='enable verbose logging, and logging to a file')
Sheet.addCommand(None, 'logging-disable', 'disable_logging()', helpstr='disable verbose logging, and logging to a file')
