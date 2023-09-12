import requests


def do_something(response):
    print("Got response!", response)
    return "Hello"


while True:
    resp = requests.get(url="http://127.0.0.1:5000")
    etag = resp.headers["ETag"]

    new_data = do_something(resp)

    resp = requests.put(
        url="http://127.0.0.1:5000", data=new_data, headers={"If-Match": etag}
    )
    print("Status code:", resp.status_code)
    if resp.status_code == 200:
        break
    elif resp.status_code == 412:
        continue
    else:
        raise RuntimeError("Unknown exception: %d" % resp.status_code)
