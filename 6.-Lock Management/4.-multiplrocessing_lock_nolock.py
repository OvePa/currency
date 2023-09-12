"""
When all programs accessing a shared resource are written in Python, the natural
method to secure accesses is to use the multiprocessing.Lock objects provided
by Python. That class is built around POSIX or Windows semaphores (depending on
your operating system) and allows use of a lock across several processes.

Multiprocessing with no lock
"""
import multiprocessing
import time


def print_cat():
    # Add some randomness by waiting a bit
    time.sleep(0.1)
    print(" /\\_/\\")
    print("( o.o )")
    print(" > ^ <")


if __name__ == "__main__":
    with multiprocessing.Pool(processes=3) as pool:
        jobs = []
        for _ in range(5):
            jobs.append(pool.apply_async(print_cat))
        for job in jobs:
            job.wait()


"""
The above example is a very simple example that uses multiprocessing.Pool to 
print cats in ASCII art. The program launches up to 3 processes that have to 
print 5 cats in parallel.

Observe by running the above application, that the cats are a bit mixed up. 
The standard output is shared across all the processes printing cats, and they 
are stepping on each other’s toes.
"""
