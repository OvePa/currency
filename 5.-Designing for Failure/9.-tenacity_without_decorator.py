"""
No decorator

Tenacity can also be used without a decorator by using the object Retrying,
which implements its main behavior and uses its call method. This object allows
one to call any function with different retry conditions, as in the following
example, or to retry any piece of code that does not use the decorator at all,
like code from an external library.
"""
import tenacity
import random


def do_something():
    if random.randint(0, 1) == 0:
        print("Failure")
        raise IOError
    print("Success")
    return True


r = tenacity.Retrying(
    wait=tenacity.wait_fixed(1), retry=tenacity.retry_if_exception_type(IOError)
)

r.call(do_something)
