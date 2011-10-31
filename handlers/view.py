import http
import json
from cgi import parse_qs
import validate

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
            if validate.validate_view_doc(row['doc'], username):
                del row['doc'] # FIXME: unless user asked for it in query
                result['rows'].append(row)
                result['total_rows'] += 1
        body = json.dumps(result) # fixme leave as a list

        del headers['transfer-encoding']
        return status, headers, body
    return 405, {}, ''

def temp_view(couch, environ, username):
    # POST; couch
    return 501, {}, '501 Not implemented'

def view_cleanup(couch, environ, username):
    # POST; couch
    return 501, {}, '501 Not implemented'

def compact(couch, environ, username):
    # POST; couch
    return 501, {}, '501 Not implemented'

