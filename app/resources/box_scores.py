from flask import g, request
from flask_restful import reqparse, Resource
from functools import cmp_to_key

from app.middleware import middleware
from app.database import db
from app.models import BoxScore, TeamStanding
from app.common import util

class BoxScoresQuery(Resource):
	@middleware
	def get(self):
		query = {}

		for field in ['team']:
			if field in request.args:
				query[field] = request.args[field]

		for field in ['season', 'week']:
			if field in request.args:
				query[field] = int(request.args[field])

		# isAdmin = g.user.privilege == 'admin'
		# raw_read = db.rankings.find(query, None if isAdmin else { '_id': 0 })

		# rankings = [Ranking(**r).get_json() for r in raw_read]
		# rankings.sort(key=lambda item: str(item.get('year'))+str(item.get('week'))+item.get('name'))

		return {}

class BoxScoreUpload(Resource):
	@middleware
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('date', type=str, required=True)
		parser.add_argument('week', type=int, required=True)
		parser.add_argument('away_team', type=str, required=True)
		parser.add_argument('home_team', type=str, required=True)
		parser.add_argument('away_team_statistics', type=dict, required=True)
		parser.add_argument('home_team_statistics', type=dict, required=True)
		parser.add_argument('away_team_points_scored', type=int, action='append', required=True)
		parser.add_argument('home_team_points_scored', type=int, action='append', required=True)
		
		args = parser.parse_args()
		
		box_score = BoxScore(**args)
		box_score_id = db['box-scores'].insert_one(box_score.get_bson()).inserted_id
		
		raw_read = db['box-scores'].find_one({ '_id': box_score_id })
		return { 'box_score': BoxScore(**raw_read).get_json() }

class ConferenceStanding(Resource):
	@middleware
	def get(self, season, conference_name):
		
		teams = db.team_standings.find({ 'season': season, 'conference': conference_name })
		teams = [TeamStanding(**t) for t in teams]
		
		def compare(x, y):
			sigma = 0.0000001

			x_conf_win_p = x.conference_wins / (x.conference_wins + x.conference_loses)
			y_conf_win_p = y.conference_wins / (y.conference_wins + y.conference_loses)

			x_win_p = x.overall_wins / x.games
			y_win_p = y.overall_wins / y.games
			
			if abs(x_conf_win_p - y_conf_win_p) < sigma: # if equal
				if y.team in x.conference_wins_against:
					  return -1
				elif x.team in y.conference_wins_against:
					return 1
				elif x.conference_wins > y.conference_wins:
					return -1
				elif x.conference_wins < y.conference_wins:
					return 1
				elif abs(x_win_p - y_win_p) < sigma:
					if x.team < y.team:
						return -1
					elif x.team > y.team:
						return 1
					else:
						return 0
				elif x_win_p > y_win_p:
					return -1
				else:
					return 1
			elif x_conf_win_p > y_conf_win_p: # if x has better conference win percentage
				return -1
			else: # if y has better conference win percentage
				return 1

		sorted_standing = sorted(teams, key=cmp_to_key(compare))
		sorted_standing = [t.get_json() for t in sorted_standing]

		return { 'standing': sorted_standing }