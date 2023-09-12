"""
Creating, Joining and Leaving Groups

Group rules
Here are the rules: a group is a set containing zero or more members. When a
node joins a group, it becomes a member of this group. A member can leave the
group at any time: either on its own (shutdown) or because it did not renew
membership. The membership tracking is automatically done by Tooz and the
backend it uses.
"""
"""
You will observe a message like Usage: tooz-join-group.py <client id> <group id>. 
You can relaunch the program by providing <client id> and <group id> such as 
python tooz-join-group.py clientA group1. You can open another terminal and 
navigate to relevant directly using cd /examples/group-membership then use the 
above command to make another client join the group. One member stays in the 
group for 60 seconds.
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

# Create the group
try:
    c.create_group(group).get()
except coordination.GroupAlreadyExist:
    pass

# Join the group
c.join_group(group).get()

# Print the members list
members = c.get_members(group)
print(members.get())

# Wait 60 seconds
time.sleep(60)

# Leave the group
c.leave_group(group).get()

# Stop when we're done
c.stop()


"""
The first step after starting the coordinator is to create the group. It is 
possible that the group has been already created, in that another client could 
have already joined that group. If that is the case, we just ignore the 
< coordination.GroupAlreadyExist > exception that is raised on line 22 of the 
above application.

The second step is to join the group. That is done using the < join_group > method. 
You might have noticed that the get method is called every time on the result 
of the < join_group > or < create_group>  methods. Indeed, Tooz exposes an 
asynchronous API; that means that calling join_group starts the process of 
joining the group, but the group is not fully joined for sure until the 
application calls the get method of the returned value of < join_group >.

Once the group is joined, you can print the list of the members that are in the 
group. That is done by using the < get_members > method.

As the example allows you to specify the group id and the member id, you can 
run any number of those examples on any number of nodes. As long as they connect 
to the same etcd service, they see each other in the same group.
"""
