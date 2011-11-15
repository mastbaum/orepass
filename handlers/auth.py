def cookie_me(couch, env, username):
    '''get a valid user cookie, for testing purposes'''
    return 200, {'Set-cookie': 'optoken=asdf1234'}, 'Cooookies!'

