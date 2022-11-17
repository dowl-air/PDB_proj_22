
import mongoengine as me

class Category(me.Document):
	id = me.IntField(primary_key=True, null=False)
	name = me.StringField()
	description = me.StringField()
