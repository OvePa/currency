## Import other libraries if you want (asyncio and aiohttp are supported)
import time, requests
import asyncio

urls = ["http://educative.io", "http://educative.io/blog", "http://youtube.com"]


##########################################
### Start your code here
async def get_url(lst):
    for URL in urls:
        r = requests.get(url=URL)
        data = r.content
        # print(data)
        return data


start_time = time.time()

event_loop = asyncio.get_event_loop()
try:
    result = event_loop.run_until_complete(
        asyncio.gather(
            get_url(urls[0]),
            get_url(urls[1]),
            get_url(urls[2]),
        )
    )
    print(result)
finally:
    event_loop.close()

### End code here
##########################################
# print("Results: %s" % results)
print("--- %s milliseconds ---" % ((time.time() - start_time) * 1000))
