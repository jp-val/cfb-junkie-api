from flask import request
from flask_restful import Resource

from app.middleware import middleware
from app.common import util, webscrapers as ws

class ScrapeRankings(Resource):
	@middleware
	def post(self, ranking_name):
		
		name = '<empty>'
		ranking = []

		if ranking_name == 'ap-poll':
			name = 'AP Poll'
			ranking = ws.scrape_ap_poll()
		
		elif ranking_name == 'sagarin-ratings':
			name = 'Sagarin Ratings'
			ranking = ws.scrape_sagarin_ratings()
		
		elif ranking_name == 'espn-fpi':
			name = 'ESPN FPI'
			ranking = ws.scrape_espn_fpi()
		
		elif ranking_name == 'massey-ratings':
			name = 'Massey Ratings'
			ranking = ws.scrape_massey_ratings()

		elif ranking_name == 'colley-matrix':
			name = 'Colley Matrix'
			ranking = ws.scrape_colley_matrix()

		else:
			return { 'message': 'You did something wrong.' }, 404

		season = util.get_season()
		week = util.get_week()
		
		rank = { 'name': name, 'season': season, 'week': week, 'ranking': ranking }
		return { 'ranking': rank }