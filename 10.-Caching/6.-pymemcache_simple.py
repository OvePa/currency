from pymemcache.client import base

# Don't forget to run `memcached' before running
client = base.Client(("localhost", 11211))
client.set("some_key", "some_value")
result = client.get("some_key")
print(result)  # some_value

"""
To run the following application, click Run and open another terminal to start 
memcached using command: memcached -u memcache -p 11211. Then, enter the command 
python pymemcache-simple.py in the first terminal.
"""
