"""
The following example shows a simple program that sends an HTTP request to
http://httpbin.org/delay/5. The URL returns a JSON content after five seconds
of delay.

As expected, when this program runs, it takes at least five seconds to complete:
the socket.recv call hangs until the remote Web server sends the reply.

This is the kind of situation that should be avoided: waiting for an input or
output to complete before going on, as the program could be doing something else
rather than waiting.
"""
import socket

s = socket.create_connection(("httpbin.org", 80))
s.send(b"GET /delay/5 HTTP/1.1\r\nHost: httpbin.org\r\n\r\n")
buf = s.recv(1024)
print(buf)
