"""
Picking the right distributed lock mechanism once and for all for your application
is not necessarily an obvious choice. Consider these factors:

First, some solutions are heavier than others to deploy and maintain. For example,
installing a memcached server is pretty straightforward, but maintaining a
ZooKeeper cluster is much more complicated. Clearly, the two solutions are not
strictly equivalent in terms of safety and guaranteed operation. However, as a
developer, it might be handy to test using a small backend and operate at scale
with a scalable backend.

Secondly, it is not always obvious which solution to pick. A few years ago,
ZooKeeper was the hot thing and the only widely available implementation of the
Paxos algorithm. Nowadays, solutions such as etcd and its Raft implementation
are getting more traction: the algorithm is simpler to understand and the project
is less complicated to deploy and operate.

All those backends offer different levels of abstraction on top of distributed
features. Some projects provide a full locking implementation whereas some others
are only key/value stores.
"""

"""
tooz library
The Tooz library was created a few years ago to solve those problems. It 
provides an abstraction on top of a varied set of backends, making it easy to 
switch from one service to another. This can be quite powerful, as it allows 
you to use memcached to test your distributed code on your laptop, for example, 
as it is lightweight to run and install, while you can also support something 
like a ZooKeeper cluster as a more robust solution. Moreover, whatever backend 
you pick, the distributed features that you need, such as locking, are provided 
using the same API for your application, whatever primitives provided by the 
underlying service.

To achieve that, Tooz provides a < Coordinator > object that represents the 
coordination service your application is connected to. The method 
< tooz.coordinator.get_coordinator > allows the program to get a new coordinator. 
All it needs is the URL to connect to and a unique identifier for the node, 
as you can see in the following example.
"""
import uuid
from tooz import coordination

# Generate a random unique identifier using UUID
identifier = str(uuid.uuid4())

# Get the Coordinator object
c = coordination.get_coordinator("etcd3://localhost", identifier)

# Start it (initiate connection)
c.start(start_heart=True)

# Stop when we're done
c.stop()
print("Done")


"""
The basic operations on a coordinator are pretty simple. Once instantiated, 
one just needs to start it and stop it when the program is done.
"""
