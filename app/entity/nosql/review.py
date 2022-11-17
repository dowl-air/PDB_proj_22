
import mongoengine as me

from .embedded import EmbeddedUser

class Review(me.Document):
	id = me.IntField(primary_key=True, null=False)
	book_id = me.IntField()
	title = me.StringField()
	content = me.StringField()
	rating = me.IntField()
	customer = me.EmbeddedDocumentField(EmbeddedUser)
