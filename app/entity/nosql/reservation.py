
import mongoengine as me

from .embedded import EmbeddedBookCopy, EmbeddedUser

class Reservation(me.Document):
	id = me.IntField(primary_key=True, null=False)
	start_date = me.DateField()
	end_date = me.DateField()
	state = me.IntField()
	book_copy = me.EmbeddedDocumentField(EmbeddedBookCopy)
	customer = me.EmbeddedDocumentField(EmbeddedUser)
