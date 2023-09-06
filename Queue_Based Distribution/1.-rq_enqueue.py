"""
Note: To run the following application, click Run and run the command python
<1.-rq_enqueue.py>. Nothing will be processed as of yet. You need to start the
worker to start processing. For this, open another terminal and enter the
command <rq worker>.
"""

import time
from rq import Queue
from redis import Redis

q = Queue(connection=Redis())

job = q.enqueue(sum, [42, 43])
# Wait until the result is ready --
while job.result is None:
    time.sleep(1)

print(job.result)

"""
When starting the program in the example above, a job whose actual work is to 
execute sum([42, 43]) is pushed into a queue. However, for now, nothing is 
processing the queue, so the program waits forever, sleeping one second.

To start consuming those events, RQ provides an rq command line tool that is 
responsible for initiating a worker.

Once the rq worker command is run, the function to be executed, its universally 
unique identifier (UUID), and the status of the job execution are displayed.

In the code above, rq indicates the result of the job is put back into the queue 
for 500 seconds. Redis supports setting values with a specific lifespan, or 
time-to-live, meaning that after 500 seconds Redis will destroy the result.
"""
"""
Warning

To pass jobs around, rq serializes the jobs using pickle, a Python specific 
serialization format. That implies several things:

-> The Python version must be the same on both producers and workers.

-> The code version must be the same on both producers and workers, and both 
    must have the same version of the code so they can import the same module.

-> It is close to impossible to have producers and workers using any language 
    other than Python.
"""
