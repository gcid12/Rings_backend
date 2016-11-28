# AvispaUser.py
from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, BooleanField, Mapping

class MyRingUser(Document):
    _id = TextField()
    #firstname = TextField()  DEPRECATED! Use "name" for firstname if needed
    name = TextField()
    lastname = TextField()
    email = TextField()
    billingemail = TextField()
    is_org = BooleanField()
    location = TextField()
    url = TextField()
    profilepic = TextField()
    about = TextField()
    #people = DictField()
    onlogin = TextField()
    people = ListField(DictField(Mapping.build(
        handle = TextField(),
        addedby = TextField(),
        added = DateTimeField(default=datetime.now)
        )))
    teams = ListField(DictField(Mapping.build(
        teamname = TextField(),
        members = ListField(DictField(Mapping.build(
                handle = TextField(),
                addedby = TextField(),
                added = DateTimeField(default=datetime.now)
            ))),
        rings = ListField(DictField(Mapping.build(
            handle = TextField(),
            ringname = TextField(),
            addedby = TextField(),
            added = DateTimeField(default=datetime.now)
            ))),
        roles = ListField(DictField(Mapping.build(
            role = TextField(),
            addedby = TextField(),
            added = DateTimeField(default=datetime.now)
            ))),
        addedby = TextField(),
        added = DateTimeField(default=datetime.now)    
        )))
    salt = TextField()
    passhash = TextField()
    guid = TextField()
    added = DateTimeField(default=datetime.now)
    branchof = TextField()
    rings = ListField(DictField(Mapping.build(
        ringname = TextField(),
        version = TextField(),
        count = IntegerField(),
        added = DateTimeField(default=datetime.now),
        roles = ListField(DictField(Mapping.build(
            role = TextField(),
            users = ListField(Mapping.build())
            )))
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
            ))),
        roles = ListField(DictField(Mapping.build(
            role = TextField(),
            users = ListField(Mapping.build())
            )))
        )))
    badges = ListField(DictField(Mapping.build(
        badgename = TextField(),
        badgedescription = TextField(),
        added = DateTimeField(default=datetime.now)
        )))
    campaigns = ListField(DictField(Mapping.build(
        campaignname = TextField(),
        campaigndescription = TextField(),
        added = DateTimeField(default=datetime.now)
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
