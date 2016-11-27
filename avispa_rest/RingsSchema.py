# AvispaUser.py
from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, BooleanField, DateTimeField, ListField, DictField, Mapping

class RingsSchema(Document):
    _id = TextField()
    added = DateTimeField(default=datetime.now)
    license = TextField()
    public = BooleanField(default=False)
    rings = ListField(DictField(Mapping.build(
        RingName = TextField(),
        RingLabel = TextField(),
        RingDescription = TextField(),
        RingVersion = TextField(),
        RingURI = TextField(),
        RingBuild = TextField(),
        RingParent = TextField()
        )))
    fields = ListField(DictField(Mapping.build(
        FieldId = TextField(),
        FieldName = TextField(),
        FieldLabel = TextField(),
        FieldSemantic = TextField(),
        FieldType = TextField(),
        FieldSource = TextField(),
        FieldWidget = TextField(),
        FieldOrder = IntegerField(),
        FieldCardinality = TextField(),
        FieldMultilingual = BooleanField(),
        FieldRequired = BooleanField(),
        FieldDefault = TextField(),
        FieldHint = TextField(),
        FieldLayer = IntegerField(),
        )))