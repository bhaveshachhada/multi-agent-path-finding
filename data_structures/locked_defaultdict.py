from threading import Lock
from collections import defaultdict


class LockedDefaultDict(defaultdict):

    def __init__(self, method):
        defaultdict.__init__(method)
        self.lock = Lock()

    def __setitem__(self, key, value):
        try:
            self.lock.acquire()
            defaultdict.__setitem__(key, value)
        except Exception as e:
            print(f'Exception in setitem:{e}')
        finally:
            self.lock.release()

    def __getitem__(self, item):
        data = None
        try:
            self.lock.acquire()
            data = defaultdict.__getitem__(item)
        except Exception as e:
            print(f'Exception in getitem:{e}')
        finally:
            self.lock.release()
        return data
