"""
Retry based on combining conditions

You can combine several conditions easily by using the | or & binary operators.
In the next example, the conditions set up make the code retry if an RuntimeError
exception is raised, or if no result is returned. Also, a stop condition is
added using the stop keyword arguments. It allows specifying a stop condition
based on a maximum delay.
"""
import tenacity
import random


def do_something():
    if random.random() > 0.0002:
        print("Failure")
        raise RuntimeError
    print("Success")
    return True


@tenacity.retry(
    wait=tenacity.wait_fixed(1),
    stop=tenacity.stop_after_delay(60),
    retry=(
        tenacity.retry_if_exception_type(RuntimeError)
        | tenacity.retry_if_result(lambda result: result is None)
    ),
)
def do_something_and_retry():
    return do_something()


do_something_and_retry()
