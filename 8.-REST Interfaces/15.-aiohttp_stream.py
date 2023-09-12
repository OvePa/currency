"""
The asyncio module is used to keep track of the responses, and results are
printed once all responses are available.
"""
import aiohttp
import asyncio


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.content.read()


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(get("http://example.com"))]
loop.run_until_complete(asyncio.wait(tasks))
print("Results: %s" % [task.result() for task in tasks])


"""
Not loading the full content is extremely important in order to avoid allocating 
potentially hundreds of megabytes of memory for nothing. If your program does 
not need to access the entire content as a whole but can work on chunks, it is 
probably better to just use those methods.
"""
