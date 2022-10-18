from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.PyObjectId import PyObjectId
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

# class TeamStatistics(BaseModel):
# 	id: Optional[PyObjectId] = Field(None, alias='_id')
# 	first_downs: int
# 	first_down_rushing_attempts: int
# 	first_down_passing_attempts: int
# 	first_down_penalties: int
# 	third_down_conversion_rate: float
# 	fourth_down_conversion_rate: float
# 	total_net_yards: int
# 	total_plays: int
# 	average_yards_per_play: float
# 	net_yards_rushing: int
# 	rushing_attempts: int
# 	average_rushing_yards_per_rushing_attempt: float
# 	total_yards_passing: int
# 	yards_per_pass: float
# 	touchdowns: int
# 	rushing_touchdowns: int
# 	passing_touchdowns: int
# 	other_touchdowns: int
# 	turnovers: int
# 	interceptions_thrown: int
# 	total_return_yards: int
# 	safeties: int
# 	pass_completions: int
# 	pass_attempts: int
# 	penalties: int
# 	penalty_yards: int
# 	fumbles: int
# 	fumbles_lost: int
# 	punts: int
# 	average_punt_yards: float
# 	punts_returns: int
# 	punt_return_yards: int
# 	kickoffs_returns: int
# 	kickoff_return_yards: int
# 	interceptions_returns: int
# 	interception_return_yards: int

# 	def get_json(self):
# 		return jsonable_encoder(self, by_alias=False, exclude_none=True)

# 	def get_bson(self):
# 		data = self.dict(by_alias=True, exclude_none=True)
# 		if data.get('_id') is None:
# 			data.pop('_id', None)
# 		return data