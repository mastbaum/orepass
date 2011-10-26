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

# map tokens (stored in cookies) to users
# this should be in a real database
users = {'asdf1234': 'bob'}

# couchdb singleton
couch = CouchDatabase('http://localhost:5984')

def orepass(environ, start_response):
    '''get json as if from a query directly to a couchdb server, but filtered
    based on in-document security settings.'''
    status = '501 NOT IMPLEMENTED'
    response_body = ''

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
                print couch[dbname].info()
                response_body = json.dumps(couch[dbname].info())
                status = '200 OK'
            except TypeError:
                status = '404 NOT FOUND'
            except couchdb.ResourceNotFound:
                status = '404 NOT FOUND'

        # access a document or built-in view
        if len(path) == 2:
            if path[1] == '_all_docs':
                view = couch[dbname].view('_all_docs', None, include_docs=True)
                result = {'total_rows': 0, 'offset': view.offset, 'rows': []}
                for row in view.rows:
                    print row['doc']
                    if not 'security' in row['doc'] or username in row['doc']['security']['readers']['names'] or username in row['doc']['security']['admins']['names']:
                        del row['doc']
                        result['rows'].append(row)
                        result['total_rows'] += 1
                    else:
                        print 'NOPE!'
                response_body = json.dumps(result)
                status = '200 OK'
            else:
                docid = path[1]
                print dbname, docid
                try:
                    if not 'security' in couch[dbname][docid] or username in couch[dbname][docid]['security']['readers']['names'] or username in couch[dbname][docid]['security']['admins']['names']:
                            response_body = json.dumps(couch[dbname][docid])
                            status = '200 OK'
                    else:
                        status = '401 FORBIDDEN'
                except TypeError:
                    status = '404 NOT FOUND'
                except couchdb.ResourceNotFound:
                    status = '404 NOT FOUND'

        # access an attachment


    response_headers = [('Content-Type', 'text/plain'),
                  ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]

# serve forever on localhost:8051
httpd = make_server('', 8051, orepass)
httpd.serve_forever()

