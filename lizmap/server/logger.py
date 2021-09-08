__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

import functools
import inspect
import time
import traceback

from contextlib import contextmanager
from pathlib import Path

from qgis.core import Qgis, QgsMessageLog

PLUGIN = 'Lizmap'


class Logger:

    @staticmethod
    def info(message: str):
        QgsMessageLog.logMessage(PLUGIN + ' : ' + message, PLUGIN, Qgis.Info)

    @staticmethod
    def warning(message: str):
        QgsMessageLog.logMessage(PLUGIN + ' : ' + message, PLUGIN, Qgis.Warning)

    @staticmethod
    def critical(message: str):
        QgsMessageLog.logMessage(PLUGIN + ' : ' + message, PLUGIN, Qgis.Critical)

    @staticmethod
    def log_exception(e: BaseException):
        """ Log a Python exception. """
        QgsMessageLog.logMessage(
            "Exception: {plugin}\n{e}\n{traceback}".format(
                plugin=PLUGIN,
                e=e,
                traceback=traceback.format_exc()
            ),
            PLUGIN,
            Qgis.Critical
        )


def exception_handler(func):
    """ Decorator to catch all exceptions. """
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            Logger.log_exception(e)
    return inner_function


@contextmanager
def trap():
    """ Define a trap context for catching all exceptions """
    try:
        yield
    except Exception as e:
        Logger.log_exception(e)


def log_function(func):
    """ Decorator to log function. """
    @functools.wraps(func)
    def log_function_core(*args, **kwargs):
        QgsMessageLog.logMessage('{}.{}'.format(PLUGIN, func.__name__), PLUGIN, Qgis.Info)
        value = func(*args, **kwargs)
        return value

    return log_function_core


def profiling(func):
    """ Decorator to make some profiling. """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        Logger.info(
            "{}.{}.{} ran in {}s".format(
                PLUGIN, Path(inspect.stack()[1].filename).stem, func.__name__, round(end - start, 2)))
        return result

    return wrapper


def log_output_value(func):
    """ Decorator to log the output of the function. """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        Logger.info(
            "{}.{}.{} output is {} for parameter {}".format(
                PLUGIN, Path(inspect.stack()[1].filename).stem, func.__name__, result, str(args)))
        return result

    return wrapper
