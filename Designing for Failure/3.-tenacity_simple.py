"""
tenacity.Retrying()

This will make the function do_something be called over and over again until
it succeeds by not raising any kind of exception.
"""
import tenacity
import random


def do_something():
    if random.randint(0, 1) == 0:
        print("Failure")
        raise RuntimeError
    print("Success")


tenacity.Retrying()(do_something)

"""
Obviously, this is a pretty rare case. Retrying without any delay is not what 
most applications want, as it can heavily burden the failing subsystem. 
An application usually needs to wait between retries.
"""
