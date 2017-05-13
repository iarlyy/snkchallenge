#!/usr/bin/env python
import os
import time
import json
import sqlite3
import cherrypy

db_path = '/opt/snkdb/snkchallenge.db'
class avgReturner():
	def index(self):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		if os.path.exists(db_path):
			dbconn = sqlite3.connect(db_path)
			current_time = int(time.time())
			fivesecs_ago = current_time - 5
			try:
				query = dbconn.execute('SELECT avg(msg) from mqmsgs WHERE sensor_time >= %d' %(fivesecs_ago))
				return json.dumps({'last_fivesecs_avg': int(query.fetchone()[0])}, sort_keys=True, indent=4, separators=(',',': '))
			except:
				json_response = json.dumps({'last_fivesecs_avg': '-1'}, sort_keys=True, indent=4, separators=(',',': '))
		else:
			json_response = json.dumps({'last_fivesecs_avg': '-1'}, sort_keys=True, indent=4, separators=(',',': '))
		return json_response
	index.exposed = True

cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.quickstart(avgReturner(), '/')
