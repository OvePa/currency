"""
Consistent Hash Rings

Being able to manage distributed groups enables the utilization of several
distributed algorithms. One of them is named consistent hash rings.

A traditional way to spread keys across a distributed system, which is composed
of n nodes, is to compute which node should be responsible for a key by using:
< hash( object) % n >. Unfortunately, as soon as n changes, the result of the modulo
operation changes and therefore all keys are remapped to a new node. This
remapping causes a massive shuffling of data or processing in a cluster.

The point of consistent hashing is to avoid that. By using a different method
of computing, when n changes, only K /n of the keys are remapped to the remaining
nodes, where K is the number of keys and n the number of nodes handling those keys.

The hash ring

A hash ring is a hashing space that wraps around itself to form a circle.
That’s why it is called a ring. Every key computed using the consistent hashing
function maps somewhere on this hash space. That means that a key is always in
the same place on the ring. The ring is then split into P partitions, where P
is a magnitude larger than the number of nodes (a lot more partitions than the
nodes). Each node is then responsible for 1/n partitions of the ring.

This implementation also has the upside of making it easy to add a replication
mechanism, meaning a set of keys managed by more than just one node.
Replication is handy in case of the failure of a node, as the keys are still
managed/stored by another node.

"""
# -*- encoding: utf-8 -*-
from tooz import hashring

NUMBER_OF_NODES = 16

# Step #1 – create a hash ring with 16 nodes
hr = hashring.HashRing(["node%d" % i for i in range(NUMBER_OF_NODES)])
nodes = hr.get_nodes(b"some data")
print(nodes)
nodes = hr.get_nodes(b"some data", replicas=2)
print(nodes)
nodes = hr.get_nodes(b"some other data", replicas=3)
print(nodes)
nodes = hr.get_nodes(b"some other of my data", replicas=2)
print(nodes)

# Step #2 – remove a node
print("Removing node8")
hr.remove_node("node8")
nodes = hr.get_nodes(b"some data")
print(nodes)
nodes = hr.get_nodes(b"some data", replicas=2)
print(nodes)
nodes = hr.get_nodes(b"some other data", replicas=3)
print(nodes)
nodes = hr.get_nodes(b"some other of my data", replicas=2)
print(nodes)

# Step #3 – add a new node
print("Adding node17")
hr.add_node("node17")
nodes = hr.get_nodes(b"some data")
print(nodes)
nodes = hr.get_nodes(b"some data", replicas=2)
print(nodes)
nodes = hr.get_nodes(b"some other data", replicas=3)
print(nodes)
nodes = hr.get_nodes(b"some other of my data", replicas=2)
print(nodes)
nodes = hr.get_nodes(b"some data that should end on node17", replicas=2)
print(nodes)

# Step #4 – add back a node with a greater weight
print("Adding back node8 with weight")
hr.add_node("node8", weight=100)
nodes = hr.get_nodes(b"some data")
print(nodes)
nodes = hr.get_nodes(b"some data", replicas=2)
print(nodes)
nodes = hr.get_nodes(b"some other data", replicas=3)
print(nodes)
nodes = hr.get_nodes(b"some other of my data", replicas=2)
print(nodes)
"""
Creating hash ring
Step 1:
The first step of this example demonstrates how to create a hash ring. The 
hashring created has 16 initial nodes, named node1 to node16.

Once the hash ring is created, the main method for using it is get_nodes. It 
expects bytes as input. It is up to the application developer to come up with 
a chain of bytes that makes sense in his application. It could be a simple key 
or a stringified version of an object or its hash.

The return value of get_nodes is a set of nodes that are responsible for handling 
this piece of data. By default, only one node is returned, but the method also 
accepts a number of replicas as an argument. In this case, the returned set will 
contain R more nodes, where R is the number of replicas.

Removing a node
Step 2:
The second step of the example removes a node from the hash ring. At this stage, 
there are only 15 nodes in this ring. The get_nodes calls are identical to 
step 1, but as you can see, the output is quite different. Since we removed 
node8 from the hash ring, the partitions that it managed are now handled by the 
nodes managing the adjacent partitions in the ring.

For the first key, node8 is replaced by node11. For the second key, node6 is used 
instead. There is no change for the third key as node8 was not a replica. Finally, 
node5 is picked for the last key instead of the missing node8.

As you can see, the promise of the hash ring is kept. One node has been removed, 
but only some of the keys were remapped - exclusively the ones being assigned to 
the removed node.

Adding a new node
Step 3:
The third step adds a new node called node17 to the ring. Once again, the promise 
is kept, and no re-balancing of the key we previously showed was done. To show 
that the node17 was indeed responsible for some partitions, I have added a 
get_node with a byte string where a replica is node17 (as there is no way to 
know in advance where a key will end up, I have just edited the key until the 
returned node would be node17).

Adding back a node with a greater weight
Step 4:
In the last step, node8 is added back to the hash ring, but this time with a 
weight of 100, which means it will be responsible for up to 100 times more keys 
than the other nodes. As the hash ring is deterministic, the keys that node8 was 
responsible for before being removed are returned to it. That means the key some 
data causes node6 to be replaced by node8, in the same spot it was at the beginning 
of the program. Since the weight is 100, that also means that this time node8 
will get a lot more keys than the others. That is why you may notice that node8 
is now one of the replicas of the keys or some other data instead of node13.

Hash rings are very convenient though they are not perfect. For one, the 
distribution of keys is not uniform, and some nodes will be responsible for more 
keys than others. This might or might not be a problem depending on your 
application.
"""
