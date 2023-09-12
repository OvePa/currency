"""
request-futures
This pattern being quite useful, it has been packaged into a library named
requests-futures. As you can see in the following example, the usage of Session
objects is made transparent to the developer.


"""
from requests_futures import sessions

session = sessions.FuturesSession()

futures = [session.get("http://example.org") for _ in range(8)]

results = [f.result().status_code for f in futures]

print("Results: %s" % results)

"""
By default, a worker with two threads is created, but a program can easily 
customize this value by passing the max_workers argument or even its own executor 
to the FuturesSession object, for example like this: 
FuturesSession(executor=ThreadP oolExecutor(max_workers=10)).

As explained earlier, requests are entirely synchronous. That makes the 
application being blocked while waiting for the server to reply, slowing down 
the program. Making HTTP requests in threads is one solution, but threads do 
have their own overhead and this implies concurrency, which is not something 
everyone is always glad to see in a program.
"""
