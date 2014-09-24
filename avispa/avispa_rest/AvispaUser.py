# AvispaUser.py
from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

class AvispaUser(Document):
    username = TextField()
    guid = TextField()
    added = DateTimeField(default=datetime.now)