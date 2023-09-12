"""
Using with
"""
import uuid

from tooz import coordination

# Generate a random unique identifier using UUID
identifier = str(uuid.uuid4())

# Get the Coordinator object
c = coordination.get_coordinator("etcd3://localhost", identifier)

# Start it (initiate connection)
c.start(start_heart=True)

lock = c.get_lock(b"foobar")

with lock:
    print("do something")


"""
Unless you are certain about the backend that your application needs, using an 
abstraction layer such as Tooz can be a great solution. This is especially true 
for some of the backends that Tooz supports such as PostgreSQL or memcached, 
for example, as there are no other Python libraries implementing a locking 
mechanism in contrast to etcd or ZooKeeper.
"""
