import http
from cgi import parse_qs

def root(couch, env, username):
    '''request handler for the root of a database
    URL: /[dbname]
    Methods: GET
    Authentication: HTTP Authorization pass-through
    '''
    path = env['PATH_INFO'].lstrip('/')
    params = parse_qs(env['QUERY_STRING'] or '')
    if env['REQUEST_METHOD'] == 'GET':
        req_headers = {'Content-type': 'application/json'}
        if 'HTTP_AUTHORIZATION' in env:
            req_headers['Authorization'] = env['HTTP_AUTHORIZATION']
            status, headers, body = couch.get(path, headers=req_headers, **params)
            return status, headers, body
    return 401, {}, ''

def revs_limit(couch, env, username):
    # HEAD|GET|PUT|DELETE; couch
    return 501, {}, '501 Not implemented'

def compact(couch, env, username):
    # POST; couch
    return 501, {}, '501 Not implemented'

def changes(couch, env, username):
    # HEAD|GET; filter (read)
    return 501, {}, '501 Not implemented'

