import random
import multiprocessing

"""
This example is a bit trickier to write as there is no data shared between 
different processes. Since each process is a new, independent instance of Python, 
the data is copied, and each process has its own independent global state. 
The multiprocessing.Manager class provides a way to create shared data structures 
that are safe for concurrent accesses.
"""


# cmd
# time python 4.-multiprocessing_workers.py
def compute(results):
    results.append(sum([random.randint(1, 100) for i in range(1000000)]))


if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        results = manager.list()
        workers = [
            multiprocessing.Process(target=compute, args=(results,)) for x in range(8)
        ]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
        print("Results: %s" % results)
