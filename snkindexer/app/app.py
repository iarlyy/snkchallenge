#!/usr/bin/env python
import os
import sys
import time
import paho.mqtt.client as mqc
import sqlite3

db_path = '/opt/snkdb/snkchallenge.db'

class snkindexer:

	# setup a sqlite database if it doesn't exists
	def db_setup(self):
		if not os.path.exists(db_path):
			dbconn = sqlite3.connect(db_path)
			dbconn.execute('CREATE TABLE mqmsgs (idx_time, sensor_time, sensor_id, msg)')
			dbconn.commit()
			print('New DB created:', db_path)
		else:
			print('Using existing db:', db_path)

	# when a connection acknowledgement is received
	def mq_gotmsg(self, mqcli, userdata, msg):

		idx_time = int(time.time())
		sensor_time = int(msg.payload.split('-')[0])
		sensor_id = msg.topic.split('/')[1]
		mqmsg = msg.payload.split('-')[1]
		dbconn.execute('INSERT INTO mqmsgs VALUES ("%d", "%d", "%s", "%s")' % (idx_time, sensor_time, sensor_id, mqmsg))
		dbconn.commit()
		return True

	def mq_gotconn(self, mqcli, userdata, res):
		return 'a notification should be fired'

	def mq_gotdisconn(self, mqcli, userdata, res):
		return 'a notification should be fired'

if __name__ == "__main__":
	app = snkindexer()
	app.db_setup()
	dbconn = sqlite3.connect(db_path)
	try:
		if os.environ.get('MQHOST') != None:
			MQ_HOST = os.environ.get('MQHOST')
		else:
			MQ_HOST = 'localhost'
	except: 
		MQ_HOST = 'localhost'

	mqcli = mqc.Client()
	mqcli.on_message = app.mq_gotmsg

	# if connection die, hook it up again
	while True:
		try:
			mqcli.connect(MQ_HOST)
			mqcli.subscribe("snksensor/#") # subscribe to all snk* messages
			mqcli.loop_forever()
		except KeyboardInterrupt:
			print('CTRL+C fired, exiting...')
			sys.exit(1)
		except:
			print('Something went wrong, reconnecting in 5s', sys.exc_info())
			mqcli.disconnect()
			time.sleep(5)
