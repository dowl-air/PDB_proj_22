

import mongoengine as me

from .embedded import EmbeddedLocation

class BookCopy(me.Document):
	id = me.IntField(primary_key=True, null=False)
	book_id = me.IntField()
	print_date = me.DateField()
	note = me.StringField()
	state = me.IntField()
	location = me.EmbeddedDocumentField(EmbeddedLocation)
