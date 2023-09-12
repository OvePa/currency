"""
There’s still one essential tool missing from this list. One common task when
working with lists is finding the first item that satisfies a specific condition.
This is usually accomplished with a function like this:
"""
import itertools


def first_positive_number(numbers):
    for n in numbers:
        if n > 0:
            return n


mylist = [-1, -10, 5, 7, -3, 8]
print(first_positive_number(mylist))


# We can also write this in functional style:
def first(predicate, items):
    for item in items:
        if predicate(item):
            return item


print(first(lambda x: x > 0, [-1, 0, 1, 2]))


"""
Using next

You can also return first positive number more concisely like this:
"""
# Less efficient
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))[0]

# Efficient but for Python 3
next(filter(lambda x: x > 0, [-1, 0, 1, 2]))

# Efficient but for Python 2
# next(itertools.ifilter(lambda x: x > 0, [-1, 0, 1, 2]))

"""
Note: list(filter(lambda x: x > 0, [-1, 0, 1, 2]))[0] may elicit an IndexError 
if no items satisfy the condition, causing list(filter()) to return an empty list.
"""

# For simple cases you can also rely on next:
a = range(10)
print(next(x for x in a if x > 3))

# This will raise StopIteration if a condition can never be satisfied.
# In that case, the second argument of next can be used:
a = range(10)
print(next((x for x in a if x > 10), "default"))


"""
Using first

Instead of writing this same function in every program you make, you can 
include the small, but very useful Python package first:
"""
from first import first

# Returns 42 because it is the first element in the list which is True
print(first([0, False, None, [], (), 42]))

# Returns -1 as it is the first element in the list which is True
print(first([-1, 0, 1, 2]))

# Returns 1 as it is the first element in the list which is True
# according to the condition provided: (x > 0)
print(first([-1, 0, 1, 2], key=lambda x: x > 0))
"""
The key argument can be used to provide a function which receives each item as 
an argument and returns a Boolean indicating whether it satisfies the condition.
"""
"""
You will notice that we used lambda in a good number of the examples so far in 
this chapter. In the first place, lambda was added to Python to facilitate 
functional programming functions such as map and filter. This would otherwise 
have required writing an entirely new function every time you wanted to check 
a different condition:
"""
import operator
from first import first


def greater_than_zero(number):
    return number > 0


print(first([-1, 0, 1, 2], key=greater_than_zero))

"""
This code works identically to the previous example, but it is a good deal more 
cumbersome: if we wanted to get the first number in the sequence that is greater 
than, say, 42, then we would need to def an appropriate function rather than 
defining it in-line with our call to first.

However, despite its usefulness in helping us avoid situations like this, 
lambda still has its drawbacks. First, and most obviously, we cannot pass a key 
function using lambda if it would require more than a single line of code. 
In this event, we are back to the cumbersome pattern of writing new function 
definitions for each key we need… or are we?

Our first step towards replacing lambda with a more flexible alternative is 
functools.partial. It allows us to create a wrapper function with a twist: 
rather than changing the behavior of a function, it instead changes the arguments 
it receives:
"""
from functools import partial
from first import first


def greater_than(number, min=0):
    return number > min


print(first([-1, 0, 1, 2], key=partial(greater_than, min=42)))

"""
Our new greater_than function works just like the old greater_than_zero by 
default, but now we can specify the value we want to compare our numbers to. 
In this case, we pass functools.partial our function and the value we want for 
min, and we get back a new function that has min set to 42, just like we want. 
In other words, we can write a function and use functools.partial to customize 
what it does to our needs in any given situation.

This is still a couple of lines more than we strictly need in this case, though. 
All we are doing in this example is comparing two numbers; what if Python had 
built-in functions for these kinds of comparisons? As it turns out, the operator 
module has just what we are looking for:
"""
import operator
from functools import partial
from first import first

print(first([-1, 0, 1, 2], key=partial(operator.le, 0)))
"""
Here we see that functools.partial also works with positional arguments. 
In this case, operator.le(a, b) takes two numbers and returns whether the first 
is less than or equal to the second: the 0 we pass to functools.partial gets 
sent to a, and the argument passed to the function returned by functools.partial 
gets sent to b. This works identically to our initial example, without using 
lambda or defining any additional functions.
"""
"""
Note: functools.partial is typically useful as a replacement of lambda and 
it should be considered as a superior alternative. lambda is to be considered 
an anomaly in Python language due to its limited body size of a single expression 
that is one line long. Lambda was once even planned for removal in Python 3, 
but in the end it escaped this fate. On the other hand, functools.partial is built 
as a nice wrapper around the original function.
"""


"""
The itertools

The itertools module in the Python standard library also provides a number of 
useful functions that you will want to keep in mind. Too many programmers end up 
writing their own versions of these functions even though Python itself provides 
them out-of-the-box:
"""
# -> accumulate(iterable[, func]) returns a series of accumulation of items
# from iterables, or whatever is mapped to the + operator.

import itertools
import operator

# initializing list
mylist = [1, 4, 5, 7]

print(list(itertools.accumulate(mylist)))

# -> chain(*iterables) iterates over multiple iterables, one after another
# without building an intermediate list of all items.

import itertools
import operator

# initializing list
mylist = [1, 4, 5, 7]
mylist2 = [11, 16, 15, 12]
mylist3 = [21, 26, 34, 42]

print(list(itertools.chain(mylist, mylist2, mylist3)))

# -> combinations(iterable, r) generates all combinations of length r from
# the given iterable.
from itertools import combinations

print(list(combinations("ABCD", 2)))

# -> compress(data, selectors) applies a Boolean mask from selectors to data
# and returns only the values from data where the corresponding element of
# selectors is true.
from itertools import compress

print(list(compress("EDUCATIVE", [1, 0, 1, 0, 0, 1, 0, 0, 1])))

# -> count(start, step) generates an endless sequence of values, starting from
# start and incrementing a step at a time with each call.
from itertools import count

for x in count(5, 5):
    if x == 50:
        break
    print(x)

# -> cycle(iterable) loops repeatedly over the values in iterable.
from itertools import cycle

count = 0

for i in cycle("EDUCATIVE"):
    if count > 15:
        break
    print(i, end=" ")
    count += 1

# -> repeat(elem[, n]) repeats an element n times.
from itertools import repeat

print(list(repeat(20, 5)))

# -> dropwhile(predicate, iterable) filters elements of an iterable starting
# from the beginning until predicate is false.
from itertools import dropwhile

# initializing list
mylist = [2, 4, 5, 8, 9, 10]

# using dropwhile() to start displaying after condition is false
print(list(dropwhile(lambda x: x % 2 == 0, mylist)))


# -> groupby(iterable, keyfunc) creates an iterator grouping items by the
# result returned by the keyfunc function.
from itertools import groupby

mylist = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("C", 6), ("C", 7)]

# Key function
getKey = lambda x: x[0]

for key, group in groupby(mylist, getKey):
    print(key + " :", list(group))

# -> permutations(iterable[, r]) returns successive r-length permutations of
# the items in iterable.
from itertools import permutations

print(list(permutations([1, 2, 3], 2)))

# -> product(*iterables) returns an iterable of the Cartesian product of
# iterables without using a nested for loop.
from itertools import product

print(list(product("ABC", [3, 4])))

# -> takewhile(predicate, iterable) returns elements of an iterable starting
# from the beginning until the predicate is false.
from itertools import takewhile

# initializing list
mylist = [2, 4, 6, 7, 8, 10, 20]

# using takewhile() to print values till condition is false.
print(list(takewhile(lambda x: x % 2 == 0, mylist)))

"""
These functions are particularly useful in conjunction with the operator module. 
When used together, itertools and the operator can handle most situations for 
which programmers typically rely on lambda:
"""

import itertools

a = [{"foo": "bar"}, {"foo": "bar", "x": 42}, {"foo": "baz", "y": 43}]

import operator

print(list(itertools.groupby(a, operator.itemgetter("foo"))))

print(
    [
        (key, list(group))
        for key, group in itertools.groupby(a, operator.itemgetter("foo"))
    ]
)

"""
In this case, we could have also written lambda x:x["foo"], but using operator 
lets us avoid having to use lambda at all.

As previously explained, all of the code and functions presented in this section 
are purely functional. That means they have no side effects, and moreover, 
they have no dependency on any global, shared data. Writing code using that 
style of programming is a key to scalability, as it makes it easy to execute 
those functions in parallel, or even to spread their execution on different systems.
"""
