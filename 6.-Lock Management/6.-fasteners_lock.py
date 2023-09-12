"""
As stated earlier, multiprocessing.Lock only works for processes started from a
single Python process. If your application is distributed across several Python
processes, such as a daemon started independently, you need an interprocess lock
mechanism.

Those locks are usually not portable across operating systems. POSIX, System V
or even Windows all offer different interprocess communication mechanisms, and
they are not compatible with one another. You may want to look in this direction
if you are not afraid of making your software platform-dependent.
"""

"""
fasteners

The fasteners module provides an excellent implementation of a generic solution 
based on file locks in Python.

Note: Locks implemented by fasteners are based on file-system locks. They are 
not specific to Python. Therefore you could also implement the same file-locking 
mechanism in another programming language in order to have cross-language locking.

Fasteners provides a lock class fasteners.InterProcessLock that takes a file 
path as its first argument. This file path is going to be the identifier for 
this lock, and it can be used across multiple independent processes. This is 
why fasteners is helpful to lock access to resources across processes that were 
started independently.
"""
import time
import fasteners

lock = fasteners.InterProcessLock("/tmp/mylock")
with lock:
    print("Access locked")
    time.sleep(1)


"""
If you run multiple copies of the program in the above example, they all 
sequentially print “Access locked” after acquiring the lock.

There is no helper provided by fasteners nor is there any rule to determine 
which file path should be used by your application. The usual convention is 
for it to be in a temporary directory that is purged on system start, such as 
$TMPDIR or /var/run. It is up to you to determine the directory where to create 
the file and to have a filename that is unique to your application but known 
to all processes.
"""
