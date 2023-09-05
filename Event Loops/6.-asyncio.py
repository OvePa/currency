"""
sleep and gather

The example given below introduces two new functions:

-> asyncio.sleep is the asynchronous implementation of time.sleep. It is a
   coroutine that sleeps some number of seconds. Since it is a coroutine and not
   a function, it can be used to yield back the control to the event loop.

-> asyncio.gather allows you to wait for several coroutines at once using a
   single await keyword. Rather than using several sequential await keywords,
   this allows explicitly stating to the scheduler that all the results of those
   operations are needed to continue the execution of the program. It ensures
   that the event loop executes those coroutines concurrently.
"""
import asyncio


async def hello_world():
    print("hello world!")


async def hello_python():
    print("hello Python!")
    await asyncio.sleep(0.1)


event_loop = asyncio.get_event_loop()
try:
    result = event_loop.run_until_complete(
        asyncio.gather(
            hello_world(),
            hello_python(),
        )
    )
    print(result)
finally:
    event_loop.close()

"""
In the above example, both the hello_world and hello_python coroutines are 
executed concurrently. If the event loop scheduler starts with hello_world, 
it will be able to continue only afterwards with hello_python. hello_python will 
then inform the scheduler that it needs to wait for the asyncio.sleep(0.1) 
coroutine to complete. The scheduler will execute this coroutine, which takes 
into account a 0.1 second delay before giving back the execution to hello_python. 
Once it does that, the coroutine is finished, terminating the event loop.

Contrary to the classic time.sleep function, which makes Python sleep synchronously 
and blocks it while it waits, asyncio.sleep can be handled asynchronously. 
So Python can do something else while it waits for the specified delay to pass.

In the case where hello_python is the first coroutine to run, the execution of 
hello_world only starts after that the await asyncio.sleep(0.1) coroutine is 
yielded back to the event loop. Then the rest of the event loop continues its 
execution and terminates.
"""
