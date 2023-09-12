import sys
import time
from tooz import coordination

members = 1

def addMemberCount(group):
    global members
    print("Adding member")
    members += 1
    print("Total members now: ", members)

def subMemberCount(group):
    global members
    print("Removing member")
    members -= 1
    print("Total members now: ", members)

# Check that a client and group ids are passed as arguments
if len(sys.argv) != 3:
    print("Usage: %s <client id> <group id>" % sys.argv[0])
    sys.exit(1)

# Get the Coordinator object
c = coordination.get_coordinator(
    # Set a short timeout to see effects faster
    "etcd3://localhost/?timeout=3",
    sys.argv[1].encode())
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
c.watch_join_group(group, addMemberCount)
c.watch_leave_group(group, subMemberCount)

while True:
    c.run_watchers()
    time.sleep(1)

# Leave the group
c.leave_group(group).get()

# Stop when we're done
c.stop()