import http
import couchdb

def root(couchdb, environ, username):
    # HEAD|GET|COPY; filtered (read)
    # PUT; filtered (db write)
    # POST|DELETE; filtered (admin)
    pass

def attachment(couchdb, environ, username):
    # HEAD|GET; filtered (read)
    # PUT|DELETE; filtered (admin)
    pass

def design(couchdb, environ, username):
    # HEAD|GET|COPY; filtered (read)
    # PUT; filtered (db write)
    # POST|DELETE; filtered (admin)
    pass

def design_attachment(couchdb, environ, username):
    # HEAD|GET; filtered (read)
    # PUT|DELETE; filtered (admin)
    pass

