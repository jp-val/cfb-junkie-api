from bson.objectid import ObjectId
from pydantic.json import ENCODERS_BY_TYPE

# ObjectId field compatible with Pydantic
class PyObjectId(ObjectId):
	@classmethod
	def __get_validators__(cls):
		yield cls.validate

	@classmethod
	def validate(cls, v):
		if not PyObjectId.is_valid(v):
			raise TypeError('Invalid ObjectId')
		return PyObjectId(v)

	@classmethod
	def __modify_schema__(cls, field_schema):
		field_schema.update(type='string')

ENCODERS_BY_TYPE[PyObjectId] = str