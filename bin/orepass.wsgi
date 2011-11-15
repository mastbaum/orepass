#!/usr/bin/env python

import re
import os
import sys
from cgi import parse_qs
from wsgiref.simple_server import make_server

import orepass.core.render
import orepass.core.resource

import orepass.handlers.auth
import orepass.handlers.server
import orepass.handlers.database
import orepass.handlers.document
import orepass.handlers.bulk_document
import orepass.handlers.view
import orepass.handlers.list_function
import orepass.handlers.show_function

# open db connection as administrator
couch = orepass.core.resource.Resource('http://adminuser:adminpass@localhost:5984')

# map tokens (stored in cookies) to users
# this should be in a real database
users = {'asdf1234': 'mastbaum'}

# url expression to request handler function map
handler = {
    # authentication
    r'^_cookie\/?$': orepass.handlers.auth.cookie_me,

    # server
    r'^\/?$': orepass.handlers.server.root,
    r'^_stats\/?$': orepass.handlers.server.stats,
    r'^_config\/(?P<settings>.+)\/?$': orepass.handlers.server.config,
    r'^_active_tasks\/?$': orepass.handlers.server.active_tasks,
    r'^_all_dbs\/?$': orepass.handlers.server.all_dbs,
    r'^_replicate\/?$': orepass.handlers.server.replicate,
    r'^_uuids\/?$': orepass.handlers.server.uuids,
    r'^_session\/?$': orepass.handlers.server.session,

    # database
    r'^(?P<dbname>\w+)\/?$': orepass.handlers.database.root,
    r'^(?P<dbname>\w+)\/_revs_limit\/?$': orepass.handlers.database.revs_limit,
    r'^(?P<dbname>\w+)\/_compact\/?$': orepass.handlers.database.compact,
    r'^(?P<dbname>\w+)\/_changes\/?$': orepass.handlers.database.changes,

    # document
    r'^(?P<dbname>\w+)\/(?!_)(?P<docid>\w+)\/?$': orepass.handlers.document.root,
    r'^(?P<dbname>\w+)\/(?!_)(?P<docid>\w+)\/(?P<attach>.+)$': orepass.handlers.document.attachment,
    r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/?$': orepass.handlers.document.design,
    r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/(?P<attach>.+)$': orepass.handlers.document.design_attachment,

    # bulk document
    r'^(?P<dbname>\w+)\/_all_docs\/?$': orepass.handlers.bulk_document.all_docs,
    r'^(?P<dbname>\w+)\/_bulk_docs\/?$': orepass.handlers.bulk_document.bulk_docs,

    # view
    r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/_view/(?P<view>\w+)\/?$': orepass.handlers.view.view,
    r'^(?P<dbname>\w+)\/_temp_view\/?$': orepass.handlers.view.temp_view,
    r'^(?P<dbname>\w+)\/_view_cleanup\/?$': orepass.handlers.view.view_cleanup,
    r'^(?P<dbname>\w+)\/_compact\/(?P<design>\w+)\/?$': orepass.handlers.view.compact,

    # show
    r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/_show/(?P<show>\w+)\/(?P<docid>\w+)\/?$': orepass.handlers.show_function.show_function,

    # list
    r'^(?P<dbname>\w+)\/_design\/(?P<design>\w+)\/_list/(?P<list>\w+)\/(?P<view>\w+)\/?$': orepass.handlers.list_function.list_function
}

def main(env, start_response):
    '''get json as if from a query directly to a couchdb server, but filtered
    based on in-document security settings.'''

    renderer = orepass.core.render.Renderer(start_response)

    # determine user from browser cookie matched with server-side token
    try:
        cookies = parse_qs(env['HTTP_COOKIE'])
        auth_token = cookies['optoken'][0]
        username = users[auth_token]
    except KeyError:
        username = ''

    path = env['PATH_INFO'].lstrip(os.sep)

    try:
        h = handler[filter(lambda x: re.match(x, path), handler)[0]]
        print h
        return renderer.render_response(*h(couch, env, username))
    except (IndexError, TypeError):
        print 'unmatched path:', path
        return renderer.render_response(404, {}, '404 Not found :(')

# serve forever on localhost:8051
print 'orepass running on localhost:8051...'
httpd = make_server('', 8051, main)
httpd.serve_forever()

