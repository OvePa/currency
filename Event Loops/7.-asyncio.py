"""
aiohttp

The aiohttp library provides an asynchronous HTTP. The example provided below
is a simple example of leveraging asyncio for concurrency.
"""
import aiohttp
import asyncio


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response


loop = asyncio.get_event_loop()
coroutines = [get("http://example.com") for _ in range(8)]
results = loop.run_until_complete(asyncio.gather(*coroutines))

print("Results: %s" % results)


"""
This example creates several coroutines, one for each call. Those coroutines are 
then gathered, and so they are executed concurrently by the event loop. If the 
remote web server is far away and needs a long delay to reply, the event loop 
switches to the next coroutine that is ready to be resumed, making sure the 
connections are ready to be read.
"""

"""
Note: The async with keyword used in the example above is equivalent to the 
await keyword, but it is specific to context managers that use await in their 
enter and exit methods.
"""
