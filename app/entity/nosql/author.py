
import mongoengine as me

from .embedded import EmbeddedBook

class Author(me.Document):
	id = me.IntField(primary_key=True, null=False)
	first_name = me.StringField()
	last_name = me.StringField()
	description = me.StringField()
	books = me.EmbeddedDocumentListField(EmbeddedBook)
