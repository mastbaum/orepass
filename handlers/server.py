import http
import couchdb

def root(couch):
    if environ['REQUEST_METHOD'] == 'GET' or environ['REQUEST_METHOD'] == 'HEAD':
        try:
            return http.status[200], json.dumps(couch[dbname].info())
        except (TypeError, couchdb.ResourceNotFound):
            return http.status[404],
    return http.status[405]



