"""
Task executions might fail, and in this case, it is crucial to handle that
properly. It is common for tasks to depend on external services, such as a
remote database or a REST API. Connection failure might be transient; it is
therefore better to deal with defeat and retry later.
"""
"""
Open another terminal and enter the command: <celery -A celery-task-retry worker>.
The 4.-celery_task_retry.py will keep waiting until the worker is started. Once
it does, the result is calculated by the 4.-celery_task_retry.py.
"""
import celery

app = celery.Celery(
    "celery-task-retry", broker="redis://localhost", backend="redis://localhost"
)


@app.task(bind=True, retry_backoff=True, retry_kwargs={"max_retries": 5})
def add(self, x, y):
    try:
        return x + y
    except OverflowError as exc:
        self.retry(exc=exc)


if __name__ == "__main__":
    result = add.delay(4, 4)
    print("Task state: %s" % result.state)
    print("Result: %s" % result.get())
    print("Task state: %s" % result.state)


"""
The above example implements a simple retry logic if an OverflowError occurs. 
The retry_backoff argument makes sure that Celery retries using an exponential 
backoff algorithm between delays (as described in Retrying with Tenacity lesson), 
while the max_retries argument makes sure it does not retry more than five times. 
Limiting the number of retries is important, as you never want to have jobs 
stuck forever in your queue because of a permanent error or a bug.
"""
"""
Record visits
Retrying a task calls the same function with the same argument. That means that 
the best design for those tasks is, as is usually the case, to be entirely 
idempotent. If a task has side effects and fails in the middle of its execution, 
it might be more complicated to handle the task repeat execution later on. 
Consider the following piece of code:

@app.task(autoretry_for=(DatabaseError,))
def record_visit(user_id):
  database.increment_visitor_counter()
  remote_api.record_last_visit_time(user_id)
  
If an error occurs while calling remote_api.record_last_visit_time, the visitor 
counter would already be incremented. When the task is retried, the counter 
will be incremented again, counting the visitor twice. Such a task should be 
re-written in a way where if executed multiple times, it produces the same 
result in the final system.
"""
"""
Note: By default, Celery stores the results in the specified backend. However, 
it is sometimes the case that a task has no interesting return value. In that 
case, pass the ignore_result=True to the app.task decorator to make sure the 
results are ignored.
"""
