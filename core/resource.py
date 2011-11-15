import httplib
import urllib
import re
import base64

class Resource():
    def __init__(self, url):
        '''connect to db based on standard-formatted url string'''
        match = re.match(r'((?P<protocol>.+):\/\/)?((?P<user>.+):(?P<pw>.+)?@)?(?P<host>.+)\/?$', url)
        if not match:
            raise ValueError('Error in URL string')
        self.protocol = match.group('protocol')
        self.host = match.group('host')
        self.headers = {'Authorization': 'Basic %s' % base64.encodestring('%s:%s' % (match.group('user'), match.group('pw')))}

    def connect(self):
        '''open an http(s) connection to this couchdb server'''
        if self.protocol == 'https':
            conn = httplib.HTTPSConnection(self.host)
        else:
            conn = httplib.HTTPConnection(self.host)
        return conn

    def request(self, method, url, body='', headers={}, **params):
        '''execute an http request to this couchdb server. params are built into
        the query string.'''
        # build headers and url
        all_headers = self.headers.copy()
        all_headers.update(headers or {})
        url = urljoin('', url, **params)
        print url

        # make the request
        conn = self.connect()
        conn.request(method, url, body, all_headers)
        resp = conn.getresponse()

        # parse the response
        status = resp.status
        headers = dict(resp.getheaders())
        body = resp.read()
        return status, headers, body

    # HTTP methods
    def delete(self, path=None, headers=None, **params):
        return self.request('DELETE', path, headers=headers, **params)

    def head(self, path=None, headers=None, **params):
        return self.request('HEAD', path, headers=headers, **params)

    def get(self, path=None, headers=None, **params):
        return self.request('GET', path, headers=headers, **params)

    def put(self, path=None, body=None, headers=None, **params):
        return self.request('PUT', path, body=body, headers=headers, **params)

    def copy(self, path=None, body=None, headers=None, **params):
        return self.request('COPY', path, body=body, headers=headers, **params)

    def post(self, path=None, body=None, headers=None, **params):
        return self.request('POST', path, body=body, headers=headers, **params)

def urlencode(data):
    if isinstance(data, dict):
        data = data.items()
    params = []
    for name, value in data:
        params.append((name, value))
    return urllib.urlencode(params)

def urljoin(base, *path, **query):
    if base and base.endswith('/'):
        base = base[:-1]
    retval = [base]

    # build the path
    path = '/'.join([''] + [s for s in path])
    if path:
        retval.append(path)

    # build the query string
    params = []
    for name, value in query.items():
        if type(value) in (list, tuple):
            params.extend([(name, i) for i in value if i is not None])
        elif value is not None:
            if value is True:
                value = 'true'
            elif value is False:
                value = 'false'
            params.append((name, value))
    if params:
        retval.extend(['?', urlencode(params)])

    return ''.join(retval)

#r'((?P<protocol>.+):\/\/)?((?P<user>.+):(?P<pw>.+)?@)?(?P<host>(\w|:)+)(\/?(\/(?P<path>.*)).)?((\?(?P<qs>.+)?)).?$'

# copy headers to pass through
#        if env['HTTP_AUTHORIZATION']:
#            self.headers['Authorization'] = 'Basic %s' % env['HTTP_AUTHORIZATION']}
#        if env['CONTENT_TYPE']:
#            self.headers['Content-type'] = env['CONTENT_TYPE']
#        if env['HTTP_USER_AGENT']:
#            self.headers['User-Agent'] = env['HTTP_USER_AGENT']

# security
#    def get_doc_roles(self, doc, username):
#        '''check if the user is permitted to see the document'''
#        if not 'security' in doc:
#            return 'admin' # admin party!
#        if username in doc['security']['admins']['names']:
#            return 'admin'
#        if username in doc['security']['readers']['names']:
#            return 'reader'

