"""
Comparison Between Fast HTTP Clients

serialized vs. sessions vs. aiohttp
All HTTP client solutions (using sessions, threads, futures or asyncio) offer
different approaches to making HTTP clients faster.

The following example is an HTTP client sending requests to httpbin.org, an
HTTP API that provides (among other things) an endpoint simulating a long
request (a second here). This example implements all the techniques listed above
and times them.
"""
import contextlib
import time
import aiohttp
import asyncio
import requests
from requests_futures import sessions

URL = "https://httpbin.org/delay/1"
TRIES = 10


@contextlib.contextmanager
def report_time(test):
    t0 = time.time()
    yield
    print("Time needed for `%s' called: %.2fs" % (test, time.time() - t0))


with report_time("serialized"):
    for i in range(TRIES):
        requests.get(URL)

session = requests.Session()
with report_time("Session"):
    for i in range(TRIES):
        session.get(URL)

session = sessions.FuturesSession(max_workers=2)
with report_time("FuturesSession w/ 2 workers"):
    futures = [session.get(URL) for i in range(TRIES)]
    for f in futures:
        f.result()

session = sessions.FuturesSession(max_workers=TRIES)
with report_time("FuturesSession w/ max workers"):
    futures = [session.get(URL) for i in range(TRIES)]
    for f in futures:
        f.result()


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            await response.read()


loop = asyncio.get_event_loop()
with report_time("aiohttp"):
    loop.run_until_complete(asyncio.gather(*[get(URL) for i in range(TRIES)]))

"""
Unsurprisingly, the slower result comes with the dumb serialized version, since 
all the requests are made one after another without reusing the connection.

Using a Session object and therefore reusing the connection means saving 8% in 
terms of time, which is already a big and easy win. Minimally, you should always 
use a session.



Note: Most likely, the serialized version is the slowest. But it is possible that 
when you run the program, the session method turns out to be the slowest. This 
could be due to variable delays in the network. The Serialized method itself is 
the slowest.

If your system and program allow the use of threads, it is a good idea to use 
them to parallelize the requests. However, threads have some overhead, and they 
are not weightless. They need to be created, started, and then joined, which 
does not make them much faster.
"""
