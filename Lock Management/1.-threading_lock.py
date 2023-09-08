import threading

stdout_lock = threading.Lock()


def print_something(something):
    with stdout_lock:
        print(something)


t = threading.Thread(target=print_something, args=("hello",))
t.daemon = True
t.start()
print_something("thread started")

"""
The lock does not force the order of the execution, but it makes sure only one 
of the threads can use print at the same time, avoiding any data corruption. 
Imagine that instead of stdout the thread would write to the same file. That 
would be some significant data corruption! That is why locks are always required 
when accessing shared resources.
"""
