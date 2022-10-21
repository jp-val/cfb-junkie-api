from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from .PyObjectId import PyObjectId
from app.common.util import get_season

class TeamStanding(BaseModel):
	id: Optional[PyObjectId] = Field(None, alias='_id')
	team: str
	conference: str
	season: int = Field(default_factory=get_season)
	week: int = 0
	games: int = 0
	home_wins: int = 0
	home_loses: int = 0
	away_wins: int = 0
	away_loses: int = 0
	neutral_site_wins: int = 0
	neutral_site_loses: int = 0
	overall_wins: int = 0
	overall_loses: int = 0
	conference_wins: int = 0
	conference_loses: int = 0
	opponents: List[str] = []
	conference_wins_against: List[str] = []

	def get_json(self):
		return jsonable_encoder(self, by_alias=False, exclude_none=True)

	def get_bson(self):
		data = self.dict(by_alias=True, exclude_none=True)
		if data.get('_id') is None:
			data.pop('_id', None)
		return data