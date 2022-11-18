
import mongoengine as me

class AuthorName(me.EmbeddedDocument):
	id = me.IntField(null=False)
	first_name = me.StringField()
	last_name = me.StringField()

class EmbeddedLocation(me.EmbeddedDocument):
	id = me.IntField(null=False)
	name = me.StringField()
	address = me.StringField()

class EmbeddedCategory(me.EmbeddedDocument):
	id = me.IntField(null=False)
	name = me.StringField()
	description = me.StringField()

class EmbeddedBookCopy(me.EmbeddedDocument):
	id = me.IntField(null=False)
	book_id = me.IntField()
	print_date = me.DateField()
	note = me.StringField()
	state = me.IntField()
	location_id = me.IntField()

class EmbeddedUser(me.EmbeddedDocument):
	id = me.IntField(null=False)
	first_name = me.StringField()
	last_name = me.StringField()
	role = me.StringField()
	email = me.StringField()

class EmbeddedBook(me.EmbeddedDocument):
	id = me.IntField(null=False)
	name = me.StringField()
	ISBN = me.StringField()
	release_date = me.DateField()
	description = me.StringField()
