var db = new PouchDB('satnogs-db');
var remote_db = 'http://178.62.230.53:5984/satnogs-db';
var opts = {
  live: true
};

db.replicate.to(remote_db, opts);
db.replicate.from(remote_db, opts);
