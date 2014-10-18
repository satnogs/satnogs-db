var remote_db_url = 'http://178.62.230.53:5984/satnogs-db';

var db = new PouchDB('satnogs-db');
var remote_db = new PouchDB(remote_db_url);

PouchDB.sync('satnogs-db', remote_db_url, {live: true});
