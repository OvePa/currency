import socket

s = socket.create_connection(("httpbin.org", 80))
s.setblocking(False)
s.send(b"GET /delay/5 HTTP/1.1\r\nHost: httpbin.org\r\n\r\n")
buf = s.recv(1024)
print(buf)


"""
Running the above example will fail with an interesting error: BlockingIOError: 
[Errno 35] Resource temporarily unavailable.

As the socket does not have any data to be read, rather than blocking (until it 
has the data), Python raises a BlockingIOError, asking the caller to retry at a 
later time.

At this point, you can see where this is going. If the program can get a message 
as soon as the socket is ready to be handled, the code can do something else 
rather than actively waiting.


"""
