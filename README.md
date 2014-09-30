SatNOGS DB
==============================
SatNOGS DB is a transponder suggestions and crowd-sourcing ``couchApp`` created using ``CouchDB``, ``PouchDB`` and ``AngularJS``.

## Installation

* Clone this repository.
* Setup a ``couchDB`` instance and enable ``CORS``.
  * For your development environment you can use Iris Couch, a service that offers CouchDB instances with a free tier.
  * In order to enable ``CORS`` you can follow the instructions from the [official documentation](http://docs.couchdb.org/en/latest/config/http.html?highlight=cors#cross-origin-resource-sharing)
* Change the database details in``db.js`` according to your setup. 
* All the functionality is implemented in client-side. That practically means that in order to deploy ``satnogs-db`` you only need to serve the static files. For development purposes we suggest to use python development server in the top level directory of the project:
  * ``python -m SimpleHTTPServer 8000``

LICENSE: MPL-2.0
