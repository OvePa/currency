# importing the requests library
import requests, time

urls = ["http://educative.io", "http://educative.io/blog", "http://youtube.com"]

start_time = time.time()
for URL in urls:
    r = requests.get(url = URL)
    data = r.content
    print(data)
print("--- %s milliseconds ---" % ((time.time() - start_time)*1000))