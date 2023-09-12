"""
Retrying based on condition

Tenacity offers more customization, such as retrying on some exceptions only.
"""
import tenacity
import random


def do_something():
    if random.randint(0, 1) == 0:
        print("Failure")
        raise RuntimeError
    print("Success")


@tenacity.retry(
    wait=tenacity.wait_fixed(1), retry=tenacity.retry_if_exception_type(RuntimeError)
)
def do_something_and_retry():
    return do_something()


do_something_and_retry()

"""
In the above example, tenacity is leveraged to retry every second to execute the 
function only if the exception raised by do_something is an instance of RuntimeError.
"""
