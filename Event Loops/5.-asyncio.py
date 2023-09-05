"""
Run coroutine cooperatively
Coroutines can cooperate. This is why they are named coroutines after all.
You can, therefore, call a coroutine from a coroutine.
"""
import asyncio


async def add_42(number):
    print("Adding 42")
    return 42 + number


async def hello_world():
    print("hello world!")
    result = await add_42(23)
    return result


event_loop = asyncio.get_event_loop()
try:
    result = event_loop.run_until_complete(hello_world())
    print(result)
finally:
    event_loop.close()

"""
The await keyword is used to run the coroutine cooperatively. await gives the 
control back to the event loop, registering the coroutine add_42(23) into it. 
The event loop can, therefore, schedule whatever it needs to run. In this case, 
only add_42(23) is ready and waiting to be executed: therefore it is one that 
gets executed. Once finished, the execution of the hello_world coroutine can be 
resumed by the event loop scheduler.

The examples thus far have been pretty straightforward, and it is easy to guess 
in which order the various coroutines are executed. Those programs were barely 
leveraging event loop scheduling.


"""
