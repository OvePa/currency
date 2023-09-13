"""
Memory profiler

Let’s consider a small program that reads a large file of binary data, and
partially copies it into another file. To examine our memory usage, we will use
memory_profiler, a nice Python package that allows us to see the memory usage
of a program line by line.
"""

"""
To run the below code, click on the Run button and use command 
< python -m memory_profiler memoryview-copy.py >to run the memory_profiler.
"""


@profile
def read_random():
    with open("/dev/urandom", "rb") as source:
        content = source.read(1024 * 10000)
        content_to_write = content[1024:]
    print(
        "Content length: %d, content to write length %d"
        % (len(content), len(content_to_write))
    )
    with open("/dev/null", "wb") as target:
        target.write(content_to_write)


if __name__ == "__main__":
    read_random()
