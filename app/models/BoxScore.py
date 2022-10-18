from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.PyObjectId import PyObjectId

class BoxScoreCFB(BaseModel):
	id: Optional[PyObjectId] = Field(None, alias='_id')
	date: str
	week: int
	away_team: str
	home_team: str
	away_team_points_scored: List[int]
	home_team_points_scored: List[int]
	away_team_statistics: dict
	home_team_statistics: dict

	def get_json(self):
		return jsonable_encoder(self, by_alias=False, exclude_none=True)

	def get_bson(self):
		data = self.dict(by_alias=True, exclude_none=True)
		if data.get('_id') is None:
			data.pop('_id', None)
		return data