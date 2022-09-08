from flask import g, request, jsonify
from functools import wraps

from app.database import db
from app.models import User
from app.common import util

# 400 - Bad Request
# 401 - Unauthorized
# 403 - Forbidden (Cleint identity is known)
# 404 - Not Found
# 500 - Server Error

def middleware(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		
		api_key = request.headers.get('x-api-key', None)
		if api_key is None:
			return jsonify({ 'message': 'Missing x-api-key header.' }), 400
		
		result_doc = db.users.find_one({ 'api_key':  api_key })
		if result_doc is None:
			return jsonify({ 'message': 'Invalid API Key.' }), 401
		
		user = User(**result_doc)
		host = request.headers.get('host', None)
		if 'localhost' not in host and host != user.domain:
			return jsonify({ 'message': 'Invalid API Key and Domain combination.' }), 401

		if user.privilege != 'admin' and request.method != 'GET':
			return jsonify({ 'message': 'Forbidden request for non-admin users.' }), 403

		date = util.get_date()
		if len(user.usage) <= 0:
			user.usage.append({ 'date': date, 'num_api_calls': 1 })
		elif user.usage[0]['date'] == date:
			user.usage[0]['num_api_calls'] = user.usage[0]['num_api_calls'] + 1
		else:
			user.usage.insert(0, { 'date': date, 'num_api_calls': 1 })

		db.users.update_one({ '_id': user.id }, { '$set': { 'usage': user.usage[:90] }})

		g.user = user

		result = f(*args, **kwargs)

		return result
	return decorated