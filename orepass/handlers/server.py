import http
from cgi import parse_qs

def root(couch, env, username):
    '''request handler for database root
    URL: /
    Methods: GET
    Authentication: None
    '''
    if env['REQUEST_METHOD'] == 'GET':
        req_headers = {'Content-type': 'application/json'}
        status, headers, body = couch.get('', headers=req_headers)
        return status, headers, body
    return 405,

def stats(couch, env, username):
    '''request handler for database statistics
    URL: /_stats
    Methods: GET
    Authentication: HTTP Authorization pass-through
    '''
    if env['REQUEST_METHOD'] == 'GET':
        req_headers = {'Content-type': 'application/json'}
        if 'HTTP_AUTHORIZATION' in env:
            print 'auth'
            req_headers['Authorization'] = env['HTTP_AUTHORIZATION']
            status, headers, body = couch.get('_stats', headers=req_headers)
            return status, headers, body
    print 'noauth'
    return 401, {}, ''

def config(couch, env, username):
    # HEAD|GET|POST; couch
    # r'^_config\/(?P<settings>.+)\/?$'
    return 501, {}, '501 Not implemented'

def active_tasks(couch, env, username):
    # HEAD|GET; couch
    return 501, {}, '501 Not implemented'

def all_dbs(couch, env, username):
    # HEAD|GET; pass
    return 501, {}, '501 Not implemented'

def replicate(couch, env, username):
    # HEAD|POST; pass
    return 501, {}, '501 Not implemented'

def uuids(couch, env, username):
    '''retreive one or more uuids from the server
    URL: /_uuids
    Methods: GET
    Authentication: None
    '''
    params = parse_qs(env['QUERY_STRING'] or '')
    if env['REQUEST_METHOD'] == 'GET':
        req_headers = {'Content-type': 'application/json'}
        status, headers, body = couch.get('_uuids', headers=req_headers, **params)
        return status, headers, body
    return 405, {}, ''

def session(couch, env, username):
    '''request handler for couchdb session information
    URL: /_session
    Methods: GET, DELETE, POST
    Authentication: HTTP Authorization pass-through
    '''
    req_headers = {'Content-type': 'application/json'}
    params = parse_qs(env['QUERY_STRING'] or '')
    if 'HTTP_AUTHORIZATION' in env:
        req_headers['Authorization'] = env['HTTP_AUTHORIZATION']
    else:
        req_headers['Authorization'] = ''

    if env['REQUEST_METHOD'] == 'GET':
        status, headers, body = couch.get('_session', headers=req_headers, **params)
        return status, headers, body
    elif env['REQUEST_METHOD'] == 'POST':
        try:
            req_length = int(env['CONTENT_LENGTH'])
            req_body = env['wsgi.input'].read(req_length)
        except ValueError:
            req_body = ''
        status, headers, body = couch.post('_session', req_body, headers=req_headers, **params)
        return status, headers, body
    elif env['REQUEST_METHOD'] == 'DELETE':
        status, headers, body = couch.delete('_session', headers=req_headers, **params)
        return status, headers, body
    return 405, {}, ''

