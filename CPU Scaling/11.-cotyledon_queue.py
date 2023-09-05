"""
Producer/consumer using cotyledon
The following example shows an implementation of the common producer/consumer pattern.
In this pattern, a service fills a queue (the producer), and other services
(the consumers) consume the jobs to execute them.
"""
import multiprocessing
import time
import cotyledon


# cmd
# python 11.cotyledon_queue.py
class Manager(cotyledon.ServiceManager):
    def __init__(self):
        super(Manager, self).__init__()
        queue = multiprocessing.Manager().Queue()
        self.add(ProducerService, args=(queue,))
        self.add(PrinterService, args=(queue,), workers=2)


class ProducerService(cotyledon.Service):
    def __init__(self, worker_id, queue):
        super(ProducerService, self).__init__(worker_id)
        self.queue = queue

    def run(self):
        i = 0
        while True:
            self.queue.put(i)
            i += 1
            time.sleep(1)


class PrinterService(cotyledon.Service):
    name = "printer"

    def __init__(self, worker_id, queue):
        super(PrinterService, self).__init__(worker_id)
        self.queue = queue

    def run(self):
        while True:
            job = self.queue.get(block=True)
            print(
                "I am Worker: %d PID: %d and I print %s"
                % (self.worker_id, self.pid, job)
            )


Manager().run()


"""
The above example implements a custom cotyledon.ServiceManager that is in charge 
of creating the queue object. This queue object is passed to all the services. 
The ProducerService uses that queue and fills it with an incremented integer 
every second, whereas the PrinterService instances consume from that queue and 
print its content.

When run, each worker would print its worker_id along with the process ID (pid) 
and the job.

The multiprocessing.queues.Queue object eases the communication between different 
processes. It is safe to use across threads and processes, as it leverages locks 
internally to guarantee data safety.
"""
