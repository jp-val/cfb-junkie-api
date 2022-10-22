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

from app.resources.box_scores import BoxScoresQuery, BoxScoreUpload, ConferenceStanding

from app.resources.scrape import ScrapeRankings, ScrapeAndUploadBoxScores, TeamStandingUpdate

api.add_resource(Home, '/')

api.add_resource(RankingById, '/ranking/<string:ranking_id>')
api.add_resource(RankingsQuery, '/rankings')
api.add_resource(RankingsLatest, '/latest-rankings')
api.add_resource(RankingsSeason, '/season-rankings')
api.add_resource(RankingUpload, '/upload-ranking')
api.add_resource(RankingUpdate, '/update-ranking')
api.add_resource(RankingDelete, '/delete-ranking/<string:ranking_id>')

api.add_resource(BoxScoresQuery, '/box-scores/')
api.add_resource(BoxScoreUpload, '/upload-box-score')
api.add_resource(ConferenceStanding, '/get-conference-standing/<int:season>/<string:conference_name>')

api.add_resource(ScrapeRankings, '/scrape-ranking/<string:ranking_name>')
api.add_resource(ScrapeAndUploadBoxScores, '/scrape-and-upload-box-scores/<int:season>/<int:week>')
api.add_resource(TeamStandingUpdate, '/update-standings/<int:season>/<int:week>')