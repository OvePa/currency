"""
Running uWSGI server
The next example shows how to deploy a simple application with uWSGI.

To run the application below, use command
<uwsgi --http :9090 --master --wsgi-file wsgi-application.py> to run the server.
Then, open another terminal and use command
<curl -v http://localhost:9090> to communicate with the wsgi server.
"""


def application(environ, start_response):
    """Simplest possible application object"""
    status = "200 OK"
    response_headers = [("Content-type", "text/plain")]
    start_response(status, response_headers)
    response_str = "Hello world!\n"
    return [response_str.encode()]


"""
The performance of your WSGI server is going to be important if you need to 
scale your HTTP application to support a large number of clients. There is 
certainly no go-to solution that can fit all use cases. You will have to benchmark 
your different use cases and see what is the best fit. If you do not need any 
of the fancy features that Apache httpd provides, uWSGI or Gunicorn are probably 
good picks.
"""
