import threading

"""
When a thread is a daemon, it is considered as a background thread by Python 
and is terminated as soon as the main thread exits.
"""


def print_something(something):
    print(something)


t = threading.Thread(target=print_something, args=("hello",))
t.daemon = True
t.start()
print("thread started")
