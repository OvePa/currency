import time
import random


def do_something():
    if random.randint(0, 1) == 0:
        print("Failure")
        raise RuntimeError
    print("Success")


while True:
    try:
        do_something()
    except Exception:
        # Sleep for one second before retrying
        time.sleep(1)
    else:
        break
