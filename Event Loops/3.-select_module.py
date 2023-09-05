"""
The select module
The simplest mechanism to make the code do something else rather than actively
waiting is to use the select module in Python. This module provides
select.select(rlist, wlist, xlist) function that takes any number of sockets
(or file descriptors) as input and returns the ones that are ready to read,
write or have errors.


"""
import select
import socket

s = socket.create_connection(("httpbin.org", 80))
s.setblocking(False)
s.send(b"GET /delay/1 HTTP/1.1\r\nHost: httpbin.org\r\n\r\n")
while True:
    ready_to_read, ready_to_write, in_error = select.select([s], [], [])
    if s in ready_to_read:
        buf = s.recv(1024)
        print(buf)
        break


"""
In the above example, the socket is passed as an argument in the list of 
descriptors we want to watch for read-readiness. As soon as the socket has data 
available to read, the program can read them without blocking.

If you combine multiple sources of events in a select call, it is easy to see 
how your program can become event-driven. The select loop becomes the main 
control flow of the program, and everything revolves around it. As soon as some 
file descriptor or socket is available for reading or writing, it is possible to 
continue operating on it.

This kind of mechanism is at the heart of any program that wants to handle, for 
example, thousands of connections at once. It is the base technology leveraged 
by tools such as really fast HTTP servers like NGINX or Node.js.

select is an old but generic system call, and it is not the highest performing 
out there. Different operating systems implement various alternatives and 
optimizations, such as epoll in Linux or kqueue in FreeBSD. As Python is a 
high-level language, it implements and provides an abstraction layer known as 
asyncio.
"""
