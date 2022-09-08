from flask import g, request, jsonify
from flask_restful import Resource

from app.database import db
from app.middleware import middleware

class Home(Resource):
	def get(self):
		response = jsonify({ 'about': 'CFB-Junkie API' })
		# response.headers.add('Content-Type', 'application/json')
		return response