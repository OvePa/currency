cache = {}


def fib(n):
    if n <= 0:
        return 0
    if n == 1 or n == 2:
        return 1
    try:
        return cache[n]
    except:
        result = fib(n - 1) + fib(n - 2)
        cache[n] = result
        return result


## Modify it to fib(100) to see how long it takes!
print(fib(100))
