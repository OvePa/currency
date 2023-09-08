"""
The get_lock method provided by the coordinator allows getting a distributed
lock from the selected backend. This lock implements two main methods: acquire
and release. They both return True or False based on their success or failure
to operate.
"""
import etcd3

client = etcd3.client()
lock = client.lock("foobar")
lock.acquire()
try:
    print("do something")
finally:
    lock.release()


"""
The above example shows how you can use those methods to acquire and release a 
lock. The acquire lock method accepts a blocking parameter which is True by 
default. This makes the caller wait until the lock is available, which can 
take forever. If forever is too long for the program, blocking can also be set 
to the number of seconds (or False, which is equivalent to zero second) to wait 
before either succeeding and returning True, or giving up and returning False.
"""
