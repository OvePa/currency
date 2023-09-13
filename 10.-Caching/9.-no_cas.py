"""
CAS
When communicating with a remote cache, the usual concurrency problem comes back:
there might be several clients trying to access the same key at the same time.
memcached provides a check and set operation, shortened to CAS, which helps to
solve this problem.

The simplest example is an application that wants to count the number of users
it has. Each time a visitor connects, a counter is incremented by 1. Using
memcached, a simple implementation is provided in the example below.
"""
from pymemcache.client import base
import threading

threads = []


def on_visit():
    client = base.Client(("localhost", 11211))
    result = client.get("visitors")
    if result is None:
        result = 1
    else:
        print("Storing: ", int(result.decode("utf-8")) + 1)
        result = int(result.decode("utf-8")) + 1
    client.set("visitors", result)


# Don't forget to run `memcached' before running
client = base.Client(("localhost", 11211))
client.flush_all()

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
In the following application, click Run and open another terminal. Enter the 
command memcached -u memcache. In the first terminal, enter command python 
no-cas.py.
"""
"""
In the above example, notice that some threads try to store the same value into 
memcache. Theoretically, all threads should store an incremented value.

What happens is if two instances of the application try to update this counter 
at the same time? The first call client.get("visitors") will return the same 
number of visitors for both of them. Let’s say it’s 42. Then both will add 1, 
compute 43, and set the number of visitors to 43. That number is wrong, and the 
result should be 44, i.e. 42 + 1 + 1.
"""
