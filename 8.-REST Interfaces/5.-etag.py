"""
Using ETag

An ETag, abbreviated from entity tag, is a header part of the HTTP standard.
It allows a client to make conditional requests using its cache, limiting
bandwidth and usage of server resources.

When a client sends a request to a server, the latter can reply with a response
including an ETag header. Common methods of ETag generation include using a
collision-resistant hash function of the resource’s content, a hash of the last
modification timestamp, or even just a revision number.

The below terminal demonstrates a server reply with an ETag header. Run the
terminal provided below to see the etag header in http response from
http://httpbin.org/etag.
"""
"""
If the ETag of the URL matches the value given in the If-None-Match header, 
the HTTP status code returned is 304 Not Modified, and no content is returned 
by the server. The client thus knows that the content did not change on the 
server, and it can use its cached copy.

Ideally, the computing of your ETag should be minimal in order to make it 
possible to save both CPU usage and network bandwidth. For a file, a simple 
ETag could be computed from the timestamp when the document has last been 
modified combined with its size since they are both available at a low cost 
from the operating system using a single stat call (or equivalent). A more robust 
ETag could be generated from computing the MD5 hash of the data about to be 
returned. However, this could be way more expensive, especially if the amount 
of data is large. Be creative.
"""
