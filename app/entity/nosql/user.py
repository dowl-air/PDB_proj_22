
import mongoengine as me

class User(me.Document):
	id = me.IntField(primary_key=True, null=False)
	first_name = me.StringField()
	last_name = me.StringField()
	role = me.StringField()
	email = me.StringField()
