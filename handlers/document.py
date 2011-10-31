import http
import json
from cgi import parse_qs
import validate

def root(couch, env, username):
    '''request handler for document
    URL: /[dbname]/[docid]
    Methods: GET, COPY, PUT, POST
    Authentication: GET|COPY|PUT: Row filtering (read access)
                    POST|DELETE:  Row filtering (admin access)
    '''
    req_headers = {'Content-type': 'application/json'}
    path = env['PATH_INFO'].lstrip('/')
    params = parse_qs(env['QUERY_STRING'] or '')

    if env['REQUEST_METHOD'] == 'GET':
        status, headers, body = couch.get(path, headers=req_headers, **params)

        doc = json.loads(body)
        if validate.validate_view_doc(doc, username):
            body = json.dumps(doc)
            #del headers['transfer-encoding']
            return status, headers, body
        else:
            return 404, {}, '404 Not found'

    return 501, {}, '501 Not implemented'

def attachment(couch, env, username):
    # HEAD|GET; filtered (read)
    # PUT|DELETE; filtered (admin)
    return 501, {}, '501 Not implemented'

def design(couch, env, username):
    # HEAD|GET|COPY; filtered (read)
    # PUT; filtered (db write)
    # POST|DELETE; filtered (admin)
    return 501, {}, '501 Not implemented'

def design_attachment(couch, env, username):
    # HEAD|GET; filtered (read)
    # PUT|DELETE; filtered (admin)
    return 501, {}, '501 Not implemented'

