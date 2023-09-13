import functools
import math


@functools.lru_cache(maxsize=2)
def memoized_sin(x):
    return math.sin(x)


print("memoized_sin(2): ", memoized_sin(2))
print("Cache info: ", memoized_sin.cache_info())

print("memoized_sin(2): ", memoized_sin(2))
print("Cache info: ", memoized_sin.cache_info())

print("memoized_sin(3): ", memoized_sin(3))
print("Cache info: ", memoized_sin.cache_info())

print("memoized_sin(4): ", memoized_sin(4))
print("Cache info: ", memoized_sin.cache_info())

print("memoized_sin(3): ", memoized_sin(3))
print("Cache info: ", memoized_sin.cache_info())

memoized_sin.cache_clear()

print("Cache info: ", memoized_sin.cache_info())
