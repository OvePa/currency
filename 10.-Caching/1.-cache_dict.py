cache = {}
cache["key"] = "value"
cache = {}


def compute_length_or_read_cache(s):
    try:
        return cache[s]
    except KeyError:
        cache[s] = len(s)
        return cache[s]


print("Foobar: ", compute_length_or_read_cache("foobar"))
print("Cache: ", cache)

print("Babaz: ", compute_length_or_read_cache("babaz"))
print("Cache: ", cache)

"""
Obviously, such a simple cache has a few drawbacks. First, its size is unbound, 
which means it can grow to a substantial size that can fill up the entire system 
memory. That would result in the death of either the process, or even the whole 
operating system in a worst-case scenario.

Therefore, a policy must be implemented to expire some items out of any cache, 
in order to be sure that the data store does not grow out of control. There are 
a few algorithms that can be found that are pretty simple to implement such as 
the following:

* Least recently used (LRU) removes the least recently used item first. 
  This means the last access time for each item must also be stored.
* Least Frequently Used (LFU) removes the least frequently used items first. 
  This means the number of accesses of each item must be stored.
* Time-to-live (TTL) based removes any entry that is older than a certain  
  period of time. This has the benefit of automatically invalidating the cache 
  after a certain amount of time, whereas the LRU and LFU policies are only 
  access-based.
  
Methods like LRU and LFU make more sense for memoization (see Memoization). 
Other methods, such as TTL, are more commonly used for a locally stored copy of 
remote data.
"""
