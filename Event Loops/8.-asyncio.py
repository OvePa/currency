"""
call_later

Asyncio also provides a way to call functions at a later time. Rather than
building a waiting loop with asyncio.sleep, the methods call_later and call_at
can be used to call functions at a relative or absolute future time respectively.
"""
import asyncio


def hello_world():
    print("Hello world!")


loop = asyncio.get_event_loop()
loop.call_later(1, hello_world)
loop.run_forever()

"""
The above example prints ”Hello world!” one second after starting and then 
blocks forever as the loop has nothing else to do.
"""
