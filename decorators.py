from contextlib import contextmanager
from functools import wraps
import logging
import sys
import time
from timeit import timeit

def logged(cls):
    ''' 
    Добавляет логирование.
    '''
    logger = logging.getLogger(cls.__name__)
    logger.addHandler(logging.NullHandler())
    cls.logger = logger
    return cls

"""
@logged
class Foo():
    def call(self):
       self.logger.info("SPAM!")

s = Foo()
s.call()
"""

def logged_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.addHandler(logging.NullHandler())
        return func(*args, **kwargs)
    return wrapper


def timethis(name=None, enable=True):
    ''' 
    Декоратор, который выводит время выполнения. 
    '''
    def decorate(func):
        if enable:
            logger = logging.getLogger(func.__name__)
            logger.addHandler(logging.NullHandler())

            @wraps(func)
            def wrapper(*args, **kwargs):

                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                #print(func.__name__, end - start)
                logger.info("TIMETHIS - {}".format(str(end - start)))
                return result

            return wrapper
        else:
            return func
    return decorate

"""
@timethis
def countdown(n):
    while n > 0:
        n -= 1

countdown(100000)
"""

@contextmanager
def timeblock(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        #print("{} - {}".format(label, str(end - start)))
        logger = logging.getLogger(label)
        logger.addHandler(logging.NullHandler())
        logger.info("TIMEBLOCK - {}".format(str(end - start)))


"""
with timeblock('counting'):
    n = 10000000
    while n > 0:
        n -= 1
"""

"""
timeit('math.sqrt(2)', 'import math')
timeit('sqrt(2)', 'from math import sqrt')
"""


