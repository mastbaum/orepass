import orepass.handlers.http

class Renderer():
    def __init__(self, start_response):
        self.start_response = start_response
    def render_response(self, status, response_headers={}, response_body=''):
        '''generate an http response from status code and body'''
        # remove hop-by-hop headers, which httplib doesn't like
        if 'transfer-encoding' in response_headers:
            del response_headers['transfer-encoding']
        response_headers['content-length'] = str(len(response_body))
        response_headers = zip(*(response_headers.keys(), response_headers.values()))
        try:
            status = orepass.handlers.http.status[status]
        except KeyError:
            status = str(status) + ' UNKNOWN'
        self.start_response(status, response_headers)
        return [response_body]

