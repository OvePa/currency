"""
Using ETag in flask application
The application in the following example shows how one can use the ETag header
to avoid returning the content of a request by checking the headers
If-None-Match and If-Match.

To run the following application, run the command python flask-etag.py. It will
start the flask based HTTP server. Then, open another terminal, and contact
the server using command http HEAD http://127.0.0.1:5000. Run http
GET http://127.0.0.1:5000 If-None-Match:"hword" to see the 304 Not Modified
response.

"""
import unittest
import flask
import werkzeug

application = flask.Flask(__name__)


class NotModified(werkzeug.exceptions.HTTPException):
    code = 304


@application.route("/", methods=["GET"])
def get_index():
    # Since the content here is always the same, we only have one Etag value
    ETAG = "hword"

    if_match = flask.request.headers.get("If-Match")
    if if_match is not None and if_match != ETAG:
        raise NotModified

    if_none_match = flask.request.headers.get("If-None-Match")
    if if_none_match is not None and if_none_match == ETAG:
        raise NotModified

    return flask.Response("hello world", headers={"ETag": "hword"})


class TestApp(unittest.TestCase):
    def test_get_index(self):
        test_app = application.test_client()
        result = test_app.get()
        self.assertEqual(200, result.status_code)

    def test_get_index_if_match_positive(self):
        test_app = application.test_client()
        result = test_app.get(headers={"If-Match": "hword"})
        self.assertEqual(200, result.status_code)

    def test_get_index_if_match_negative(self):
        test_app = application.test_client()
        result = test_app.get(headers={"If-Match": "foobar"})
        self.assertEqual(304, result.status_code)

    def test_get_index_if_none_match_positive(self):
        test_app = application.test_client()
        result = test_app.get(headers={"If-None-Match": "hword"})
        self.assertEqual(304, result.status_code)

    def test_get_index_if_none_match_negative(self):
        test_app = application.test_client()
        result = test_app.get(headers={"If-None-Match": "foobar"})
        self.assertEqual(200, result.status_code)


if __name__ == "__main__":
    application.run()

"""
ETags can also be used for optimistic concurrency control to help prevent 
simultaneous updates of a resource from overwriting each other. By comparing 
the ETag received during the first GET request and by passing it in a subsequent 
PUT, POST, PATCH or DELETE request, it is possible to make sure that concurrent 
operations are not writing on to each other.
"""
