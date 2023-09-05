from concurrent import futures
import random


# cmd
# time python 7.-futures_processes_worker.py
def compute():
    return sum([random.randint(1, 100) for i in range(1000000)])


if __name__ == "__main__":
    with futures.ProcessPoolExecutor() as executor:
        futs = [executor.submit(compute) for _ in range(8)]

    results = [f.result() for f in futs]

    print("Results: %s" % results)


"""
There is no need to set the number of max_workers: as by default concurrent.futures 
calls the multiprocessing.cpu_count function to set the number of workers to use, 
which is equal to the number of CPUs the system can use as is shown in the following example.

class ProcessPoolExecutor(_base.Executor):
  def __init__(self, max_workers=None):
    # [...]
    if max_workers is None:
      self._max_workers = multiprocessing.cpu_count()
    else:
      self._max_workers = max_workers
"""
"""
Warning: One important thing to notice with both of the pool based executors is 
the way they manage the processes and threads they spawn. There are several 
policies that the authors could have implemented. The one selected is that for 
each job submitted, a new worker is spawned to do the work, and the work is put in 
a queue shared across all the existing workers. That means that if the caller 
sets max_workers to 20, then 20 workers will exist as soon as 20 jobs are submitted. 
None of those processes will ever be destroyed. This is different than, for example, 
Apache httpd workers that exit after being idle for a while. You can see that this 
is marked as a TODO in Python source code as shown in the following example.

class ThreadPoolExecutor(_base.Executor):
  def submit(self, fn, *args, **kwargs):
    [...]
    self._adjust_thread_count()

  def _adjust_thread_count(self):
    [...]
    # TODO(bquinlan): Should avoid creating new threads if there are more
    # idle threads than items in the work queue.
    if len(self._threads) < self._max_workers:
      t = threading.Thread(target=_worker,
      args=(weakref.ref(self, weakref_cb),
      self._work_queue))
      t.daemon = True
      t.start()
      self._threads.add(t)
      _threads_queues[t] = self._work_queue
"""
