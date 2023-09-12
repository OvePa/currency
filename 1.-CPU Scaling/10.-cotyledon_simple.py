"""
A widespread use case is to run long-running, background processes
(often called daemons) that are responsible for scheduling some tasks regularly
or processing jobs from a queue.

It could be possible to leverage concurrent.futures and a ProcessPoolExecutor
to do that, as discussed in Using Futures. However, the pool does not provide
any control regarding how it dispatches jobs. The same goes for using the
multiprocessing module. They both make it hard to efficiently control the
running of background tasks. Think of it as the “pets vs. cattle” analogy for
processes.
"""
"""
-> cotyledon <-

This section introduces you to cotyledon, a Python library designed to build 
long-running processes.
"""
import threading
import time
import cotyledon


# cmd
# python cotyledon_simple.py


class PrinterService(cotyledon.Service):
    name = "printer"

    def __init__(self, worker_id):
        super(PrinterService, self).__init__(worker_id)
        self._shutdown = threading.Event()

    def run(self):
        while not self._shutdown.is_set():
            print("Doing stuff")
            time.sleep(1)

    def terminate(self):
        self._shutdown.set()


# Create a manager
manager = cotyledon.ServiceManager()
# Add 2 PrinterService to run
manager.add(PrinterService, 2)
# Run all of that
manager.run()

"""
The above example is a simple implementation of a daemon using Cotyledon. 
It creates a class named PrinterService that implements the needed method for 
cotyledon.Service: run which contains the main loop, and terminate, which is 
called by another thread when it terminates the service.

Cotyledon uses several threads internally (at least to handle signals), which 
is why the threading.Event object is used to synchronize the run and terminate 
methods.

This service does not do much; it simply prints the message ‘Doing stuff’ every 
second. The service is started twice by passing two as the number of services 
to start to manager.add. That means Cotyledon starts two processes, each of them 
launching the PrinterService.run method.

When launching this program, you can run the ps (on Unix) and ps aux (on linux) 
command to see what is running. On the above application, open another terminal 
after running cotyledon-simple.py and enter the command ps aux to view the 
running processes.

Cotyledon runs a master process that is responsible for handling all of its 
children. It then starts the two instances of PrinterService as it was requested 
to launch. It also gives them nice shiny process names, making them easier to 
track in the long list of processes. If one of the processes gets killed or crashes, 
it is automatically relaunched by Cotyledon. The library does a lot behind the 
scenes, e.g., doing the os.fork calls and setting up the right modes for daemons.

Cotyledon also supports all operating systems supported by Python itself, 
freeing the developer from having to consider operating system portability, 
which can be quite complex.

The example provided above is a simple scenario for independent workers. They 
can execute a job on their own, and they do not need to communicate with each 
other. This scenario is rare, as most services need to communicate with one 
another.
"""
