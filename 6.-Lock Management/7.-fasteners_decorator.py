"""
Fasteners decorator
Fasteners also provides a function decorator to easily lock an entire function
as shown.
"""
import time
import fasteners


@fasteners.interprocess_locked("/tmp/tmp_lock_file")
def locked_print():
    for i in range(10):
        print("I have the lock")
        time.sleep(0.1)


locked_print()

"""
Fasteners locks are reliable and efficient. They do not have a 
single-point-of-failure (except the operating system itself). So, they are a 
good choice for interprocess locking needs that are local to a machine.
"""
