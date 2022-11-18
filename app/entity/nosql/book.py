
import mongoengine as me

from .embedded import AuthorName, EmbeddedBookCopy, EmbeddedCategory

class Book(me.Document):
	id = me.IntField(primary_key=True, null=False)
	authors = me.EmbeddedDocumentListField(AuthorName)
	name = me.StringField()
	ISBN = me.StringField()
	release_date = me.DateField()
	description = me.StringField()
	book_copies = me.EmbeddedDocumentListField(EmbeddedBookCopy)
	categories = me.EmbeddedDocumentListField(EmbeddedCategory)
