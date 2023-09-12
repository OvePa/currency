"""
Celery execution workflow
Celery supports chaining tasks, which allows you to build more complex workflows.
"""
# python 5.-celery_chain.py
# Another terminal and Enter the command: <celery -A celery-chain worker>.

import celery

app = celery.Celery(
    "celery-chain", broker="redis://localhost", backend="redis://localhost"
)


@app.task
def add(x, y):
    return x + y


@app.task
def multiply(x, y):
    return x * y


if __name__ == "__main__":
    chain = celery.chain(add.s(4, 6), multiply.s(10))
    print("Chain: %s" % chain)
    result = chain()
    print("Task state: %s" % result.state)
    print("Result: %s" % result.get())
    print("Task state: %s" % result.state)


"""
The above example shows how to chain two tasks. First, the numbers 4 and 6 are 
summed using the add function. Then, the result of this function is passed to 
multiply with 10 as the second argument. The Chain, Task state, and the Result 
is displayed when you run worker and 5.-celery_chain.py.

Building your program with multiple idempotent functions that can be chained 
together is very natural in functional programming. Again, this kind of design 
makes it very easy to parallelize job execution and therefore makes it possible 
to increase the throughput of your program and scale its execution horizontally.
"""
