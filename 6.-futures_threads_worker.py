# pip install futures ya viene instalado en py3 stdlibrary
"""
The concurrent.futures module is pretty straightforward to use. First, one needs
to pick an executor. An executor is responsible for scheduling and running
asynchronous tasks. It can be seen as a type of engine for execution.
The module currently provides two kinds of executors: concurrent.futures.ThreadPoolExecutor
and concurrent.futures.ProcessPoolExecutor. As one might guess,
the first one is based on threads and the second one on processes.

The process-based executor is going to be much more efficient for long-running
tasks that benefit from having an entire CPU available. The threading executor
suffers from the same limitation as the threading module.

-> concurrent.futures.Future abstraction <-
So what is interesting about the concurrent.futures module is that it provides
an easier-to-use abstraction layer on top of the threading and multiprocessing
modules. It allows one to run and parallelize code in a straightforward way,
providing an abstract data structure called a concurrent.futures.Future object.

Each time a program schedules some tasks to execute in threads or processes,
the concurrent.futures module returns a Future object for each of the tasks scheduled.
This Future object owns the promise of the work to be completed. Once that work
is achieved, the result is available in that Future object. So in the end,
it does represent the future and the promise of a task to be performed.
That is why it is called “Future” in Python, and sometimes “promise” in other languages.
"""
# cmd
# time python 6.-futures_threads_worker.py

from concurrent import futures
import random


def compute():
    return sum([random.randint(1, 100) for i in range(1000000)])


with futures.ThreadPoolExecutor(max_workers=8) as executor:
    futs = [executor.submit(compute) for _ in range(8)]

results = [f.result() for f in futs]

print("Results: %s" % results)


"""
The code just schedules the jobs to be fulfilled and collects the results from 
the Future objects using the result method, which also supports a timeout parameter 
in case the program cannot hang for too long. Future objects offer some more 
interesting methods:

done(): This returns True if the call was successfully canceled or terminated 
    correctly.
add_done_callback(fn): This attaches a callable to the future which is called 
    with the future as its only argument; it is done as soon as the future is 
    canceled or terminates correctly
"""
