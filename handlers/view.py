import http
import json
from cgi import parse_qs

def validate_view_doc(doc, username):
    '''check if the user is permitted to see the document'''
    if not 'security' in doc:
        # FIXME: whitelist by default
        return True
    if username in doc['security']['readers']['names']:
        return True
    if username in doc['security']['admins']['names']:
        return True
    return False

def view(couch, env, username):
    '''request handler for view
    URL: /[dbname]/_design/[designname]/_view/[viewname]
    Methods: GET
    Authentication: Row filtering (read access)
    '''
    if env['REQUEST_METHOD'] == 'GET':
        req_headers = {'Content-type': 'application/json'}
        path = env['PATH_INFO'].lstrip('/')
        params = {'include_docs': True}
        params.update(parse_qs(env['QUERY_STRING'] or ''))
        status, headers, body = couch.get(path, headers=req_headers, **params)

        # select only rows allowed by access control
        view = json.loads(body)
        result = {'total_rows': 0, 'offset': view['offset'], 'rows': []}
        for row in view['rows']:
            if validate_view_doc(row['doc'], username):
                del row['doc'] # FIXME: unless user asked for it in query
                result['rows'].append(row)
                result['total_rows'] += 1
        body = json.dumps(result) # fixme leave as a list

        del headers['transfer-encoding']
        return status, headers, body
    return 405, {}, ''

def temp_view(couchdb, environ, username):
    # POST; couch
    pass

def view_cleanup(couchdb, environ, username):
    # POST; couch
    pass

def compact(couchdb, environ, username):
    # POST; couch
    pass

