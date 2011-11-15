def validate_view_doc(doc, username):
    '''check if the user is permitted to see the document'''
    if not 'security' in doc:
        # FIXME: whitelist by default
        return True
    if username in doc['security']['readers']['names']:
        return True
    if username in doc['security']['admins']['names']:
        return True
    return False

