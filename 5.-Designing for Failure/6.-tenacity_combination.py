"""
Combining methods

Another interesting point of tenacity is that you can easily combine several
methods. For example, you can combine tenacity.wait.wait_random with
tenacity.wait.wait_fixed to wait a number of seconds defined in an interval.
"""
import tenacity
import random


def do_something():
    if random.randint(0, 1) == 0:
        print("Failure")
        raise RuntimeError
    print("Success")


@tenacity.retry(wait=tenacity.wait_fixed(10) + tenacity.wait_random(0, 3))
def do_something_and_retry():
    do_something()


do_something_and_retry()

"""
This makes the function being retried wait randomly for between 10 and 13 seconds 
before trying again.
"""
