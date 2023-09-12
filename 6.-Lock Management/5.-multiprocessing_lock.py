"""
Multiprocessing with lock
The way to fix that is to lock the standard output until the cat is fully
printed on the screen. This is easily done by using a multiprocessing.Lock.
"""
import multiprocessing
import time

stdout_lock = multiprocessing.Lock()


def print_cat():
    # Add some randomness by waiting a bit
    time.sleep(0.1)
    with stdout_lock:
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
