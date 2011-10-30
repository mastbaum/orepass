import couchdb

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

    def __getitem__(self, item):
        return self.couch.__getitem__(item)

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

    def get_doc_roles(self, doc, username):
        '''check if the user is permitted to see the document'''
        if not 'security' in doc:
            return 'admin' # admin party!
        if username in doc['security']['admins']['names']:
            return 'admin'
        if username in doc['security']['readers']['names']:
            return 'reader'
