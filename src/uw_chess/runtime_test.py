# ============================================================================
# runtime_test.py
# logging the time it takes to run functions
# ============================================================================

import functools
import time
import pkg_resources

class LogExecutionTime:
    """
    A decorator class for logging the execution time of functions.

    This class, when used as a decorator, measures the time a function takes to execute
    and logs this information to a specified text file.

    Attributes:
        func (callable): The function to be decorated.
        log_file (str): Path to the file where the log will be written.
    """

    def __init__(self, func):
        """
        Initializes the LogExecutionTime decorator.

        Args:
            func (callable): The function to be decorated.
            log_file (str, optional): Path to the log file. Defaults to "execution_time_log.txt".
        """
        self.func = func
        
        self.log_file = pkg_resources.resource_filename(__name__, "./tests/execution_time_log.txt")
        functools.wraps(func)(self)

    def __call__(self, *args, **kwargs):
        """
        Executes the wrapped function and logs its execution time.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the wrapped function.
        """
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()

        # Log the execution time to the specified file
        with open(self.log_file, "a") as file:
            file.write(f"{self.func.__name__} executed in {end_time - start_time} seconds\n")

        return result

    def __get__(self, instance, owner):
        """
        Supports instance methods.

        Args:
            instance: The instance that the method is being called on.
            owner: The class that the instance method belongs to.

        Returns:
            A partial function with the instance bound as the first argument.
        """
        if instance is None:
            return self
        return functools.partial(self.__call__, instance)
