"""
Asynchronous HTTP API

It is pretty common when writing HTTP API to return a 200 OK status code to the
caller to indicate that the request succeeded. While easy and convenient, it is
possible that the action triggered by the caller takes a lot of time. If the
call requires a long delay to be executed, it blocks the caller as it has to
wait for the reply, and this increases the risk of failure.

Indeed, if the connection lasts for too long (let’s say, a few seconds) and the
network is having issues, the connection can be interrupted. In such a case,
the caller has to retry the request. If that problem happens thousands of times
with flaky clients, it means that tons of CPU time and network bandwidth are
spent for nothing.

An obvious way to avoid those problems is to make lengthy operations asynchronous.
This can be done easily by returning a 202 Accepted HTTP status code and returning
little or no content. This status code indicates that the request has been accepted
and is being processed by the server. Another asynchronous process can then
handle the request and take care of it.
"""
"""
Flask async server
The next example provides an application implementing this mechanism. 
The provided API allows any client to use its sum service: pass some number 
to this service, and it sums them. The client can later request the results, 
as soon as it is ready.
"""
import queue  # Queue on Python 2
import threading
import uuid
import flask
from werkzeug import routing

application = flask.Flask(__name__)
JOBS = queue.Queue()
RESULTS = {}


class UUIDConverter(routing.BaseConverter):
    @staticmethod
    def to_python(value):
        try:
            return uuid.UUID(value)
        except ValueError:
            raise routing.ValidationError

    @staticmethod
    def to_url(value):
        return str(value)


application.url_map.converters["uuid"] = UUIDConverter


@application.route("/sum/<uuid:job>", methods=["GET"])
def get_job(job):
    if job not in RESULTS:
        return flask.Response(status=404)
    if RESULTS[job] is None:
        return flask.jsonify({"status": "waiting"})
    return flask.jsonify({"status": "done", "result": RESULTS[job]})


@application.route("/sum", methods=["POST"])
def post_job():
    # Generate a random job identifier
    job_id = uuid.uuid4()
    # Store the job to be executed
    RESULTS[job_id] = None
    JOBS.put((job_id, flask.request.args.getlist("number", type=float)))
    return flask.Response(
        headers={"Location": flask.url_for("get_job", job=job_id)}, status=202
    )


def compute_jobs():
    while True:
        job_id, number = JOBS.get()
        RESULTS[job_id] = sum(number)


if __name__ == "__main__":
    t = threading.Thread(target=compute_jobs)
    t.daemon = True
    t.start()
    application.run(debug=True)


"""
In the above application, on line number 42, the numbers in arguments are stored 
as a list and the list is put into JOBS queue. The compute_jobs function does the 
sum of the list using sum(number) function on line 52 and stores the result in 
the RESULTS. Then, get_job(job) function prints the result (sum) on line 34.

GET and POST endpoints
The application offers two endpoints. A request made to POST /sum should contain 
numbers in the query string. The application stores those numbers in a queue.
Queue object along with a unique identifier (UUID). Python provides thread-safe 
queues as the queue.Queue objects. Since this application uses a background (daemon) 
thread, it needs such a thread-safe data structure. This thread is responsible 
for computing the sum of the numbers stored as part of the sum job.

The second endpoint allows the client to retrieve the result of its operation by 
querying the RESULT variable with the job id, and returning the result if available.

As expected, the reply of 100.0 is the sum of the numbers sent via the first call: 
42, 23, and 35. If the result is not available, the server would reply with a 
{"status": "waiting"} response.

Note: If the result is not computed by the time the request arrives, the server 
will reply with a {"status":"waiting"}. The client will have to try again. 
This method is often referred to as polling as it forces the client to regularly 
send requests to retrieve its final result. This is definitely not optimal, 
so two solutions are possible to improve this:

* Implement streaming as shown in the streaming lesson. It is possible to allow 
the client to connect to a special endpoint where the application will push the 
result as soon as it is available.
* Implement a webhook. The server should store a URL sent by the client with 
the numbers. This URL will then be called by the application with the result 
included. This model is referred to as push since it pushes the result to the 
client, as soon as they are ready, to the client. However, that requires the 
client to be able to receive such events by having a web server of its own running.
By using this design model, it can be ensured that the service can receive a 
substantial amount of job requests while being able to handle those tasks in 
the background. Obviously, adding numbers together is not very CPU intensive 
nowadays, but I am sure you can imagine heavier jobs that would profit from this design.
"""
