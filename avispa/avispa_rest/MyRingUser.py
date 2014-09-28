# AvispaUser.py
from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, Mapping

class MyRingUser(Document):
    _id = TextField()
    firstname = TextField()
    lastname = TextField()
    email = TextField()
    salt = TextField()
    passhash = TextField()
    guid = TextField()
    added = DateTimeField(default=datetime.now)
    rings = ListField(DictField(Mapping.build(
        ringname = TextField(),
        version = TextField(),
        added = DateTimeField()
    	)))