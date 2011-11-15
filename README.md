orepass
=======

orepass is a Python WSGI middleware layer for making CouchDB actually usable in the wild.

CouchDB's architecture makes per-document security impossible -- users are defined as "readers" or "admins" at the database level, and "readers" have permission to read the entire database and create and edit documents. The "official" solution to this problem is to create a database for every access control group. However, in most applications the relevant access control group is a single user. Filtered replication to duplicate content for many users is not a scalable approach in many cases.

orepass instead adds per-document authentication to CouchDB. Documents are filtered based on a field "security" formatted as for the database:

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

where "names" and "roles" are lists of strings. "roles" is currently not implemented. "names" match a username derived from a cookie-based authentication token, which is stored by the client browser and the server.

Requests for documents, view, shows, and configuration data are subject to authentication. Documents are returned (or modified, deleted, etc.) if the user has appropriate credentials. Views return only rows for documents the user has permission to view. In cases where CouchDB already provides HTTP authentication, orepass will funnel requests through passively.

This approach, of course, sacrifices much of the speed of CouchDB. However, all other attempts to enforce access control will suffer similarly. Multiple databases will involve multiple queries, etc. Preliminary tests suggest that the delay added by orepass is insignificant compared to typical network latency.

