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
    collections = ListField(DictField(Mapping.build(
        collectionname = TextField(),
        added = DateTimeField(),
        version = TextField(),
        rings = ListField(DictField(Mapping.build(
            layer = IntegerField(),
            ringname = TextField(),
            version = TextField()
            )))
        )))
    rings = ListField(DictField(Mapping.build(
        ringname = TextField(),
        version = TextField(),
        count = IntegerField(),
        added = DateTimeField(default=datetime.now)
    	)))