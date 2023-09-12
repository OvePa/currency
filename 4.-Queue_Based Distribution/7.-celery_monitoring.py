"""
Celery: Monitoring

Celery comes with a lot of monitoring tools built in, and this allows you to
supervise things and get information about what is going on inside the cluster.
This also makes it a great option over a custom built solution where all of
this would have to be implemented again.
"""
# python 7.-celery_monitoring.py
# another terminal :< elery -A celery-task-queue worker --queues celery,low-priority >
# another terminal: < celery -A celery-task-queue status >
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
The result of celery -A celery-task-queue status will be the status and the 
number of nodes online.
"""
"""
Inspect
The inspect command accepts a few subcommands, among them active, which returns 
the task currently being done. Enter celery < -A celery-task-queue inspect active >
command in any idle terminal
"""
"""
Celery web dashboard
Celery also comes with a nicely designed Web dashboard that allows for 
supervising the activity of the workers and the queue. It is named Flower and 
it is easy to install using pip install flower. It is simple enough to start.
"""
