import http
import couchdb

def root(couchdb, environ, username):
    # HEAD|GET|PUT|DELETE; pass
    pass

def revs_limit(couchdb, environ, username):
    # HEAD|GET|PUT|DELETE; couch
    pass

def compact(couchdb, environ, username):
    # POST; couch
    pass

def changes(couchdb, environ, username):
    # HEAD|GET; filter (read)
    pass

