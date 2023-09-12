"""
Streaming Data

A common pattern with any HTTP API is the need to receive events. In a lot of
cases, there is no way to achieve this other than regularly polling the API.
That can cause a lot of stress on the HTTP endpoint, as it requires setting up
a new connection, which means a lot of overload with TCP and SSL.

Streaming basics
A more efficient way is to use streaming. An adequate technology here is
ServerSent Events message protocol defined by HTML5. Alternatively, it would be
possible to use Transfer-Encoding:chunked defined by HTTP/1.1 or even the
WebSocket protocol. However, chunked encoding is more complicated, and the
WebSocket is a little bit overkill for the simple use case presented here.

To implement any streaming mechanism in a scalable and efficient manner, you
need to be sure that your backend offers that feature. It could be a messaging
queue, a database or any other software that provides a stream of events that
the application can subscribe to.

If the offered API has to poll its backend regularly to know about new events,
it is simply moving the problem from one layer to another. It is better than
nothing, but it is far from ideal.

Redis Pub/Sub mechanism
The example illustrated in this lesson is a small application that stores
messages in Redis and provides access to those messages via an HTTP REST API.
Each message consists of a channel number, a source string, and a content string.
The backend used in the examples in this lesson is Redis, as it provides a
notification mechanism that is close to what a message queue could offer.

The goal is to stream these messages to the client so it can process them in
real time on its side. To do this, we are going to use the Redis Pub/Sub mechanism
provided by the PUBLISH and SUBSCRIBE commands.

These features allow us to subscribe and receive messages sent by other processes.
"""
import redis

r = redis.Redis()
p = r.pubsub()
p.subscribe("chatroom")
for message in p.listen():
    print(message)


"""
The above example shows how to publish a message to a channel. The publish 
method sends the message to the channel passed as the first argument. The 
second argument is a string carrying the actual payload.

It is possible to check that the trigger works by using the SUBSCRIBE command. 
If everything is OK, it receives a notification as soon as the PUBLISH command 
is executed.


"""
