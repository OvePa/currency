import asyncio

SERVER_ADDRESS = ("0.0.0.0", 1234)


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def talk(self):
        self.transport.write(self.message)

    def connection_made(self, transport):
        self.transport = transport
        self.talk()

    def data_received(self, data):
        self.talk()

    def connection_lost(self, exc):
        self.loop.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(
    loop.create_connection(
        lambda: EchoClientProtocol(b"Hello World!", loop), *SERVER_ADDRESS
    )
)
try:
    loop.run_forever()
finally:
    loop.close()

"""
In the above example, basic statistics are stored, computed, and printed at the 
end of the program.

While running it on my laptop with five clients at the same time, the asyncio 
server is able to handle more than 23,000 messages per second. Obviously, this 
server is not doing much work – upper-casing a string is not that impressive – 
but this is still a pretty decent result. Keep in mind that this server is not 
using any thread or any extra processes, so it is only using one single CPU.

Asyncio is a transcendent solution to write asynchronous network clients and 
servers. The protocol implementation is straightforward, and the ability to mix 
all kinds of asynchronous workload makes the framework powerful.
"""
