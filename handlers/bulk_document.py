import http
from cgi import parse_qs

def all_docs(couch, environ, username):
    # HEAD|GET; row filtering (read)
    return 501, {}, '501 Not implemented'

def bulk_docs(couch, environ, username):
    # POST; filter (db write)
    return 501, {}, '501 Not implemented'

