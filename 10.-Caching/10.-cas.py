from pymemcache.client import base
import threading

threads = []


def on_visit():
    client = base.Client(("localhost", 11211))
    while True:
        result, cas = client.gets("visitors")
        if result is None:
            result = 1
        else:
            print("Storing: ", int(result.decode("utf-8")) + 1)
            result = int(result.decode("utf-8")) + 1
            if client.cas("visitors", result, cas):
                break
            client.cas("visitors", result, cas)


# Don't forget to run `memcached -u memache' before running
client = base.Client(("localhost", 11211))
client.flush_all()
client.set("visitors", 0)

for _ in range(50):
    t = threading.Thread(target=on_visit)
    t.daemon = True
    t.start()
    threads.append(t)

# join all threads
for t in threads:
    t.join()

print("Total visitors: ", client.get("visitors"))

"""
The gets method returns the value, just like the get method, but it also returns 
a CAS value. What is in this value is not relevant, but it is used for the next 
method cas call. This method is equivalent to the set operation, except that it 
fails if the value has changed since the gets operation. In case of success, 
the loop is broken. Otherwise, the operation is restarted from the beginning.

In the scenario where two instances of the application try to update the counter 
at the same time, only one succeeds to move the counter from 42 to 43. The 
second instance gets a False value returned by the client.cas call, and has to 
retry the loop. It will retrieve 43, as value this time, will increment it to 44, 
and its cas call will succeed, solving our problem.

Tip: Incrementing a counter is interesting as an example to explain how CAS works 
because it is simplistic. However, memcached also provides the incr and decr 
methods to increment or decrement an integer in a single request rather than doing 
multiple gets/cas calls. In real-world applications, gets and cas are used for 
more complex data types or operations.

Most remote caching servers and data stores provide such a mechanism to prevent 
concurrency issues. It is critical to be aware of those cases to make proper 
use of their features.
"""
