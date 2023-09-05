def compute(numbers):
    ### `filter` function filters the number that are smaller than 50 and then the
    ### `map` applies the multiplication operator on each of the filtered number.
    ###  Finally, the `sum` function calculates the sum of the squared numbers in the list
    return sum(list(map(lambda x: x * x, filter(lambda x: x < 50, numbers))))


numbers = [10, 3, 52, 79]

print(list(filter(lambda x: x < 50, numbers)))
print(list(map(lambda x: x * x, filter(lambda x: x < 50, numbers))))
print(compute(numbers))
