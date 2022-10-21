from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from .PyObjectId import PyObjectId
from app.common.util import generate_api_key

class User(BaseModel):
	id: Optional[PyObjectId] = Field(None, alias='_id')
	name: str
	alias: str
	email: str
	domain: str
	api_key: str = Field(default_factory=generate_api_key)
	usage: List[dict] = []
	privilege: str = 'user'
	date_added: datetime = Field(default_factory=datetime.utcnow)

	def get_json(self):
		return jsonable_encoder(self, by_alias=False, exclude_none=True)

	def get_bson(self):
		data = self.dict(by_alias=True, exclude_none=True)
		if data.get('_id') is None:
			data.pop('_id', None)
		return data