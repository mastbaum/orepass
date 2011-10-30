class Renderer():
    def __init__(self, start_response):
        self.start_response = start_response
    def render_response(status, response_body=''):
        '''generate an http response from status code and body'''
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))
        ]
        self.start_response(status, response_headers)
        return [response_body]

