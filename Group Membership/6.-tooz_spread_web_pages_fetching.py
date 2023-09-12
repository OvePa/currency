"""
Using partitioner to fetch webpages

This mechanism is quite powerful and can solve some problems.

For example, you can automatically divide up the workload across several nodes.
Imagine you have 100 URLs to continuously fetch from the Web. You can spread
that workload pretty easily using this mechanism.
"""
import itertools
import uuid
import requests
from tooz import coordination


class URL(str):
    def __tooz_hash__(self):
        # The unique identifier is the URL itself
        return self.encode()


urls_to_fetch = [
    # Return N bytes where the number of bytes
    # is the number at the end of the URL
    URL("https://httpbin.org/bytes/%d" % n)
    for n in range(100)
]

GROUP_NAME = b"fetcher"
MEMBER_ID = str(uuid.uuid4()).encode("ascii")

# Get the Coordinator object
c = coordination.get_coordinator("etcd3://localhost", MEMBER_ID)
# Start it (initiate connection)
c.start(start_heart=True)

# Join the partitioned group
p = c.join_partitioned_group(GROUP_NAME)

try:
    for url in itertools.cycle(urls_to_fetch):
        # Be sure no membership changed
        c.run_watchers()
        # print("%s -> %s" % (url, p.members_for_object(url)))
        if p.belongs_to_self(url):
            try:
                r = requests.get(url)
            except Exception:
                # IF an error occur, just move on
                # to the next item
                pass
            else:
                print("%s: fetched %s (%d)" % (MEMBER_ID, r.url, r.status_code))
finally:
    # Leave the group
    c.leave_group(GROUP_NAME).get()

    # Stop when we're done
    c.stop()


"""
Running multiple fetching programs
As soon as a second instance of the program starts and joins the hash ring, the 
first instance of the program starts skipping some of the pages. Those skipped 
pages are fetched by the other running program as you can see in the output of 
the following example.

In the above application, run another webpage fetching program in another terminal 
(using python tooz-spread-web-page-fetching.py) 

As soon as a member joins the group, the members spread the URLs to fetch between 
them using the hash ring. Therefore, it all goes twice as fast as before.

Of course, this kind of mechanism does not fit every workload. Non-cyclic 
workloads which need a queue are still better handled by queue mechanism as 
discussed in Queue-Based Distribution. However, it is easy to imagine using that 
mechanism to distribute the consumption of multiple queues across workers.
"""
