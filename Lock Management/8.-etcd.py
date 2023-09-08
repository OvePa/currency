"""
Introduction to etcd

etcd is a popular distributed key/value store. It stores keys and values and
replicates them on several nodes which can be used to query or update the keys.
To keep its members in sync, etcd implements the Raft algorithm. Raft solves the
consensus issue in distributed systems by electing a leader who is responsible
for maintaining consistency across nodes. In short, Raft makes sure that data
stored by etcd are consistent across all nodes, and that if a node crashes,
the etcd cluster can continue to operate until its failed node comes back to life.

In that regard, etcd allows implementing a distributed lock. The basic idea
behind the lock algorithm is to write some value in a predetermined key.
All the services in the cluster would pick, for example, the key lock1 and would
try to write the value acquired in it. As etcd supports transactions, this
operation would be executed in a transaction that would fail if the key already
existed. In that case, the lock would be unable to be acquired. If it succeeds,
the lock is acquired by the process that managed to create the key and write the value.

To release a lock, the client that acquired it just has to delete the key from etcd.

etcd is able to notify clients when a key is modified or deleted. Therefore,
any client that was unable to create the key (and acquire the lock) can be notified
as soon as the lock is released. Then it can try to acquire it.

If the client that acquired the lock crashes, the lock becomes impossible to
release. To avoid such cases, the keys have a time-to-live predefined at their
creation and need to be refreshed as long as the lock is kept acquired by the client.

This workflow is a basic locking algorithm and it is implementable with many
other key/value stores.
"""
