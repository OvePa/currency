"""
tenacity.wait_exponential()

"""
import tenacity
import random


def do_something():
    if random.randint(0, 1) == 0:
        print("Failure")
        raise RuntimeError
    print("Success")


@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=0.5, max=30, exp_base=2),
)
def do_something_and_retry():
    do_something()


do_something_and_retry()

"""
The way the decorator is configured in the above example makes the algorithm 
retry after waiting first 1 second, then waiting 2 seconds, then 4 seconds, 
8 seconds, 16 seconds, and then 30 seconds, keeping that last value for all the 
subsequent retries. The back-off algorithm computes the time to wait by computing 
min(multiplier * (exp_base^retry_attempt_number), max) and using that number of 
seconds. It makes sure that if a request is unable to succeed quickly after a retry, 
the application waits longer and longer each time rather than repeatedly hammering 
the targeted subsystem at a fixed interval.
"""
