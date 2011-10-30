#!/usr/bin/env python

import re
import os
import sys
import json
from cgi import parse_qs
from wsgiref.simple_server import make_server

import render
import dbi

couch = dbi.CouchDatabase('http://localhost:5984')

# map tokens (stored in cookies) to users
# this should be in a real database
users = {'asdf1234': 'bob'}

def main(environ, start_response):
    '''get json as if from a query directly to a couchdb server, but filtered
    based on in-document security settings.'''

    render = render.Render(start_response)

    # determine user from browser cookie matched with server-side token
    try:
        cookies = parse_qs(environ['HTTP_COOKIE'])
        auth_token = cookies['optoken'][0]
        username = users[auth_token]
        print username
    except KeyError:
        username = ''

    path = environ['PATH_INFO'].lstrip(os.sep)

    # url expression to request handler map
    handler = {
        # server
        r'^': handlers.server.root,
        r'^_stats\/?$': handlers.server.stats,
        r'^_config\/?(?P<settings>.+)$': handlers.server.config,
        r'^_active_tasks\/?$': handlers.server.active_tasks,
        r'^_all_dbs\/?$': handlers.server.all_dbs,
        r'^_replicate\/?$': handlers.server.replicate,
        r'^_uuids\/$': handlers.server.uuids,
        r'^_session\/?$': handlers.server.session

        # database
        r'^(?P<dbname>\w+)\/?$': handlers.db.root

        # document

        # bulk document

        # view

        # show

        # list
    }

    try:
        h = handler[filter(lambda x: re.match(x, path), handler)[0]]
        return render.render_response(*h(couch, environ, username))
    except IndexError:
        # no match
        raise

# serve forever on localhost:8051
httpd = make_server('', 8051, main)
httpd.serve_forever()

