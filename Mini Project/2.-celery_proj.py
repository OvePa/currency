"""
Solution: Add workers

Now that the tasks are waiting to be processed in the queue, you can add celery
workers to process these tasks. Workers can be added using command
< celery -A celery-task worker >. You can also name the workers when using more
than one worker using < -n workername > flag. Workers can be started in the
background using < --detach > flag.
"""
import celery
import requests

app = celery.Celery(
    "celery-proj", broker="redis://localhost", backend="redis://localhost"
)


@app.task()
def getURL(url_to_crawl):
    dic = {}
    r = requests.get(url=url_to_crawl)
    text = r.text
    dic["data"] = text
    dic["status_code"] = r.status_code
    return dic


if __name__ == "__main__":
    urls = ["http://educative.io", "http://example.org/", "http://example.com"]

    results = []
    for url in urls:
        results.append(getURL.delay(url))

    for result in results:
        print("Task state: %s" % result.state)
        print("Result: %s" % result.get())
        print("Task state: %s" % result.state)


"""
Solution explanation

We start three workers using commands 
< celery -A celery-proj worker -n worker1 --detach >, 
< celery -A celery-proj worker -n worker2 --detach >, and 
< celery -A celery-proj worker -n worker3 --detach > commands.

The workers start processing the task and the responses are stored in results 
list. The task state is changed from PENDING to SUCCESS. The responses are also 
printed using result.get() function on line 37.
"""
