import sys
from functools import wraps


class OutputBuffer:

    def __init__(self):
        self.buffer = str()


    def write(self, s):
        self.buffer += s


    def read(self):
        return self.buffer


outbuf = OutputBuffer()


# class PrintToBuffer:

#     def __init__(self, func):
#         self.func = func

#     def __call__(self, *args, **kwargs):
#         sys.stdout = outbuf
#         result = self.func(*args, **kwargs)
#         sys.stdout = sys.__stdout__
#         return result


def redirect_stdout(func):
    '''
    redirect stdout to a string object
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        sys.stdout = outbuf
        result = func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return result
    return wrapper


if __name__ == '__main__':
    @redirect_stdout
    def hello_world():
        print 'hello, world'

    hello_world()
    print 'buffer: ' + outbuf.read()
