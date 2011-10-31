import http
from cgi import parse_qs

def list_function(couch, environ, username):
    # HEAD|GET; blacklist
    return 501, {}, '501 Not implemented'

