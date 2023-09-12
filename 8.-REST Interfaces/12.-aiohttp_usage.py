"""
Asynchronicity using asyncio
Starting with version 3.5, Python offers asynchronicity as its core using asyncio.
The aiohttp library provides an asynchronous HTTP client built on top of asyncio.
This library allows sending requests in series but without waiting for the first
reply to come back before sending the new one. In contrast to HTTP pipelining,
aiohttp sends the requests over multiple connections in parallel, avoiding the
ordering issue explained earlier.
"""
import aiohttp
import asyncio


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.content.read()


loop = asyncio.get_event_loop()
coroutines = [get("http://example.com") for _ in range(8)]
results = loop.run_until_complete(asyncio.gather(*coroutines))

print("Results: %s" % results)
