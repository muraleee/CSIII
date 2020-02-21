from functools import wraps
import time


def time_me(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        x = time.time()
        res = func(*args, **kwargs)
        y = time.time() - x

        if y > 3600.0:
            msg = '{:4.3f} hours'.format(y / 3600.0)
        elif y > 60.0:
            msg = '{:4.3f} minutes'.format(y / 60.0)
        else:
            msg = '{:4.3f} seconds'.format(y)

        print('{} took {}'.format(func.__name__, msg))
        return res
    return wrapper
