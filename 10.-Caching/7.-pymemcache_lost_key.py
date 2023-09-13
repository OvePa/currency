from pymemcache.client import base


def do_some_query():
    # Replace with actual querying code to a database, a remote REST API, etc.
    return 42


# Don't forget to run `memcached' before running
client = base.Client(("localhost", 11211))
result = client.get("some_key")
if result is None:
    # The cache is empty, need to get the value from the canonical source
    result = do_some_query()
    # Cache the result for next time
    client.set("some_key", result)
print(result)
