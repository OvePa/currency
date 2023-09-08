"""
Solution: Add failure handling

We use tenacity to handle failures in our web crawler.
"""
import celery
import requests
import tenacity

app = celery.Celery(
    "celery-proj", broker="redis://localhost", backend="redis://localhost"
)


def do_something(url_to_crawl):
    dic = {}
    r = requests.get(url=url_to_crawl)
    if r.status_code != 200:
        raise RuntimeError
    text = r.text
    dic["data"] = text
    dic["status_code"] = r.status_code
    return dic


@app.task()
def getURL(url_to_crawl):
    @tenacity.retry(wait=tenacity.wait_fixed(5), stop=tenacity.stop_after_attempt(3))
    def do_something_and_retry(url_to_crawl):
        return do_something(url_to_crawl)

    return do_something_and_retry(url_to_crawl)


if __name__ == "__main__":
    urls = ["http://educative.io", "http://example.org/", "http://example2ed3d.com"]

    results = []
    for url in urls:
        results.append(getURL.delay(url))

    for result in results:
        print("Task state: %s" % result.state)
        print("Result: %s" % result.get())
        print("Task state: %s" % result.state)

"""
Solution explanation

The tenacity library is used in the getURL() function. On line 28, tenacity 
decorator is defined with < wait=tenacity.wait_fixed(5) > so that it waits for 5 
seconds before retrying. The < stop=tenacity.stop_after_attempt(3) > argument is 
used so that it retries 3 times before giving up on a certain URL.

In line 29 - 30, < do_something_and_retry() > function is defined on which the 
decorator is applied. This function is then called right after the definition. 
The original body of < getURL() > function is moved to < do_something() > 
function defined on line 15 - 23. The result of < do_something() > is returned to 
the caller < do_something_and_retry() >, which then returns it to < getURL() >, 
and it returns the result to the main function (results list).

To demonstrate the retrying mechanism, we replace the third URL in the urls list 
that does not exist (http://example2ed3d.com). When the request fetches this URL, 
it checks for the < status_code > of the response on line 18, since the status code 
of this is not 200, it raises RuntimeError exception. The tenacity keeps on 
trying but eventually stops and raises < tenacity.RetryError > for this URL.
"""

"""
Terminal - todo en una sola linea

redis-server --daemonize yes && 
celery -A celery-proj worker -n worker1 --detach && 
celery -A celery-proj worker -n worker2 --detach && 
celery -A celery-proj worker -n worker3 --detach && 
python celery-proj.py
"""
