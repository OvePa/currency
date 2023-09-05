"""
Event loop in asyncio

Asyncio is centered on the concept of event loops, which work in the same way
as the select module. Once asyncio has created an event loop, an application
registers the functions to call back when a specific event happens: as time
passes, a file descriptor is ready to be read, or a socket is ready to be
written.

That type of function is called a coroutine. It is a particular type of function
that can give back control to the caller so that the event loop can continue
running. It works in the same manner that a generator would, giving back the
control to a caller using the yield statement.
"""
import asyncio


async def hello_world():
    print("hello world!")
    return 42


hello_world_coroutine = hello_world()
print(hello_world_coroutine)

event_loop = asyncio.get_event_loop()
try:
    print("entering event loop")
    result = event_loop.run_until_complete(hello_world_coroutine)
    print(result)
finally:
    event_loop.close()


"""
The above example shows a very straightforward implementation of an event loop 
using a coroutine. The coroutine hello_world is defined as a function, except 
that the keyword to start its definition is async def rather than just def. 
This coroutine just prints a message and returns a result.

The event loop runs this coroutine and is terminated as soon as the coroutine 
returns, ending the program. Coroutines can return values, and in this case, 
the value 42 is returned by the coroutine, which is then returned by the event 
loop itself.
"""
