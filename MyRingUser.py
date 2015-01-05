# AvispaUser.py
from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, BooleanField, Mapping

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
        count = IntegerField(),
        added = DateTimeField(default=datetime.now)
    	)))
    collections = ListField(DictField(Mapping.build(
        collectionname = TextField(),
        collectiondescription = TextField(),
        version = TextField(),
        added = DateTimeField(default=datetime.now),
        rings = ListField(DictField(Mapping.build(
            handle = TextField(),
            ringname = TextField(),
            version = TextField(),
            layer = IntegerField()
            )))
        )))
    is_active = BooleanField(default=True)
    is_authenticated = BooleanField(default=False)
    new_password_key = TextField()
    new_password_requested = DateTimeField()
    new_email = TextField()
    new_email_key = TextField()
    last_login = DateTimeField()
    last_ip = TextField()
    modified = DateTimeField(default=datetime.now)
