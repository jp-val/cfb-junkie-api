from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

CORS(app)

api = Api(app)

from app.resources.home import Home
from app.resources.rankings import ( RankingById, RankingsQuery, RankingsLatest,
	RankingsSeason, RankingUpload, RankingUpdate, RankingDelete )

from app.resources.scrape import ScrapeRankings

api.add_resource(Home, '/')

api.add_resource(RankingById, '/ranking/<string:ranking_id>')
api.add_resource(RankingsQuery, '/rankings')
api.add_resource(RankingsLatest, '/latest-rankings')
api.add_resource(RankingsSeason, '/season-rankings')
api.add_resource(RankingUpload, '/upload-ranking')
api.add_resource(RankingUpdate, '/update-ranking')
api.add_resource(RankingDelete, '/delete-ranking/<string:ranking_id>')

api.add_resource(ScrapeRankings, '/scrape-ranking/<string:ranking_name>')