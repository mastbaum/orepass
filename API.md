Introduction
============
orepass aims to wrap all of the CouchDB API features that can be implemented in a safe way. Requests to whitelisted URLs and those that CouchDB aleady authenticates are passed through directly. Requests for which filtering makes sense (documents, shows, and views), orepass will apply its access control rules. Requests which CouchDB allows that cannot be access-controlled are deniedwith an appropriate HTTP client error. Unavailable and blacklisted URLs result in a 404 error.

HTTP responses and status codes are generally constructed to look like normal CouchDB responses -- it is important that the user not know that they are getting 206 Partial Content. orepass tries to be as transparent as possible.

CouchDB Server API
====================
The server API provides access to server configuration data and operations, and is generally useful to administrators but not the general public. If CouchDB does not already provide authentication, orepass will pass through HTTP authentication headers to allow CouchDB admin users, but return 404 instead of 401 if authentication fails.

[HEAD|GET] /
------------
Returns the welcome message and version

Authentication: Blacklisted by default

[HEAD|GET] /_config
-------------------
Gets CouchDB server configuration information

Authentication: CouchDB authenticates

[HEAD|GET] /_stats
------------------
Returns server statistics

Authentication: HTTP pass-through with 404 on failure

POST /_config/[settings]
------------------------
Modify CouchDB server configuration

Authentication: CouchDB authenticates

GET /_active_tasks
------------------
A list of all active tasks.

Authentication: CouchDB authenticates

[HEAD|GET] /_all_dbs
--------------------
A list of all databases

Authentication: HTTP pass-through with 404 on failure

[HEAD|POST] /_replicate
------------------------
Start, stop, or configure a database replication operation

Authentication: HTTP pass-through with 404 on failure

GET /_uuids
-----------
Fetches one or more UUIDs

Authentication: None

[GET|HEAD|DELETE|POST] /_session
--------------------------------
Get and set session information

Authentication: None (used for CouchDB authentication)

CouchDB Database API
====================
The database API defines interaction with individual databases. Users generally need do not require database-level access. CouchDB provides good database-level security, which is configurable through Futon or /dbname/_security. If CouchDB does not already provide authentication, orepass will pass through HTTP authentication headers to allow CouchDB admin users, but return 404 instead of 401 if authentication fails.

[HEAD|GET] /dbname/
-------------------
Get information about a database

Authentication: HTTP pass-through with 404 on failure

[PUT|DELETE] /dbname/
---------------------
Create or delete a new database

Authentication: CouchDB authenticates

[PUT|DELETE] /dbname/_[db option]
---------------------------------
Set a database option. Currently CouchDB supports only "_revs_limit".

Authentication: CouchDB authenticates

[HEAD|GET] /dbname/_[db option]
-------------------------------
Get the value of a database option.

Authentication: HTTP pass-through with 404 on failure

POST /dbname/_compact
----------------------
Starts compaction of the database (removing unused sections and old revisions)

Authentication: CouchDB authenticates

GET /dbname/_changes
--------------------
Returns a list or stream of changes made to the database

Authentication: Row filtering (read access)

CouchDB Document API
====================
The document API defines how documents within a database are accessed. orepass filters CouchDB responses based on user context and in-document access control lists, providing modified reponses that contain only that which the requester is authorized to see.

[HEAD|GET|COPY] /dbname/docid
-----------------------------
Retrieve or copy the document with id "docid"

Authentication: Filtered (read or admin access)

PUT /dbname/docid
-----------------
Create a document with id "docid"

Authentication: Filtered (DB write access)

[POST|DELETE] /dbname/docid
-------------------------------
Modify, or delete the document with id "docid"

Authentication: Filtered (admin access)

[HEAD|GET] /dbname/docid/attachment
-----------------------------------
Read a file attached to a document

Authentication: Filtering (read access)

[PUT|DELETE] /dbname/docid/attachment
-------------------------------------
Add or remove an attachment from a document

Authentication: Filtering (admin access)

CouchDB Bulk Document API
=========================
The bulk document API allows one to fetch or put several documents in a single HTTP request.

GET /dbname/_all_docs
---------------------
See a built-in view returning all documents in the database ordered by _id

Authentication: Row filtering (read access)

POST /dbname/_bulk_docs
-----------------------
Creates several documents

Authentication: Filtered (DB write access)

CouchDB View API
================
CouchDB views return a pre-computed list of documents sorted by a set of keys. Using in-document access control information, orepass filters view results to remove rows to which the requester does not have access.

GET /dbname/_design/designname/_view/viewname
---------------------------------------------
Get all rows returned from a view

Authentication: Row filtering (read access)

POST /dbname/_temp_view
-----------------------
Execute a single-use view

Authentication: CouchDB authentication

POST /dbname/_view_cleanup
--------------------------
Remove old view output cached on disk

Authentication: CouchDB authentication

POST /dbname/_compact/designname
--------------------------------
Remove unused sections and old revisions from view results in a given design document

Authentication: CouchDB authentication

CouchDB List and Show Functions
===============================
Added in CouchDB 0.9, show and list functions allow parsing and formatting of documents and view results, respectively. They are commonly used for converting from JSON to other formats, such as HTML for rendering. Although cacheable, shows and lists cannot be precomputed like views because their input depends on run-time (e.g. query string) options.

Show functions
--------------
Show functions operate on a single document, typically transforming its format before returning it to the requester. orepass will render shows if reading input document is permitted by access control requirements. Otherwise, a 404 is returned.

GET /dbname/_design/designname/_show/showname/docid

Authentication: Filtering (read access)

List functions
--------------
List functions operate on view results, which are passed internally in CouchDB and cannot be intercepted for filtering. Therefore, there is no way to guarantee that list functions will not leak data to unauthorized users, and list function URLs are blacklisted by default in orepass. Developers are advised to approach list functions with extreme caution.

GET /dbname/_design/designname/_list/listname/viewname

Authentication: Blacklisted by default

