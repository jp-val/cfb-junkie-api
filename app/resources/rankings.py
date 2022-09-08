from flask import g, request
from flask_restful import reqparse, Resource

from app.middleware import middleware
from app.database import db
from app.models import Ranking
from app.common import util

from bson.objectid import ObjectId
from datetime import datetime

class RankingById(Resource):
	@middleware
	def get(self, ranking_id):
		if not ObjectId.is_valid(ranking_id):
			return { 'message': 'Invalid Object ID.' }, 400
		else:
			ranking_id = ObjectId(ranking_id)
		
		raw_read = db.rankings.find_one({ '_id': ranking_id })
		return { 'ranking': Ranking(**raw_read).get_json() }

class RankingsQuery(Resource):
	@middleware
	def get(self):
		query = {}

		for field in ['name']:
			if field in request.args:
				query[field] = request.args[field]

		for field in ['season', 'week']:
			if field in request.args:
				query[field] = int(request.args[field])

		isAdmin = g.user.privilege == 'admin'
		raw_read = db.rankings.find(query, None if isAdmin else { '_id': 0 })

		return { 'rankings': [Ranking(**r).get_json() for r in raw_read] }

class RankingsLatest(Resource):
	@middleware
	def get(self):
		season = util.get_season()
		week = util.get_week()

		query = { 'season': season, 'week': week }
		isAdmin = g.user.privilege == 'admin'
		raw_read = db.rankings.find(query, None if isAdmin else { '_id': 0 })

		return { 'rankings': [Ranking(**r).get_json() for r in raw_read] }

class RankingsSeason(Resource):
	@middleware
	def get(self):
		season = util.get_season()
		query = { 'season': season }
		isAdmin = g.user.privilege == 'admin'
		raw_read = db.rankings.find(query, None if isAdmin else { '_id': 0 })
		return { 'rankings': [Ranking(**r).get_json() for r in raw_read] }

ranking_upload_parser = reqparse.RequestParser()
ranking_upload_parser.add_argument('name', type=str, required=True)
ranking_upload_parser.add_argument('season', type=int, required=True)
ranking_upload_parser.add_argument('week', type=int, required=True)
ranking_upload_parser.add_argument('ranking', type=str, action='append', required=True)

class RankingUpload(Resource):
	def post(self):
		args = ranking_upload_parser.parse_args()
		
		ranking = Ranking(**args)
		ranking_id = db.rankings.insert_one(ranking.get_bson()).inserted_id
		
		raw_read = db.rankings.find_one({ '_id': ranking_id })
		return { 'ranking': Ranking(**raw_read).get_json() }

ranking_update_parser = reqparse.RequestParser()
ranking_update_parser.add_argument('id', type=str, required=True)
ranking_update_parser.add_argument('name', type=str)
ranking_update_parser.add_argument('season', type=int)
ranking_update_parser.add_argument('week', type=int)
ranking_update_parser.add_argument('ranking', type=str, action='append')

class RankingUpdate(Resource):
	@middleware
	def put(self):
		args = ranking_update_parser.parse_args()

		if not ObjectId.is_valid(args.id):
			return { 'message': 'Invalid Object ID.' }, 400
		else:
			args.id = ObjectId(args.id)

		raw_ranking = { 'date_updated': datetime.utcnow() }
		for key in ['name', 'season', 'week', 'ranking']:
			if args[key] != None:
				raw_ranking[key] = args[key]

		db.rankings.update_one({ '_id': args.id }, { '$set': raw_ranking })
		raw_read = db.rankings.find_one({ '_id': args.id })

		return { 'ranking': Ranking(**raw_read).get_json() }

class RankingDelete(Resource):
	@middleware
	def delete(self, ranking_id):
		if not ObjectId.is_valid(ranking_id):
			return { 'message': 'Invalid Object ID.' }, 400
		else:
			ranking_id = ObjectId(ranking_id)

		db.rankings.delete_one({ '_id': ranking_id })
		return { 'id': str(ranking_id) }