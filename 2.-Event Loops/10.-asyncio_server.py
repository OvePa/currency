"""
Asyncio server

Following is a simple example of a TCP server. This server listens for strings
terminated by \n and returns them in upper case.
"""
import asyncio

SERVER_ADDRESS = ("0.0.0.0", 1234)


class YellEchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print("Connection received from:", transport.get_extra_info("peername"))

    def data_received(self, data):
        self.transport.write(data.upper())

    def connection_lost(self, exc):
        print("Client disconnected")


event_loop = asyncio.get_event_loop()

factory = event_loop.create_server(YellEchoServer, *SERVER_ADDRESS)
server = event_loop.run_until_complete(factory)

try:
    event_loop.run_forever()
    print("Server started")
finally:
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    event_loop.close()


"""
To implement a server, the first step is to define a class that inherits from 
asyncio.Protocol. It is not strictly necessary to inherit from this class, but 
it is a good idea to get all the basic methods defined – even if they do nothing.

The connection_made(transport) method is called as soon as a connection is 
established by a client. An asyncio.BaseTransport object is passed as the 
argument, which represents the underlying socket and stream with the client. 
This object offers several methods such as get_extra_info to get more information 
on the client, or close method, to close the transport. The connection_lost is 
the other end of the connection handling code. It is called when the connection 
is terminated. Both connection_made and connection_lost are called once per connection.

The data_received method is called each time some data is received. It might 
never be called if no data is ever received. The eof_received method might be 
called once if the client sends an EOF signal.
"""

"""
The simplest way to test the above example is to use the netcat program, 
available as the nc command on most versions of Unix.

In the above application, after running the server, open another terminal and 
enter the command nc localhost 1234 to start communication with the server. 
Once the connection is made, enter lowercase character strings, press enter to 
send, and the server will return the same string in uppercase.

Typing any text followed by \n returns it in upper case. Sending EOF by pressing 
Control+d closes the connection.
"""
