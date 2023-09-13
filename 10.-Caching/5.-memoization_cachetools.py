"""
Using cachetools for memoization
If an older version of Python is used, or if a different algorithm is desired,
the cachetools package, as seen previously, provides a useful cachetools module
that can be imported with a wide variety of cache types as shown in the below
example.
"""
import cachetools.func
import math
import time

memoized_sin = cachetools.func.ttl_cache(ttl=5)(math.sin)

print("memoized_sin(3): ", memoized_sin(3))
print("Cache info: ", memoized_sin.cache_info())

print("memoized_sin(3): ", memoized_sin(3))
print("Cache info: ", memoized_sin.cache_info())

time.sleep(5)
print("Cache info after 5 seconds: ", memoized_sin.cache_info())
