"""
Problem
You have implemented a flask-based REST API server that stores a variable
serverData. The contents of this data do not change very frequently so you want
to enable caching using ETag. The server code given below works fine without
using caching and returns the content every time, even when it is not changed.

Your task is to implement ETag in the following server so that it sends 304 Not
Modified on every GET request if the ETag provided is not updated. However,
it should send the updated value otherwise and send the new Etag to the clients.

After implementing Etag functionality, run http GET http://127.0.0.1:5000
If-None-Match:"<your_etag>" to see the 304 Not Modified response. Try to change
the serverData using PUT and then check if it returns updated content.

To run the following application, run the command python etag-test.py. It will
start the flask-based HTTP server. Then, open another terminal, and contact the
server using command http HEAD http://127.0.0.1:5000.
Run http PUT http://127.0.0.1:5000 serverData="New data" to update the
serverData variable.
"""
import random
import flask
from werkzeug import exceptions

app = flask.Flask(__name__)

serverData = "This is some useful data"


@app.route("/", methods=["GET"])
def get_index():
    return flask.Response(serverData)


@app.route("/", methods=["PUT"])
def put_index():
    global serverData

    serverData = flask.request.data
    return flask.Response(serverData)


if __name__ == "__main__":
    app.run()
