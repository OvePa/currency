import multiprocessing
import random

"""
Using multiprocessing.Pool, there is no need to manage the processes “manually”. 
The pool starts processes on-demand and takes care of reaping them when done. 
They are also reusable, reducing the usage of the fork system call, which is 
quite costly. It is a convenient design pattern that is also leveraged in futures, 
as discussed in the next lesson.
"""


def compute(n):
    return sum([random.randint(1, 100) for i in range(1000000)])


if __name__ == "__main__":
    # Start 8 workers
    pool = multiprocessing.Pool(processes=8)
    print("Results: %s" % pool.map(compute, range(8)))
