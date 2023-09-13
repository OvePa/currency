"""
Memoization

Memoization is a technique used to speed up function calls by caching their
results. The results can be cached only if the function is pure, meaning that
it has no side effects or outputs and that it does not depend on any global
state.
"""
import math

_SIN_MEMOIZED_VALUES = {}


def memoized_sin(x):
    if x not in _SIN_MEMOIZED_VALUES:
        _SIN_MEMOIZED_VALUES[x] = math.sin(x)
    return _SIN_MEMOIZED_VALUES


print("memoized_sin(1): ", memoized_sin(1))
print("_SIN_MEMOIZED_VALUES:", _SIN_MEMOIZED_VALUES)

print("memoized_sin(2):", memoized_sin(2))
print("memoized_sin(2):", memoized_sin(2))
print("_SIN_MEMOIZED_VALUES:", _SIN_MEMOIZED_VALUES)

print("memoized_sin(1):", memoized_sin(1))
print("_SIN_MEMOIZED_VALUES:", _SIN_MEMOIZED_VALUES)
