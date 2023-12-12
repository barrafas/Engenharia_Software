""" Module: Database Utils

Description: This module contains the database utils.

Functions:
    timeout: Decorator to set a timeout for a function.
    TimeExceedError: Exception raised when the timeout is exceeded.
    TimeoutDecorator: Decorator to set a timeout for a DatabaseModule.
"""
import functools
import platform

from src.database.database_module import DatabaseModule

class TimeExceedError(Exception):
    """Raised when the timeout is exceeded"""
    pass

def timeout(seconds, error_message="Timeout"):
    """ Timeout for the decorator.

    Args:
        seconds (int): The timeout in seconds.
        error_message (str): The error message to be raised.

    Returns:
        function: The decorated function.
    """
    def decorator(func):
        """ Timeout for the decorator.

        Args:
            func (function): The function to be decorated.

        Returns:
            function: The decorated function.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """ wrapper function """
            result = None
            exception = None

            # Check the operating system and import the appropriate module
            if platform.system() == "Windows":
                import threading

                def worker():
                    nonlocal result, exception
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        exception = e

                thread = threading.Thread(target=worker)
                thread.start()
                thread.join(seconds)

                if thread.is_alive():
                    raise TimeExceedError(error_message)
                elif exception is not None:
                    raise exception

                return result

            else:
                import signal

                def handler(signum, frame):
                    raise TimeExceedError(error_message)

                def worker():
                    nonlocal result, exception
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        exception = e

                signal.signal(signal.SIGALRM, handler)
                signal.alarm(seconds)

                try:
                    worker()
                finally:
                    signal.alarm(0)

                if exception is not None:
                    raise exception

                return result

        return wrapper

    return decorator

class TimeoutDecorator(DatabaseModule):
    """ Decorator to set a timeout for a DatabaseModule.

    Args:
        decorated (DatabaseModule): The DatabaseModule to be decorated.
        timeout_seconds (int): The timeout in seconds.
    """
    def __init__(self, decorated, timeout_seconds=10):
        """ 
        Constructor method

        Args:
            decorated (DatabaseModule): The DatabaseModule to be decorated.
            timeout_seconds (int): The timeout in seconds.
        """
        self._decorated = decorated
        self._timeout_seconds = timeout_seconds

    def _timeout_wrapper(self, method):
        """
        Function to wrap a method with a timeout.

        Args:
            method (function): The method to be wrapped.
        """
        @timeout(self._timeout_seconds)
        def wrapped_method(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapped_method

    def connect(self):
        """ Connect to the database."""
        print("Connecting to the database...")
        # return self._timeout_wrapper(self._decorated.connect)()
        return self._decorated.connect()

    def disconnect(self):
        """ Disconnect from the database."""
        return self._timeout_wrapper(self._decorated.disconnect)()

    def insert_data(self, collection_name, data):
        """ Insert data into the database."""
        return self._timeout_wrapper(self._decorated.insert_data)(collection_name,
                                                                  data)

    def delete_data(self, collection_name, condition):
        """ Delete data from the database."""
        return self._timeout_wrapper(self._decorated.delete_data)(collection_name,
                                                                  condition)

    def update_data(self, collection_name, condition, new_data):
        """ Update data in the database."""
        return self._timeout_wrapper(self._decorated.update_data)(collection_name,
                                                                  condition,
                                                                  new_data)

    def select_data(self, collection_name, condition):
        """ Select data from the database."""
        return self._timeout_wrapper(self._decorated.select_data)(collection_name,
                                                                  condition)

    def __str__(self):
        """ String representation of the object."""
        return "@timeout("+str(self._decorated)+")"

    # setting the getters for the attributes of the decorated object
    @property
    def host(self):
        """ Getter for the host attribute."""
        return self._decorated.host

    @property
    def port(self):
        """ Getter for the port attribute."""
        return self._decorated.port

    @property
    def user(self):
        """ Getter for the user attribute."""
        return self._decorated.user
    
    @property
    def password(self):
        """ Getter for the password attribute."""
        return self._decorated.password