"""
Using Watchers Callbacks

When a member joins or leaves a group, applications usually want to run an
action. There is a mechanism provided by Tooz to help with the named watchers.
It works by caching a list of the members and running the specified callback
functions each time a member joins or leaves the group.

To use those callbacks, Tooz provides the watch_join_group and watch_leave_group
methods to register functions to call on join or leave events. If you ever need
to un-register a callback, unwatch_join_group and unwatch_leave_group provide
this functionality.

Once the callback functions are registered, they are only run when the
run_watcher method is called. If your application is thread-safe, you can run
this method regularly in a different thread. If not, you should call it in any
loop your program provides.

Join and leave callbacks using Tooz

The following example provides an example of an application joining a group and
checking when a member joins or leaves that group. As soon as this happens and
that run_watchers is executed, it prints which member joined or left which group.
"""
import sys
import time
from tooz import coordination

# Check that a client and group ids are passed as arguments
if len(sys.argv) != 3:
    print("Usage: %s <client id> <group id>" % sys.argv[0])
    sys.exit(1)

# Get the Coordinator object
c = coordination.get_coordinator(
    # Set a short timeout to see effects faster
    "etcd3://localhost/?timeout=3",
    sys.argv[1].encode(),
)
# Start it (initiate connection).
c.start(start_heart=True)

group = sys.argv[2].encode()

# Create the group
try:
    c.create_group(group).get()
except coordination.GroupAlreadyExist:
    pass

# Join the group
c.join_group(group).get()

# Register the print function on group join/leave
c.watch_join_group(group, print)
c.watch_leave_group(group, print)

while True:
    c.run_watchers()
    time.sleep(1)

# Leave the group
c.leave_group(group).get()

# Stop when we're done
c.stop()

"""
As soon as Ctrl+c is pressed to interrupt the program, it loses its connection 
to etcd, and its keys will expire after the configured timeout. You can see the 
configured timeout as being passed in the connection URL as < ?timeout= >.

Using Ctrl+c to interrupt the program simulates a crash or a violent interruption, 
and you can see that this system is pretty robust in this regard. Obviously, the 
program would also be notified of the member leaving the group if it would have 
called the < leave_group > method.

This feature allows following all members joining and leaving a distributed system, 
and it is very handy in higher-level applications, as discussed in Partitioner 
lesson.
"""
