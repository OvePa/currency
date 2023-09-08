"""
Solution: Add URLs to queue

In this component, you were required to create a celery queue and add tasks to
the queue so that they can be fetched later by a worker for processing.
"""
import celery
import requests

# cmd
# celery -A celery-proj worker --queues celery

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
    ## This urls list contains some url to be fetched
    urls = ["http://educative.io", "http://example.org/", "http://example.com"]

    results = []

    # Add tasks to queue here
    for url in urls:
        results.append(getURL.delay(url))

    # Print the tasks states here
    for result in results:
        print("Task state: %s" % result.state)


"""
Solution explanation
The solution to this component can be divided into three sub-parts:

On line 13 - 15, a celery queue is created that has redis as backend and broker. 
We also start the redis server in the background using command 
redis-server --daemonize yes.

On line 18 - 25, a celery task is defined. This includes the declaration of the 
task @app.task() followed by the function definition that workers would be running. 
The getURL() function takes a URL as an argument and fetches the URL using requests. 
It stores the text and status_code of the response in a dictionary and returns it.

From line 28 - 40 is the main function that has the list urls containing all 
the URLs to be fetched and an empty results list where all the responses will 
be stored. We populated the urls list with three sample URLs. On line 35 -36 
we iterate over the URLs to send it to the queue using getURL.delay() function 
and append the celery.result.AsyncResult object to the results list. Finally, 
on line 39 - 40, we display the state of each task which would be pending since 
there are no workers yet.
"""
