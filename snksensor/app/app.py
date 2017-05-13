#!/usr/bin/env python
import os
import sys
import random
import time
import paho.mqtt.publish as mqc

class snksensor:
	# the most simple integer random generator ever
	def genint(self):
		return random.randint(1,10000)

app = snksensor()

if __name__ == "__main__":
	try:
		if os.environ.get('MQHOST') != None:
			MQ_HOST = os.environ.get('MQHOST')
		else:
			MQ_HOST = 'localhost'

		if os.environ.get('SENSOR_ID') != None:
			SID = os.environ.get('SENSOR_ID')
		else:
			SID = 'default'
	except: 
		MQ_HOST = 'localhost'

	while True:
		try:
			curtime = str(int(time.time()))
			rint = str(app.genint())
			mqmsg = curtime+'-'+rint
			mqc.single('snksensor/'+SID+'/randint', mqmsg, hostname=MQ_HOST)
		except:
			print('Something went wrong, trying again in 1s', sys.exc_info())
			
			# TODO - to implement local caching of messages if broker went down (file, sqlite, external call)

		time.sleep(1)
