"""
threading.Event

The last commonly used object for synchronizing thread is threading.Event.
You can think about this object being a boolean value - being True or False.
A thread can set the value to true by calling threading.Event.set() and another
thread can wait for the value to become True by calling threading.Event.wait().

One of the most common use cases for such an object is to synchronize the
background thread with your main thread on exit.
"""
import threading
import time

stop = threading.Event()


def background_job():
    while not stop.is_set():
        print("I'm still running!")
        stop.wait(0.1)


t = threading.Thread(target=background_job)
t.start()
print("thread started")
time.sleep(2)
stop.set()
t.join()


"""
As boring as the above example might be, it shows pretty well how the main 
thread can let the secondary thread know that it is time to stop. The usage 
of a threading.Event object for such synchronization between threads is a 
popular design pattern when using threads.
"""
