from threading import Lock


class Singleton(object):

    __singleton_instance = None
    __singleton_lock = Lock()

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls, *args, **kwargs):
        Singleton.__singleton_lock.acquire()
        try:
            if cls.__singleton_instance is None:
                cls.__singleton_instance = cls(*args, **kwargs)
        except Exception as e:
            print(f'Error in creating singleton object of class {cls.__name__}, {e}')
        finally:
            Singleton.__singleton_lock.release()
        return cls.__singleton_instance


if __name__ == '__main__':

    class AppliedSingleton(Singleton):

        def __init__(self, name=''):
            Singleton.__init__(self)
            self.name = name

        def __str__(self):
            return self.name

    a = AppliedSingleton.get_instance(name='a')
    b = AppliedSingleton.get_instance(name='b')

    print(a is b)
    print(a.name)
    print(b.name)
    a.name = 'hello-world'
    print(a.name)
    print(b.name)
