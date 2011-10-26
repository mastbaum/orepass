#! /usr/bin/env python

import re
import os
import sys
import json
import couchdb
from cgi import parse_qs
from wsgiref.simple_server import make_server

class CouchDatabase():
    '''wrapper for couchdb providing some convenience methods'''
    def __init__(self, url):
        '''connect to db based on standard-formatted url string'''
        match = re.match(r'((?P<protocol>.+):\/\/)?((?P<user>.+):(?P<pw>.+)?@)?(?P<host>.+)(:(?P<port>.+)).?', url)
        if not match:
            raise ValueError
        self.protocol = match.group('protocol')
        self.host = match.group('host')
        self.port = match.group('port')
        user = match.group('user')
        pw = match.group('pw')

        url = self.protocol + '://' + self.host + ':' + self.port
        self.couch = couchdb.Server(url)
        try:
            self.check_version()
        except couchdb.http.Unauthorized:
            self.authenticate(user, pw)
            self.check_version()

    def check_version(self, min_required='1.1.0'):
        '''check the version of the couchdb server. useful also for knowing if
        we're authenticated'''
        if self.couch.version() < min_required:
            print 'Error: couchdb version >=', min_required, 'required'
            sys.exit(1)

    def authenticate(self, user=None, pw=None):
        '''authentication with the couchdb module means setting a tuple.
        prompts the user for login information if necessary.'''
        if user is None or pw is None:
            print 'Authentication required for CouchDB database at', self.host
            user = raw_input('Username: ')
            pw = getpass.getpass('Password: ')
        self.couch.resource.credentials = (user, pw)

    def __getitem__(self, item):
        return self.couch.__getitem__(item)

    def validate_view_doc(self, doc, username):
        '''check if the user is permitted to see the document'''
        if not 'security' in doc:
            return True
        if username in doc['security']['readers']['names']:
            return True
        if username in doc['security']['admins']['names']:
            return True
        return False

    def get_validated(self, dbname, id, username):
        '''get only if the user has permission to read the document'''
        doc = self.couch[dbname][id]
        if self.validate_view_doc(doc, username):
            return doc
        raise couchdb.Unauthorized 

    def post_validated(self, dbname, id, username):
        '''post (save) only if the user has permission to modify the document'''
        if username in doc['security']['admins']['names']:
            # post
            pass
        # don't post

    def view_validated(self, dbname, viewname, username):
        '''return view results with only rows user is allowed to see'''
        view = self.couch[dbname].view(viewname, None, include_docs=True)
        result = {'total_rows': 0, 'offset': view.offset, 'rows': []}
        for row in view.rows:
            if self.validate_view_doc(row['doc'], username):
                del row['doc'] # (FIXME: unless user asked for it in query)
                result['rows'].append(row)
                result['total_rows'] += 1
        return result

# map tokens (stored in cookies) to users
# this should be in a real database
users = {'asdf1234': 'bob'}

# couchdb singleton
couch = CouchDatabase('http://localhost:5984')

def render_response(start_response, status, response_body=''):
    '''generate an http response from status code and body'''
    response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]

def main(environ, start_response):
    '''get json as if from a query directly to a couchdb server, but filtered
    based on in-document security settings.'''
    status = '501 NOT IMPLEMENTED'
    response_body = ''

    # determine user from browser cookie matched with server-side token
    try:
        cookies = parse_qs(environ['HTTP_COOKIE'])
        auth_token = cookies['optoken'][0]
        username = users[auth_token]
        print username
    except KeyError:
        username = ''

    path = environ['PATH_INFO'].lstrip(os.sep).split(os.sep, 3)
    dbname = path[0]
    if environ['REQUEST_METHOD'] == 'GET':
        # root of db
        if len(path) == 1:
            try:
                return render_response('200 OK', json.dumps(couch[dbname].info()))
            except TypeError:
                return render_response(start_response, '404 NOT FOUND')
            except couchdb.ResourceNotFound:
                return render_response(start_response, '404 NOT FOUND')

        if len(path) == 2:
            # built-in view
            if path[1] == '_all_docs':
                result = couch.view_validated(dbname, '_all_docs', username)
                return render_response(start_response, '200 OK', json.dumps(result))
            docid = path[1]

            # document
            try:
                doc = couch.get_validated(dbname, docid, username)
                return render_response(start_response, '200 OK', json.dumps(doc))
            except couchdb.Unauthorized:
                return render_response(start_response, '401 FORBIDDEN')
            except TypeError:
                return render_response(start_response, '404 NOT FOUND')
            except couchdb.ResourceNotFound:
                return render_response(start_response, '404 NOT FOUND')

# serve forever on localhost:8051
httpd = make_server('', 8051, main)
httpd.serve_forever()

