from concurrent import futures
import requests

with futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(lambda: requests.get("http://example.org")) for _ in range(8)
    ]

results = [f.result().status_code for f in futures]

print("Results: %s" % results)

"""
The above application uses futures.ThreadPoolExecuter with four workers to send 
the GET request to example.org. The status codes of the responses are stored in 
the results list as the responses arrive.
"""
