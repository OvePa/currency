"""
requests vs. aiohttp

Unless you are still using old versions of Python, without a doubt, using
aiohttp should be the way to go if you want to write a fast and asynchronous
HTTP client. It is the fastest and the most scalable solution, as it can handle
hundreds of parallel requests. The alternative, managing hundreds of threads in
parallel, is probably not a great option.

Another speed optimization that can be efficient is streaming the requests.
When making a request, by default, the body of the response is downloaded
immediately. The stream parameter provided by the requests library or the
content attribute for aiohttp both provide a way to not load the full content
in memory as soon as the request is executed.


"""
import requests


# Use `with` to make sure the response stream is closed and the connection can
# be returned back to the pool.
with requests.get("http://example.org", stream=True) as r:
    print(list(r.iter_content()))
