import re
import http
import urllib
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

    if env['REQUEST_METHOD'] not in ['GET','COPY','PUT','POST','DELETE']:
        return 501, {}, '501 Not implemented'

    status, headers, body = couch.get(path, headers=req_headers, **params)
    doc = json.loads(body)

    if env['REQUEST_METHOD'] == 'GET':
        if validate.validate_view_doc(doc, username):
            body = json.dumps(doc)
            return status, headers, body
        else:
            return 404, {}, '404 Not found'
    elif env['REQUEST_METHOD'] == 'COPY':
        if validate.validate_view_doc(doc, username):
            status, headers, body = couch.copy(path, headers=req_headers, **params)
            return status, headers, body
        else:
            return 404, {}, '404 Not found'
    elif env['REQUEST_METHOD'] == 'POST':
        if validate.validate_modify_doc(doc, username):
            try:
                req_length = int(env['CONTENT_LENGTH'])
                req_body = env['wsgi.input'].read(req_length)
            except ValueError:
                req_body = ''
            status, headers, body = couch.post(path, req_body, headers=req_headers, **params)
            return status, headers, body
        elif validate.validate_view_doc(doc, username):
            return 401, {}, '401 Forbidden'
        else:
            return 404, {}, '404 Not found'
    elif env['REQUEST_METHOD'] == 'DELETE':
        if validate.validate_modify_doc(doc, username):
            status, headers, body = couch.delete(path, headers=req_headers, **params)
            return status, headers, body
        elif validate.validate_view_doc(doc, username):
            return 401, {}, '401 Forbidden'
        else:
            return 404, {}, '404 Not found'
    elif env['REQUEST_METHOD'] == 'PUT':
        return 501, {}, '501 Not implemented'
    else:
        return 405, {}, ''

def attachment(couch, env, username):
    '''request handler for document attachment
    URL: /[dbname]/[docid]/[attachment]
    Methods: GET, COPY, PUT, POST
    Authentication: GET|COPY|PUT: Row filtering (read access)
                    POST|DELETE:  Row filtering (admin access)
    '''
    path = env['PATH_INFO'].lstrip('/')
    params = parse_qs(env['QUERY_STRING'] or '')

    match = re.match(r'^(?P<dbname>\w+)\/(?P<docid>\w+)\/(?P<attach>.+)$', path)
    doc_path = '/'.join([match.group('dbname'), match.group('docid')])

    if env['REQUEST_METHOD'] == 'GET':
        status, headers, body = couch.get(doc_path, headers={'Content-type': 'application/json'})
        doc = json.loads(body)
        if validate.validate_view_doc(doc, username):
            return couch.get(urllib.quote(path))
        else:
            return 404, {}, '404 Not found'

    return 501, {}, '501 Not implemented'

def design(couch, env, username):
    '''request handler for design document
    URL: /[dbname]/[docid]/_design/[designname]
    Methods: GET, COPY, PUT, POST
    Authentication: GET|COPY|PUT: Row filtering (read access)
                    POST|DELETE:  Row filtering (admin access)
    '''
    req_headers = {'Content-type': 'application/json'}
    path = env['PATH_INFO'].lstrip('/')
    params = parse_qs(env['QUERY_STRING'] or '')

    status, headers, body = couch.get(path, headers=req_headers, **params)
    doc = json.loads(body)

    if env['REQUEST_METHOD'] == 'GET':
        if validate.validate_view_doc(doc, username):
            body = json.dumps(doc)
            return status, headers, body
        else:
            return 404, {}, '404 Not found'

    return 501, {}, '501 Not implemented'

def design_attachment(couch, env, username):
    '''request handler for design document attachment
    URL: /[dbname]/[docid]/_design/[designname]/[attachment]
    Methods: GET, COPY, PUT, POST
    Authentication: GET|COPY|PUT: Row filtering (read access)
                    POST|DELETE:  Row filtering (admin access)
    '''
    path = env['PATH_INFO'].lstrip('/')
    params = parse_qs(env['QUERY_STRING'] or '')

    match = re.match(r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/(?P<attach>.+)$', path)
    doc_path = '/'.join([match.group('dbname'), '_design', match.group('design')])

    if env['REQUEST_METHOD'] == 'GET':
        status, headers, body = couch.get(doc_path, headers={'Content-type': 'application/json'})
        doc = json.loads(body)
        if validate.validate_view_doc(doc, username):
            return couch.get(urllib.quote(path))
        else:
            return 404, {}, '404 Not found'

    return 501, {}, '501 Not implemented'

