"""
etcd acquire lock

The following example shows two different methods to acquire the < lock >.
You can use < lock.acquire() > to get the lock and you can also use it with the
< with > statement, which makes it more readable and handles exceptions in an
easier way.
"""
import etcd3


def lock_acquire(lock):
    """This function acquires lock using lock_acquire()"""
    lock.acquire()
    try:
        print("do something")
    finally:
        lock.release()


def lock_with(lock):
    """This function acquires lock using with"""
    with lock:
        print("do something else")


client = etcd3.client()
lock = client.lock("foobar")

lock_acquire(lock)
lock_with(lock)


"""
For more robustness, deploying etcd as a cluster of several nodes makes sure 
that if the etcd server that your application connects to goes down, the rest 
of the cluster can continue to work, and likewise your clients, as long as 
they switch to a different server when an error occurs (though this feature 
is not implemented in python-etcd3 yet).
"""
