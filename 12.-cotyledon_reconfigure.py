"""
Reconfiguration
Last, but not least, Cotyledon also offers a few more features, such as reloading
the program configuration or changing the number of workers for a class dynamically.
"""
import multiprocessing
import time
import cotyledon


class Manager(cotyledon.ServiceManager):
    def __init__(self):
        super(Manager, self).__init__()
        queue = multiprocessing.Manager().Queue()
        self.add(ProducerService, args=(queue,))
        self.printer = self.add(PrinterService, args=(queue,), workers=2)
        self.register_hooks(on_reload=self.reload)

    def reload(self):
        print("Reloading")
        self.reconfigure(self.printer, 5)


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
In the example given above, only two processes for PrinterService are started. 
As soon as SIGHUP is sent to the master process, Cotyledon calls the Manager.reload 
method that reconfigures the printer service to now have five processes. 
This is easy to check. In the above application, open another terminal and enter 
the command ps ax | grep cotyledon to see the running processes.

Cotyledon is an excellent library for managing long-running processes. Leverage it 
to build long-running, background, job workers.
"""
