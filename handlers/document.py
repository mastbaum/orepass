import http
from cgi import parse_qs

def root(couch, environ, username):
    # HEAD|GET|COPY; filtered (read)
    # PUT; filtered (db write)
    # POST|DELETE; filtered (admin)
    return 501, {}, '501 Not implemented'

def attachment(couch, environ, username):
    # HEAD|GET; filtered (read)
    # PUT|DELETE; filtered (admin)
    return 501, {}, '501 Not implemented'

def design(couch, environ, username):
    # HEAD|GET|COPY; filtered (read)
    # PUT; filtered (db write)
    # POST|DELETE; filtered (admin)
    return 501, {}, '501 Not implemented'

def design_attachment(couch, environ, username):
    # HEAD|GET; filtered (read)
    # PUT|DELETE; filtered (admin)
    return 501, {}, '501 Not implemented'

