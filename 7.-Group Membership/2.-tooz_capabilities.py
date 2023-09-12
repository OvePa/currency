"""
Using Capabilities

Tooz provides a capability mechanism on top of the group feature. When joining
a group, a member can specify what its capabilities are. It can also update
them later as needed.

Capabilities are any simple data structure that your program needs to share.
It can be as simple as a string and as complicated as a nested dictionary. The
typical usage of this data structure is to pass information about the member,
such as its processing power or its feature set. It allows filtering members
based on their functionality or weighing them differently based on their
computing power.

Joining a group with a capability set
The example below shows a complete example of joining a group with a capability
set. In this example, each client can provide a mood when joining a group. All
members can then get member capabilities and retrieve their moods.


"""
import sys
import time
from tooz import coordination

# Check that a client and group ids are passed as arguments
if len(sys.argv) != 4:
    print("Usage: %s <client id> <group id> <mood>" % sys.argv[0])
    sys.exit(1)

# Get the Coordinator object
c = coordination.get_coordinator("etcd3://localhost", sys.argv[1].encode())
# Start it (initiate connection).
c.start(start_heart=True)

group = sys.argv[2].encode()

# Create the group
try:
    c.create_group(group).get()
except coordination.GroupAlreadyExist:
    pass

# Join the group
c.join_group(group, capabilities={"mood": sys.argv[3]}).get()

# Print the members list and their capabilities.
# Since the API is asynchronous, we mit all the request to get the capabilities
# at the same time so they are run in parallel.
get_capabilities = [
    (member, c.get_member_capabilities(group, member))
    for member in c.get_members(group).get()
]

for member, cap in get_capabilities:
    print("Member %s has capabilities: %s" % (member, cap.get()))

# Wait 20 seconds
time.sleep(20)

# Leave the group
c.leave_group(group).get()

# Stop when we're done
c.stop()
