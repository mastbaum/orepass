import handlers.http

class Renderer():
    def __init__(self, start_response):
        self.start_response = start_response
    def render_response(self, status, response_headers=[], response_body=''):
        '''generate an http response from status code and body'''
        response_headers = zip(*(response_headers.keys(), response_headers.values()))
        try:
            status = handlers.http.status[status]
        except KeyError:
            status = str(status) + ' UNKNOWN'
        self.start_response(status, response_headers)
        return [response_body]

