import requests

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount("http://", adapter)
response = session.get("http://example.org")
print(response)

"""
Reusing the TCP connection to send out several HTTP requests offers a number of 
performance advantages:

Lower CPU and memory usage (fewer connections opened simultaneously).
Reduced latency in subsequent requests (no TCP handshaking).
Exceptions can be raised without the penalty of closing the TCP connection.
The HTTP protocol also provides pipelining, which allows sending several requests 
on the same connection without waiting for the replies to come (think batch). 
Unfortunately, this is not supported by the requests library. However, pipelining 
requests may not be as fast as sending them in parallel. Indeed, the HTTP 1.1 
protocol forces the replies to be sent in the same order as the requests were 
sent – FIFO (first-in-first-out).

requests also has one major drawback: it is synchronous. Calling 
requests.get(" http://example.org") blocks the program until the HTTP server 
replies completely. Having the application waiting and doing nothing can be a 
drawback here. It is possible that the program could do something else rather 
than sitting idle.
"""
