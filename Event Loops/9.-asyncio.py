import asyncio

loop = asyncio.get_event_loop()


def hello_world():
    loop.call_later(1, hello_world)
    print("Hello world!")


loop = asyncio.get_event_loop()
loop.call_later(1, hello_world)
loop.run_forever()

"""
The above example provides a hello_world function that leverages the call_later 
method to reschedule itself every second.

Asyncio is excellent at handling network-related tasks. Its event loop can handle 
thousands of concurrent sockets. Therefore, connection switches to the one that 
is ready to be processed as soon as possible. This happens as long as your 
program regularly yields back control to the event loop using the await keyword. 
It obviously means programs need to use code and libraries that are asyncio 
compatible, which are not always widely available for all sorts of things.
"""
