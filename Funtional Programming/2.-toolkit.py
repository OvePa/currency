"""
map(function, iterable)

map(function, iterable) applies the function to each item in iterable and
returns either a list in Python 2 or an iterable map object in Python 3:
"""
print(map(lambda x: x + "bzz!", ["I think", "I'm good"]))

## map wrapped in a list to print the list
print(list(map(lambda x: x + "bzz!", ["I think", "I'm good"])))


"""
filter(function or None, iterable)

filter(function or None, iterable) filters the items in iterable based on the 
result returned by the function and returns either a list in Python 2 or better, 
an iterable filter object in Python 3:
"""
print(filter(lambda x: x.startswith("I "), ["I think", "I'm good"]))

## filter wrapped in a list to print
print(list(filter(lambda x: x.startswith("I "), ["I think", "I'm good"])))


"""
TIPS

You can write a function equivalent to filter or map using generators and list 
comprehension:

Equivalent of map using list comprehension
"""
(x + "bzz!" for x in ["I think", "I'm good"])
# <generator object <genexpr> at 0x7f9a0d697dc0>
[x + "bzz!" for x in ["I think", "I'm good"]]
# ['I thinkbzz!', 'I\'m goodbzz!']

"""Equivalent of filter using list comprehension"""
(x for x in ["I think", "I'm good"] if x.startswith("I "))
# <generator object <genexpr> at 0x7f9a0d697dc0>
[x for x in ["I think", "I'm good"] if x.startswith("I ")]
# ['I think']

""" END TIPS"""

"""
enumerate(iterable[, start])

enumerate(iterable[, start]) returns an iterable enumerate object that yields a 
sequence of tuples, each consisting of an integer index (starting with start, 
if provided) and the corresponding item in iterable. It is useful when you need 
to write code that refers to array indexes.
"""
mylist = [1, 2, 3]
for i, item in enumerate(mylist):
    print("Item %d: %s" % (i, item))


"""
sorted(iterable, key=None, reverse=False)
sorted(iterable, key=None, reverse=False) returns a sorted version of iterable. 
The key argument allows you to provide a function that returns the value to sort on.
"""

print(sorted([10, 5, 20, 30, 25, -5]))


"""
any(iterable) and all(iterable)

any(iterable) and all(iterable) both return a boolean depending on the values 
returned by iterable. These functions are equivalent to:
"""


def all(iterable):
    for x in iterable:
        if not x:
            return False
    return True


## Returns False because 0 is False
print(all([1, 0, 3, 5]))


def any(iterable):
    for x in iterable:
        if x:
            return True
    return False


## Returns True because 1, 3 and 5 are True
print(any([1, 0, 3, 5]))

# These functions are useful for checking whether any or all of the values
# in an iterable satisfy a given condition:
mylist = [0, 1, 3, -1]
if all(map(lambda x: x > 0, mylist)):
    print("All items are greater than 0")
if any(map(lambda x: x > 0, mylist)):
    print("At least one item is greater than 0")


"""
zip(iter1 [,iter2 [...]])

The zip(iter1 [,iter2 [...]]) takes multiple sequences and combines them into 
tuples. It is useful when you need to combine a list of keys and a list of 
values into a dictionary. Like the other functions described above, it returns 
a list in Python 2 and an iterable in Python 3:
"""
keys = ["foobar", "barzz", "ba!"]

print(map(len, keys))

print(zip(keys, map(len, keys)))

print(list(zip(keys, map(len, keys))))

print(dict(zip(keys, map(len, keys))))
