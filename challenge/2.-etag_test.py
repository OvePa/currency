import random
import unittest
import flask
from werkzeug import exceptions

app = flask.Flask(__name__)


class NotModified(exceptions.HTTPException):
    code = 304


ETAG = random.randint(1000, 5000)
serverData = "hello"


def check_etag(exception_class):
    global ETAG

    if_match = flask.request.headers.get("If-Match")
    if if_match is not None and if_match != str(ETAG):
        raise exception_class

    if_none_match = flask.request.headers.get("If-None-Match")
    if if_none_match is not None and if_none_match == str(ETAG):
        raise exception_class


@app.route("/", methods=["GET"])
def get_index():
    check_etag(NotModified)
    return flask.Response(serverData, headers={"ETag": ETAG})


@app.route("/", methods=["PUT"])
def put_index():
    global ETAG, serverData

    check_etag(exceptions.PreconditionFailed)

    ETAG += random.randint(3, 9)
    serverData = flask.request.data
    return flask.Response(serverData, headers={"ETag": ETAG})


if __name__ == "__main__":
    app.run()
