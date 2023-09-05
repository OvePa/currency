import futurist
from futurist import waiters
import random


def compute():
    return sum([random.randint(1, 100) for i in range(10000)])


with futurist.ThreadPoolExecutor(max_workers=8) as executor:
    futs = [executor.submit(compute) for _ in range(8)]
    print(executor.statistics)

results = waiters.wait_for_all(futs)
print(executor.statistics)

print("Results: %s" % [r.result() for r in results.done])


"""
Note: The below code snippet is not meant to work properly on purpose and 
raises an exception.
"""
import futurist
from futurist import rejection
import random


def compute():
    return sum([random.randint(1, 100) for i in range(1000000)])


with futurist.ThreadPoolExecutor(
    max_workers=8, check_and_reject=rejection.reject_when_reached(2)
) as executor:
    futs = [executor.submit(compute) for _ in range(20)]
    print(executor.statistics)

results = [f.result() for f in futs]
print(executor.statistics)

print("Results: %s" % results)

"""
Depending on the speed of your computer, it is likely that the above example 
raises a futurist.RejectedSubmission exception because the executor is not fast 
enough to absorb the backlog, the size of which is limited to two. This example 
does not catch the exception. Obviously, any decent program should handle that 
exception and either retry later, or raise a different exception to the caller.
"""
