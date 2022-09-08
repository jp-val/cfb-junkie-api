from bson.objectid import ObjectId
from pydantic.json import ENCODERS_BY_TYPE

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.common.util import generate_api_key

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

class User(BaseModel):
	id: Optional[PyObjectId] = Field(None, alias='_id')
	name: str
	alias: str
	email: str
	domain: str
	api_key: str = Field(default_factory=generate_api_key)
	usage: List[dict] = Field([])
	privilege: str = Field('user')
	date_added: datetime = Field(default_factory=datetime.utcnow)

	def get_json(self):
		return jsonable_encoder(self, by_alias=False, exclude_none=True)

	def get_bson(self):
		data = self.dict(by_alias=True, exclude_none=True)
		if data.get('_id') is None:
			data.pop('_id', None)
		return data

class Ranking(BaseModel):
	id: Optional[PyObjectId] = Field(None, alias='_id')
	name: str
	season: int
	week: int
	ranking: List[str]
	date_added: datetime = Field(default_factory=datetime.utcnow)
	date_updated: datetime = Field(default_factory=datetime.utcnow)

	def get_json(self):
		return jsonable_encoder(self, by_alias=False, exclude_none=True)

	def get_bson(self):
		data = self.dict(by_alias=True, exclude_none=True)
		if data.get('_id') is None:
			data.pop('_id', None)
		return data