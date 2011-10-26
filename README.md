orepass
=======

This is a collection of python middleware tools for making couchdb actually usable.

orepass.py is a wsgi server that can add per-document authentication to couchdb. documents contain a field "security" formatted as for the database:

    "security": {
        "admins": {
            "names": [],
            "roles": []
        },
        "readers": {
            "names": [],
            "roles": []
        }
    }

"names" and "roles" are lists of strings. "roles" is currently not implemented. "names" match a username derived from a cookie-based authentication token, which is stored by the client browser and the server.

Requests for couchdb documents, specifically "GET /dbname/docid" will return the document if the user is authorized or a 401 error if not.

