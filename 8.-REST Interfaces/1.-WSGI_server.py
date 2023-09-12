"""
The WSGI Protocol

Before considering a REST API, one needs to know the first layer of abstraction
of the Python world when HTTP is involved: WSGI.

WSGI

WSGI stands for Web Server Gateway Interface. It started its life as part of
PEP 0333, and was updated as part of PEP 3333. This PEP was designed to solve
the problem of mixing frameworks and web servers. It makes sure there is a
common protocol between web servers and web frameworks, so they are not
necessarily tied together. Indeed, it would be a shame to be forced to provide
a web server for each framework, wherein there is already a vast collection of
likely better alternatives out there.

The WSGI protocol is pretty easy to understand, and this understanding is also
valuable as all Python frameworks are based on it.

When a WSGI web server loads an application, it looks for an application object
that is callable. Calling this object must return a result that is shipped back
to the HTTP client.

The callable must be named application and will receive two arguments: a dict
filled with environment keys and values named environ, and a function named
start_response. The WSGI application must use the latter to send the status and
headers reply to the client, as demonstrated in the following example.

def application(environ, start_response):
    #Simplest possible application object
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']

A web development framework plugs itself in at this stage by providing the
application object and letting the developer concentrate on the implementation
of its business logic.

The WSGI specification has been built so applications implementing the WSGI
protocol could be stacked. Some applications implement both sides of the WSGI
protocol and are called middleware: that means they can handle a request and
then pass it to the next WSGI application in the pipeline (if needed). You can,
therefore, chain WSGI middlewares to do pre-processing (e.g., ACL management,
rate limiting, etc.) until the pipeline reaches the actual WSGI application.
"""
from wsgiref.simple_server import make_server


def application(environ, start_response):
    """Return the environ keys as text/plain"""
    body = "\n".join(
        ["%s: %s" % (key, value) for key, value in sorted(environ.items())]
    )

    start_response(
        "200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))]
    )

    return [body.encode()]


# Instantiate the server
httpd = make_server("localhost", 10000, application)
# Wait for a single request, serve it and quit
httpd.handle_request()
# Run `curl -v http://localhost:10000' to see the request and reply

"""
To run the following example, click Run and then use the command 
< python wsgi-server.py >. Then, run curl -v http://localhost:10000 from the 
second terminal to see the request and reply.
"""

"""
While completely functional, the wsgiref server should probably be avoided for 
any serious use. It is very limited and neither offers good performance nor fine 
tuning, both of which are usually required when deploying production systems.

WSGI servers
There are some other WSGI servers that you can use:

* The most famous is Apache httpd and its mod_wsgi companion. Both are well tested 
and have been supported for years, so this is one of the safest choices. They 
allow a variety of combinations when deploying, such as deploying several WSGI 
applications on the same port with different paths. A small downside though is 
that restarting the httpd process to reload the configuration usually restarts 
all the services, which might be a problem if you deploy several WSGI applications 
with the same httpd process.
* Gunicorn (Green Unicorn). It is relatively easy to use and deploy.
* Waitress is a pure-Python HTTP server.
* uWSGI is a very complete and very fast WSGI server – it is probably my favorite. 
It is a bit harder to use and configure as it presents a lot of configuration 
options and supports more than just WSGI. However, only a few options are needed 
to have a working application. It even supports HTTP 2 and other programming 
languages (Perl, Ruby, Go, etc.).
"""
