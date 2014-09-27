var db = new PouchDB('satnogs-db');
var remote_db = 'http://178.62.230.53:5984/satnogs-db';
PouchDB.sync('satnogs-db', remote_db, {live: true});
