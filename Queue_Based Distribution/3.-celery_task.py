"""
Celery backend
Celery also needs a backend for storing the results of the job. It supports a
variety of solutions, such as Redis, MongoDB, SQL databases, ElasticSearch,
files, RabbitMQ or Amazon SQS, etc. Just like for brokers, you can also write
your own.

Celery implements its own serialization format for its jobs. However, this
format is not specific to Python. That means it is possible to implement job
creators or consumers in different languages. There are already clients in PHP
and Javascript.
"""
"""
Celery task execution: Worker and queues

In Celery, tasks are functions that can be called asynchronously. When called, 
Celery puts them in the broker queue for execution. Remote workers then execute 
the tasks, putting the task results into the backend.

When called, a task returns a <celery.result.AsyncResult> object. This object 
offers a principal method, get, which returns the result as soon as it is 
available, blocking the program in the meantime.
"""
import celery

app = celery.Celery(
    "celery-task", broker="redis://localhost", backend="redis://localhost"
)


@app.task
def add(x, y):
    return x + y


if __name__ == "__main__":
    result = add.delay(4, 4)
    print("Task state: %s" % result.state)
    print("Result: %s" % result.get())
    print("Task state: %s" % result.state)


"""
The above example is a simple implementation of a Celery task. The Celery 
application is created with the main module name as its first argument, and 
then the URL to access the broker and backends.

The <app.task> function decorator registers the add task so it can be used 
asynchronously in the application, leveraging Celery workers for execution.

Once run, this program prints Task state: PENDING.

The program is blocked and then waits forever. There is no worker processing 
the job queue yet, therefore calling the <result.get> method blocks the program 
until the result is ready, which is not going to happen until a worker starts.

The celery command line tool provides a broad set of commands to manipulate and 
inspect the jobs queue and the workers. It is in charge of starting the actual 
workers.
"""
"""
Note: After running python 3.-celery_task.py open another terminal. 
Then, enter the command: <celery -A celery-task worker>. The output will be the 
configuration settings and queues.
"""
"""
As soon as it starts, the worker processes queue tasks and puts results in the 
backend. That unblocks the program celery-task started earlier and prints the 
computed result.
"""
