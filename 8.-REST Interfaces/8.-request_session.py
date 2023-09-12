"""
Fast HTTP Client

It is more than likely that you will have to write a client for your server
software, or that, at some point, your application will have to talk to another
HTTP server. The ubiquity of REST API makes their optimization patterns a
prerequisite nowadays.


"""
"""
requests
There are many HTTP clients in Python, but the most widely used and easy to work 
with is requests.

The first optimization to take into account is the use of a persistent connection
to the Web server. Persistent connections are a standard since HTTP 1.1, though 
many applications do not leverage them. This lack of optimization is simple to 
explain if you know that when using requests in its simple mode (e.g. with the 
get function) the connection is closed on return. To avoid that, an application 
needs to use a Session object that allows reusing an already opened connection.
"""
import requests

session = requests.Session()
session.get("http://example.com")
print("Connection made")
# Connection is re-used
session.get("http://example.com")
print("Connection reused")

"""
Each connection is stored in a pool of connections (10 by default), the size 
of which is also configurable,
"""
