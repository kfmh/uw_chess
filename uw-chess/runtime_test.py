import functools
import time

class LogExecutionTime:
    def __init__(self, func):
        self.func = func
        functools.wraps(func)(self)

    def __call__(self, *args, **kwargs):
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()
        print(f"{self.func.__name__} executed in {end_time - start_time} seconds")
        return result

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return functools.partial(self.__call__, instance)
