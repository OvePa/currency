"""
RQ provides several nifty features that can help tweaking your workloads,
such as specifying the time-to-live of the job itself (ttl option) or the
time-to-live of the result (ttl_result option). The queue name can also be
specified, making it easy to dispatch jobs to different queues.
"""

"""
NOTE: run the command <python 2.-rq_enqueue_params.py>. Then, open another 
terminal and enter the command <rq worker http>.
"""
import time

from rq import Queue
from redis import Redis
import requests

q = Queue(name="http", connection=Redis())

job = q.enqueue(requests.get, "http://httpbin.org/delay/1", ttl=60, result_ttl=300)
# While the URL is fetched, it's possible to do anything else.
# Wait until the result is ready.
while job.result is None:
    time.sleep(1)

print(job.result)

"""
Running the worker with a custom queue name is possible by passing the name as 
an argument via the command line.

The rq command line tool reveals information about the state of the queue. 
So, you can open another terminal in the above application and use the command 
<rq info> to get information about the state of the queue.
"""
"""
RQ dashboard
The cherry on the cake, the rq-dashboard package (available on PyPI) allows for 
visual feedback and gives some control over the queues as you can see in 
<rq-dashboard> by running the below-provided application. Once installed, 
simply run it by running the <rq-dashboard>, using arguments to point to the 
right Redis instance as needed. It is then available on port 9181 by default, 
but you can customize the port on which you want it to run.
"""
