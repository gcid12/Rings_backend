# AvispaUser.py
from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, Mapping

class MyRingBlueprint(Document):
    _id = TextField()
    added = DateTimeField(default=datetime.now)
    rings = ListField(DictField(Mapping.build(
        RingName = TextField(),
        RingDescription = TextField(),
        RingVersion = TextField(),
        RingURI = TextField(),
        RingBuild = TextField()
        )))
    fields = ListField(DictField(Mapping.build(
        FieldName = TextField(),
        FieldLabel = TextField(),
        FieldSemantic = TextField(),
        FieldType = TextField(),
        FieldSource = TextField(),
        FieldWidget = TextField(),
        FieldOrder = TextField(),
        FieldCardinality = TextField(),
        FieldMultilingual = TextField(),
        FieldRequired = TextField(),
        FieldDefault = TextField(),
        FieldHint = TextField(),
        FieldLayer = TextField(),
        )))