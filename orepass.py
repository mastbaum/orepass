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
        r'^_config\/(?P<settings>.+)\/?$': handlers.server.config,
        r'^_active_tasks\/?$': handlers.server.active_tasks,
        r'^_all_dbs\/?$': handlers.server.all_dbs,
        r'^_replicate\/?$': handlers.server.replicate,
        r'^_uuids\/$': handlers.server.uuids,
        r'^_session\/?$': handlers.server.session,

        # database
        r'^(?P<dbname>\w+)\/?$': handlers.database.root,
        r'^(?P<dbname>\w+)\/_revs_limit\/?$': handlers.database.revs_limit,
        r'^(?P<dbname>\w+)\/_compact\/?$': handlers.database.compact,
        r'^(?P<dbname>\w+)\/_changes\/?$': handlers.database.changes,

        # document
        r'^(?P<dbname>\w+)\/(?P<docid>\w+)\/?$': handlers.document.root,
        r'^(?P<dbname>\w+)\/[^\_](?P<docid>\w+)\/(?P<attach>.+)$': handlers.document.attachment,
        r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/?$': handlers.document.design,
        r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/(?P<attach>.+)$': handlers.document.design_attachment,

        # bulk document
        r'^(?P<dbname>\w+)\/_all_docs\/?$': handlers.bulk_document.all_docs,
        r'^(?P<dbname>\w+)\/_bulk_docs\/?$': handlers.bulk_document.bulk_docs

        # view
        r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/_view/(?P<view>\w+)\/?$': handlers.view.view,
        r'^(?P<dbname>\w+)\/_temp_view\/?$': handlers.view.temp_view,
        r'^(?P<dbname>\w+)\/_view_cleanup\/?$': handlers.view.view_cleanup,
        r'^(?P<dbname>\w+)\/_compact\/(?P<design>\w+)\/?$': handlers.view.compact,

        # show
        r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/_show/(?P<show>\w+)\/(?P<docid>\w+)\/?$': handlers.show_function.show_function,

        # list
        r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/_list/(?P<list>\w+)\/(?P<view>\w+)\/?$': handlers.list_function.list_function
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

