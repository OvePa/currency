"""
Asyncio client

The same asyncio.Protocol class can be used to implement a client.
"""
# This works with 10.-asyncio_server
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
The client in the above example connects to the YellEchoServer. Once connected, 
connection_made is called and the client sends its message via its talk method. 
The server replies back with that text in uppercase, and the data_received is 
called. In this case, the client talks again to the server, creating an infinite 
loop of interaction between the two.
"""
