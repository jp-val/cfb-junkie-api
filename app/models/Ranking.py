from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.PyObjectId import PyObjectId

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