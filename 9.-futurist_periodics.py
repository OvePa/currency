"""
futurist.periodics
futurist addresses a widespread use case with the futurist.periodics.
PeriodicWorker class. It allows scheduling functions to run regularly,
based on the system clock.
"""

# cmd
# python 9.-futurist_periodics.py

import time

from futurist import periodics


@periodics.periodic(1)
def every_one(started_at):
    print("1: %s" % (time.time() - started_at))


w = periodics.PeriodicWorker(
    [
        (every_one, (time.time(),), {}),
    ]
)


@periodics.periodic(4)
def print_stats():
    print("stats: %s" % list(w.iter_watchers()))


w.add(print_stats)
w.start()

"""
The above example implements two tasks: one runs every second and prints the 
time elapsed since the start of the task. The second task runs every four 
seconds and prints statistics about the running of those tasks. Here, once again, 
futurist offers internal access to its statistics, which is very handy for 
reporting the status of the application.

While not necessary to depend on, futurist is a great improvement over 
concurrent.futures if you need fine-grained control over the execution of your 
threads or processes.
"""
