"""
Partitioner

Now that you know how a hash ring works and how to manage group memberships, we
can start thinking about mixing the two.

On one side, we have a group system that can tell us which nodes in our
distributed system are live, and on the other side, we have an object that tells
us which node handles a piece of data. By updating the hash ring members using
the group system that Tooz offers, we can construct a new object called a
partitioned group.

Instead of building that into each application, Tooz provides an API that can
be leveraged while relying on both those mechanisms. The join_partitioned_group
method allows an application to join a group in which all members share some
workload using a consistent hash ring.
"""
import sys
import time
from tooz import coordination

# Check that a client and group ids are passed as arguments
if len(sys.argv) != 3:
    print("Usage: %s <client id> <group id>" % sys.argv[0])
    sys.exit(1)

# Get the Coordinator object
c = coordination.get_coordinator("etcd3://localhost", sys.argv[1].encode())
# Start it (initiate connection).
c.start(start_heart=True)

group = sys.argv[2].encode()

# Join the partitioned group
p = c.join_partitioned_group(group)

try:
    while True:
        print(p.members_for_object("foobar"))
        time.sleep(1)
finally:
    # Leave the group
    c.leave_group(group).get()

    # Stop when we're done
    c.stop()


"""
The Partitioner object provides a members_for_object which returns a set of members 
responsible for an object.

Note: To compute a unique byte identifier for a Python object, the Tooz partitioner 
calls the __tooz_hash__ method on the object passed as argument to members_for_object. 
If this method does not exist, the standard hash Python module is called instead. 
Having this method defined is important because each object must be uniquely but 
consistently identified across the cluster.

You can run the above example in parallel in different terminals.

Before running commands in other terminals, remember to change the directory 
first using cd examples/group-membership/.

You’ll see that they will join the same group, and output the same member id:

1234
$ python tooz-join-partitioned-group.py client1 test-group
{b'client1'}
$ python tooz-join-partitioned-group.py client2 test-group
{b'client2'}
Output of above example
That will obviously only work if both clients are connected at the same time 
and are part of the same group. If you run client2 alone, the output will be 
client2, as it is the only member of the group.

Note: In order to work correctly, the Tooz partitioner relies on the watchers 
(as seen in Section 8.3). Do not forget to regularly call tooz.coordination.
Coordinator.run_watchers so the hash ring of the partitioner is kept aware of 
members joining and leaving the partitioned group.
"""
