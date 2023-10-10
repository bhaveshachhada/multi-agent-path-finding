import threading
import traceback
from functools import wraps


class ThreadSafe:

    def __init__(self, lock: threading.RLock):
        self.lock = lock

    def __call__(self, function):

        @wraps(function)
        def decorator(*args, **kwargs):

            self.lock.acquire()
            output = None
            try:
                output = function(*args, **kwargs)
            except Exception as e:
                print(f'ERROR: while executing {function.__name__}, error: {e}')
                print(traceback.format_exc())
            finally:
                self.lock.release()
                return output

        return decorator
