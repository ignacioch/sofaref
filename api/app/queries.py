import logging
from datetime import datetime
import mysql.connector


logger1 = logging.basicConfig(filename=datetime.now().strftime('queries_%d_%m_%Y.log'),level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')


def add_match_fn(args,mysql):
	match_id = args.match_id.data
	match_datetime = args.match_datetime.data
	team_a = args.team_a.data
	team_b = args.team_b.data
	competition = args.competition.data
	match_status = args.match_status.data
	none_element=False
	cnx = mysql.connect()
	cursor = cnx.cursor()
	for fieldname, value in args.data.items():
		if value==None or value=="":
			none_element = True
			logger1.error('Forgot an attribute! -'+fieldname)
			raise ValueError('Please input all arguments for the selected action : '+fieldname)

	#Used the boolean varieble none_element to check if any of the elements are empty
	#because some of the arguments are not mandatory and can be NULL in our INSERT query

	if none_element==False:
		query = ("INSERT into matches (match_id,match_datetime,team_a,team_b,competition,match_status) values (%s, %s,%s, %s,%s, %s)") 	
		try:
			cursor.execute(query,(match_id,match_datetime, team_a,team_b,competition,match_status))
		except cnx.Error as err:
				logger1.error('Inside queries - add_match')
				logger1.error(format(err))
				return format(err)
		cnx.commit()
		cnx.close()
		logger1.info(cursor._last_executed)
		logger1.info('Query completed '+ query %(match_id,match_datetime, team_a,team_b,competition,match_status))
		return (cursor._last_executed)

def update_match_fn(args,mysql):
	#This is doing multiple queries for each element to update. Should find something to do one query
			#Need to be careful for SQL injection
	match_id = args.match_id.data
	match_datetime = args.match_datetime.data
	team_a = args.team_a.data
	team_b = args.team_b.data
	competition = args.competition.data
	match_status = args.match_status.data
	none_element=False
	result = ' '
	for fieldname, value in args.data.items():
		cnx = mysql.connect()
		cursor = cnx.cursor()
		if fieldname!='Type' and fieldname!='Action' and fieldname!='match_id' and fieldname!='submit' and fieldname!='csrf_token' and value!=None and value!="":
			
			sql = 'UPDATE matches SET ' + fieldname + '=%s WHERE match_id = %s'
			#The next assignment could be used in a for loop to create all the SET attributes {arg=value , arg1 = value1 etc.}, but could be potentially open to SQL Injection
			#sql = ("Update matches SET "+arg + " = '"+str(getattr(args,arg))+"' WHERE match_id = "+str(match_id))	
			try:
				cursor.execute(sql, (value,match_id))
			except cnx.Error as err:
				logger1.error('Inside queries - update_match')
				logger1.error(format(err))
				#return format(err)
			cnx.commit()
			cursor.close()
			cnx.close()
			logger1.info(cursor._last_executed)
			result+=cursor._last_executed + ' '
			logger1.info('Query completed '+ sql %(value,match_id))
	
	return (result)
	#return (cursor._last_executed)

def add_event_fn(args,mysql):
	event_id = args.event_id.data
	match_id = args.match_id.data
	description = args.description.data
	question = args.question.data
	none_element=False
	cnx = mysql.connect()
	cursor = cnx.cursor()
	for fieldname, value in args.data.items():
		if value==None or value=="":
			none_element = True
			logger1.error('Forgot an attribute!- '+fieldname)
			raise ValueError('Please input all arguments for the selected action : '+fieldname)
	if none_element==False:
		query = ("INSERT into events (event_id,match_id,description,question_text) values (%s, %s,%s, %s) ")
		try:
			cursor.execute(query, (event_id,match_id,description,question))
		except cnx.Error as err:
				logger1.error('Inside queries - add_event')
				logger1.error(format(err))
				return format(err)
		cnx.commit()
		cnx.close()
		logger1.info(cursor._last_executed)
		return (cursor._last_executed)

def update_event_fn(args,mysql):
	event_id = args.event_id.data
	match_id = args.match_id.data
	description = args.description.data
	question = args.question.data
	none_element=False
	result = ' '
	for fieldname, value in args.data.items():
		cnx = mysql.connect()
		cursor = cnx.cursor()	
		if fieldname!='Type' and fieldname!='Action' and fieldname!='event_id' and fieldname!='submit' and fieldname!='csrf_token' and value!=None and value!="":
			sql = 'UPDATE events SET ' + fieldname + '=%s WHERE event_id = %s'	
			try:
				cursor.execute(sql, (value,event_id))
			except cnx.Error as err:
				logger1.error('Inside queries - update_event')
				logger1.error(format(err))
				return format(err)
			cnx.commit()
			cursor.close()
			cnx.close()
			logger1.info(cursor._last_executed)
			result+=cursor._last_executed + ' '
	return (result)		

def add_media_fn(args,mysql):
	media_id = args.media_id.data
	event_id = args.event_id.data
	media_type = args.media_type.data
	media_url = args.media_url.data
	none_element=False
	cnx = mysql.connect()
	cursor = cnx.cursor()
	for fieldname, value in args.data.items():
		if value==None or value=="":
			none_element = True
			logger1.error('Forgot an attribute!- '+fieldname)
			raise ValueError('Please input all arguments for the selected action : '+fieldname)
	if none_element==False:
		query = ("insert into media(media_id,event_id,media_type,media_url) values (%s, %s,%s, %s)")
		try:
			cursor.execute(query, (media_id,event_id,media_type,media_url))
		except cnx.Error as err:
			logger1.error('Inside queries - add_media')
			logger1.error(format(err))
			return format(err)
		cnx.commit()
		cnx.close()
		logger1.info(cursor._last_executed)
		return (cursor._last_executed)	

def update_media_fn(args,mysql):
	media_id = args.media_id.data
	event_id = args.event_id.data
	media_type = args.media_type.data
	media_url = args.media_url.data
	none_element=False
	result = ' '

	for fieldname, value in args.data.items():
		cnx = mysql.connect()
		cursor = cnx.cursor()
		if fieldname!='Type' and fieldname!='Action' and fieldname!='media_id' and fieldname!='submit' and fieldname!='csrf_token' and value!=None and value!="":
			sql = 'UPDATE media SET ' + fieldname + '=%s WHERE media_id = %s'
			try:
				cursor.execute(sql, (value,media_id))
			except cnx.Error as err:
				logger1.error('Inside queries - update_media')
				logger1.error(format(err))
				return format(err)
			cnx.commit()
			cursor.close()
			cnx.close()
			logger1.info(cursor._last_executed)
			result+=cursor._last_executed + ' '
	return (result)


