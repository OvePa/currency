"""
Celery: Multiple Queues

By default, Celery uses a single queue named <celery>. However, it is possible to
use multiple queues to spread the distribution of the tasks. This feature makes
it possible to have finer control over the distribution of the jobs to execute.
"""
"""
Low priority job

For example, it is common to have a queue dedicated to low-priority jobs, where 
only a few workers are available.
The queue for a task can be specified at call time as shown in line number 32 
in the example below.

Notice the new options in the worker command --queues celery,low-priority.
"""
# python 6.-celery_task_queue.py
# another terminal and Enter the command <celery -A celery-task-queue worker --queues celery,low-priority>
import celery

app = celery.Celery(
    "celery-task-queue", broker="redis://localhost", backend="redis://localhost"
)


@app.task
def add(x, y):
    return x + y


if __name__ == "__main__":
    result = add.apply_async(args=[4, 6], queue="low-priority")
    print("Task state: %s" % result.state)
    print("Result: %s" % result.get())
    print("Task state: %s" % result.state)


"""
To treat queues other than just the default one, there’s the --queues option. 
Upon running the above application, the configuration settings and queues will 
be displayed.

This worker consumes jobs from both the default celery queue and the low-priority 
queues. Running other workers with just the celery queue would make sure that 
the low-priority queue is only acted on by one worker when the worker has time 
to do it, whereas all the other workers would keep waiting for normal priority 
jobs on the default celery queue.

There is no magic recipe to determine the number of queues that your application 
may need. Using the jobs priority as a criteria to split them is the most common 
and obvious use case. Queues give you access to more finely grained scheduling 
possibilities, so don’t hesitate to use them.
"""
