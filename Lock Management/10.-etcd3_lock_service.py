"""
Locking service with etcd and cotyledon
The next example implements a distributed service using the Cotyledon library.
It spawns four different processes, and only one is authorized to print at any
given time.
"""
import threading
import time
import cotyledon
import etcd3


class PrinterService(cotyledon.Service):
    name = "printer"

    def __init__(self, worker_id):
        super(PrinterService, self).__init__(worker_id)
        self._shutdown = threading.Event()
        self.client = etcd3.client()

    def run(self):
        while not self._shutdown.is_set():
            with self.client.lock("print"):
                print("I'm %s and I'm the only one printing" % self.worker_id)
                time.sleep(1)

    def terminate(self):
        self._shutdown.set()


# Create a manager
manager = cotyledon.ServiceManager()
# Add 4 PrinterService to run
manager.add(PrinterService, 4)
# Run all of that
manager.run()

"""
You can run this program any number of times on any number of machines on your 
network and you can be sure that one and only one process at a time will own 
this lock and be able to print its line. Since the lock is acquired for a tiny 
amount of time (a print operation and one second), we do not expect it to timeout. 
The default time-to-live for a lock is 60 seconds, which ought to be enough. 
If the program takes longer to print something and sleep one second, then 
something is wrong, and it might be better to let the lock expire.

However, for sustained operations, an application should not cheat and extend 
the time-to-live value. The program should keep the lock active by regularly 
calling the Lock.refresh method.

Combining such a distributed lock mechanism and a library like Cotyledon can 
make building a distributed service straightforward.
"""
