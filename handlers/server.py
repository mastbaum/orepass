import http
import couchdb

def root(couch, env, username):
    # HEAD|GET; none
    if env['REQUEST_METHOD'] == 'GET':
        req_headers = {'Content-type': 'application/json'}
        status, headers, body = couch.get('', headers=req_headers)
    return status, headers, body

def stats(couch, environ, username):
    # HEAD|GET; pass
    pass

def config(couch, environ, username):
    # HEAD|GET|POST; couch
    # r'^_config\/(?P<settings>.+)\/?$'
    pass

def active_tasks(couch, environ, username):
    # HEAD|GET; couch
    pass

def all_dbs(couch, environ, username):
    # HEAD|GET; pass
    pass

def replicate(couch, environ, username):
    # HEAD|POST; pass
    pass

def uuids(couch, environ, username):
    # HEAD|GET; none
    pass

def session(couch, environ, username):
    # GET|HEAD|DELETE|POST; none
    pass

