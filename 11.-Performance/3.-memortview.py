"""
memoryview
When dealing with large amounts of data, performing this kind of operation on
large byte arrays is going to be a disaster. If you happen to have experience
writing C code, you know that using malloc and memcpy has a significant cost,
both in terms of memory usage and regarding general performance: allocation
and copying memory is slow.

However, as a C programmer, you also know that strings are arrays of characters
and that nothing stops you from looking at only part of this array without
copying it, through the use of pointer arithmetic, assuming that the entire
string is in a contiguous memory area.

This is possible in Python using objects that implement the buffer protocol.
The buffer protocol is defined in PEP 3118, which explains the C API used to
provide this protocol to various types, such as strings.

When an object implements this protocol, you can use the memoryview class
constructor on it to build a new memoryview object that references the original
object memory.
"""
s = b"abcdefgh"
view = memoryview(s)
print("View[1]: ", view[1])  # 98 is the ASCII code for the letter b.

limited = view[1:3]
print("limited: ", limited)

print("bytes(view[1:3]): ", bytes(view[1:3]))

"""
In this case, we are going to make use of the fact that the memoryview object’s 
slice operator itself returns a memoryview object. That means it does not copy 
any data, but merely references a particular slice of it.

With this in mind, we can now rewrite the program, this time referencing the 
data we want to write using a memoryview object.
"""
