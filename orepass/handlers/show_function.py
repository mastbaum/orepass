import http
from cgi import parse_qs

def show_function(couch, environ, username):
    # HEAD|GET; filtering (read)
    return 501, {}, '501 Not implemented'

