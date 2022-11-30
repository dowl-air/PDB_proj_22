
import mongoengine as me

from .embedded import EmbeddedBookCopy, EmbeddedUser


class Borrowal(me.Document):
    id = me.IntField(primary_key=True, null=False)
    start_date = me.DateField()
    end_date = me.DateField()
    returned_date = me.DateField(null=True)
    state = me.IntField()
    book_copy = me.EmbeddedDocumentField(EmbeddedBookCopy)
    customer = me.EmbeddedDocumentField(EmbeddedUser)
    employee = me.EmbeddedDocumentField(EmbeddedUser)
