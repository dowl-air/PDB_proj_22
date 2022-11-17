
import mongoengine as me

class Location(me.Document):
	id = me.IntField(primary_key=True, null=False)
	name = me.StringField()
	address = me.StringField()
