"""
Reentrant lock

In the case that one of your threads might need to acquire a lock multiple
times (internally, the reentrant lock uses the concepts of owning thread and
recursion level), the threading.RLock provides what is called a reentrant lock.
This type of lock can be acquired multiple times by the same thread, rather
than being blocked when already acquired.
"""
import threading

rlock = threading.RLock()

with rlock:
    with rlock:
        print("Double acquired")


"""
Note: If a threading.Lock was being used in the above example instead, 
the program would be in a dead-lock state, unable to continue its execution.
"""
