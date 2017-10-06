from datetime import datetime
from functools import wraps


def my_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(datetime.now())
        func(*args, **kwargs)
    return wrapper


@my_decorator
def hello():
    print("hello world!")


@my_decorator
def add(num1, num2):
    sum = num1 + num2
    print('{} + {} = {}'.format(num1, num2, sum))


hello()
add(1, 2)
print(hello.__name__)








