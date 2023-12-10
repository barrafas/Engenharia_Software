import signal
import functools
from src.database.database_module import DatabaseModule


class TimeExceedError(Exception):
    pass

def timeout(seconds, error_message="Timeout"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeExceedError(error_message)

            # Set the signal handler and timeout
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                # Reset the alarm
                signal.alarm(0)

            return result

        return wrapper

    return decorator

class TimeoutDecorator(DatabaseModule):
    def __init__(self, decorated, timeout_seconds=5):
        self._decorated = decorated
        self._timeout_seconds = timeout_seconds

    def _timeout_wrapper(self, method):
        @timeout(self._timeout_seconds)
        def wrapped_method(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapped_method

    def connect(self):
        return self._timeout_wrapper(self._decorated.connect)()

    def disconnect(self):
        return self._timeout_wrapper(self._decorated.disconnect)()

    def insert_data(self, collection_name, data):
        return self._timeout_wrapper(self._decorated.insert_data)(collection_name, data)

    def delete_data(self, collection_name, condition):
        return self._timeout_wrapper(self._decorated.delete_data)(collection_name, condition)

    def update_data(self, collection_name, condition, new_data):
        return self._timeout_wrapper(self._decorated.update_data)(collection_name, condition, new_data)

    def select_data(self, collection_name, condition):
        return self._timeout_wrapper(self._decorated.select_data)(collection_name, condition)
