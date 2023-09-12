"""
Testing REST API

Writing REST APIs is nice, but writing REST APIs that work is better. That is
why you should always write and run tests against those APIs. It can be tedious
and feel unrewarding; however, it is always the solid call in the long run.

Running a distributed system requires cooperation between developers, quality
control, and operation engineers. It also means that all those involved should
be able to make sure that a service is going to be OK. It is important for
developers to be able to do rapid prototyping and testing of an idea. It is
crucial for quality engineers to be able to validate what is expected from the
developed service. It is essential that engineers deploying the service can
test that it is deployed and works as expected.
"""
"""
Testing using gabbi
With all of that in mind, the traditional way of writing Python unit and functional 
tests sounds a bit far from this objective. However, there is a Python tool that 
is great at solving this problem: it is named Gabbi.

Gabbi is an HTTP testing tool. It allows writing testing scenarios in a 
declarative YAML-based format. This file format is powerful enough to write all 
the tests you could use and imagine while staying simple enough so that it is 
easy to write and maintain. Having an uncomplicated way of writing tests is 
helpful as it lowers the friction and the barrier of entry when it comes to 
writing tests. Concretely, this means it is less of a burden for the software 
engineer to write tests and it is simpler for quality engineers to provide new 
checks.

To run tests, Gabbi needs a YAML file per scenario to run. A scenario is a 
sequence of HTTP calls, each one described as an entry, such as shown in the 
snapshot provided below.
tests:
  - name: A test
    GET: /api/resources/id
"""
import os
import flask
from gabbi import driver
import werkzeug

application = flask.Flask(__name__)


class NotModified(werkzeug.exceptions.HTTPException):
    code = 304


@application.route("/", methods=["GET"])
def get_index():
    # Since the content here is always the same, we only have one ETag value
    ETAG = "hword"

    if_match = flask.request.headers.get("If-Match")
    if if_match is not None and if_match != ETAG:
        raise NotModified

    if_none_match = flask.request.headers.get("If-None-Match")
    if if_none_match is not None and if_none_match == ETAG:
        raise NotModified

    return flask.Response("hello world", headers={"ETag": "hword"})


# Run tests using:
# python3 -m unittest -v app.py
def load_tests(loader, tests, pattern):
    return driver.build_tests(
        os.path.dirname(__file__), loader, intercept=lambda: application
    )


if __name__ == "__main__":
    application.run()

"""
unittest
The tests can easily be run using the unittest module. After running the tests, 
the result will be displayed on the terminal. The result will contain the 
information regarding the tests conducted and whether the application passed 
those tests.

gabbi-run
Another interesting aspect of Gabbi is that it can run the tests from the 
command line. This portable version allows validating any deployed application, 
even in production if the tests are written with that aspect in mind.

In the application provided above, click Run and enter command python app.py to 
run the server. Then, open another terminal and change the directory to the 
relevant folder using command cd examples/building-rest-api/gabbi and run tests 
using the command gabbi-run http://localhost:5000 < etag.yaml.

The output will contain the tests conducted and their results.

Using gabbi-run, it is easy to run the YAML scenario file on a remote server. 
All it needs to be passed as argument is the root URL where to send the requests 
and a scenario on its standard input. This tool can be extremely powerful, 
for example, for continuous integration jobs where one wants to do functional 
testing with a service that is really deployed.

Gabbi provides various other features, such as the use of content from previous 
requests to send out subsequent requests or the usage of JSONPath to validate 
the returned content. Its characteristics make it incredibly powerful to test 
and validate HTTP REST API in Python.
"""
