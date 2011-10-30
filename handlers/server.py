import http
import couchdb

def root(couch, environ, username):
    # HEAD|GET; none
    if environ['REQUEST_METHOD'] == 'GET' or environ['REQUEST_METHOD'] == 'HEAD':
        try:
            return http.status[200], json.dumps(couch[dbname].info())
        except (TypeError, couchdb.ResourceNotFound):
            return http.status[404],
    return http.status[405]

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

