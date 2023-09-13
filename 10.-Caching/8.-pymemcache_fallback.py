from pymemcache.client import base
from pymemcache import fallback


def do_some_query():
    # Replace with actual querying code to a database, a remote REST API, etc.
    return 42


# Set `ignore_exc=True` so it is possible to shut down the old cache before
# removing its usage from the program, if ever necessary.
old_cache = base.Client(("localhost", 11211), ignore_exc=True)
new_cache = base.Client(("localhost", 11212))

client = fallback.FallbackClient((new_cache, old_cache))

result = client.get("some_key")
if result is None:
    # The cache is empty, need to get the value from the canonical source
    result = do_some_query()
    # Cache the result for next time
    client.set("some_key", result)
print(result)


"""
To run the following application, click on the Run button and open another 
terminal to start memcached using command: memcached -u memcache -p 11212 
Open yet another terminal to start another memcached instance on port 11211 by 
using command memcached -u memcache -p 11211. Then, enter the command python 
pymemcache-fallback.py in the first terminal.
"""
"""
The FallbackClient queries the old cache passed to its constructor, respecting 
the order. In this case, the new cache server will always be queried first, and 
in case of a cache miss, the old one will be queried, avoiding a possible 
return-trip to the primary source of data. If any key is set, it will only be 
set to the new cache. After some time, the old cache can be decommissioned and 
the FallbackClient can be replaced directly with the new_cache client.
"""
