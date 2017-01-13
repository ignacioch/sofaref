import mysql.connector
import logging
from datetime import datetime

#logging.basicConfig(filename='example.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(filename=datetime.now().strftime('add_to_table_%d_%m_%Y.log'),level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')


#Connect to the mysql db / These elements need to change to our AWS RDS db 
cnx = mysql.connector.connect(user='root', password='vaios',
	host='127.0.0.1',
	database='sofaref')
cursor=cnx.cursor()


def queries (args):
	#First we check if the input argument is one of {match, event, media}

	if args.subcommand=='match':
		match_id = args.match_id
		match_datetime = args.match_datetime
		team_a = args.team_a
		team_b = args.team_b
		competition = args.competition
		match_status = args.match_status
		none_element=False

		#Check for add or update operation. Used else and not elif action == update, because the input is allways bound betwen the two of them

		if args.action == 'add':

			#Because the arguments could be variable in either add or update
			#Or between the three basic arguments of match, event, media
			#We need to iterate over the available arguments each time, in order to generate dynamically the query
			#The same is true for all the next for loops in the if statements

			for arg in vars(args):
				if getattr(args,arg)==None:
					none_element = True
					logging.error('Forgot an attribute! -'+arg)
					raise ValueError('Please input all arguments for the selected action : '+arg)

			#Used the boolean varieble none_element to check if any of the elements are empty
			#because some of the arguments are not mandatory and can be NULL in our INSERT query

			if none_element==False:
				query = ("INSERT into matches (match_id,match_datetime,team_a,team_b,competition,match_status) values (%s, %s,%s, %s,%s, %s)") 	
				cursor.execute(query,(match_id,match_datetime, team_a,team_b,competition,match_status))
				cnx.commit()
				logging.info('Query completed '+ query %(match_id,match_datetime, team_a,team_b,competition,match_status))
		else:

			#This is doing multiple queries for each element to update. Should find something to do one query
			#Need to be careful for SQL injection

			for arg in vars(args):
				if arg!='subcommand' and arg!='action' and arg!='match_id' and getattr(args,arg)!=None:
					sql = 'UPDATE matches SET ' + arg + '=%s WHERE match_id = %s'
					#The next assignment could be used in a for loop to create all the SET attributes {arg=value , arg1 = value1 etc.}, but could be potentially open to SQL Injection
					#sql = ("Update matches SET "+arg + " = '"+str(getattr(args,arg))+"' WHERE match_id = "+str(match_id))	
					cursor.execute(sql, (getattr(args,arg),match_id))
					cnx.commit()
					logging.info('Query completed '+ sql %(getattr(args,arg),match_id))


		#The same comments and structure as above

	elif args.subcommand=='event':
		event_id = args.event_id
		match_id = args.match_id
		description = args.description
		question = args.question
		none_element=False
		#Check for add or update operation.
		if args.action == 'add':
			for arg in vars(args):
				if getattr(args,arg)==None:
					none_element = True
					logging.error('Forgot an attribute!')
					raise ValueError('Please input all arguments for the selected action : '+arg)
			if none_element==False:
				query = ("insert into events (event_id,match_id,description,question_text) values (%s, %s,%s, %s) ")
				cursor.execute(query, (event_id,match_id,description,question))
				cnx.commit()
				logging.info('Query completed '+ query %(event_id,match_id,description,question))
		else:
			for arg in vars(args):
				if arg!='subcommand' and arg!='action' and arg!='event_id' and getattr(args,arg)!=None:
					sql = 'UPDATE events SET ' + arg + '=%s WHERE event_id = %s'	
					cursor.execute(sql, (getattr(args,arg),event_id))
					cnx.commit()
					logging.info('Query completed '+ sql %(getattr(args,arg),match_id))


	elif args.subcommand=='media':
		media_id = args.media_id
		event_id = args.event_id
		media_type = args.media_type
		media_url = args.media_url
		none_element=False
		#Check for add or update operation.
		if args.action == 'add':
			for arg in vars(args):
				if getattr(args,arg)==None:
					none_element = True
					logging.error('Forgot an attribute!')
					raise ValueError('Please input all arguments for the selected action : '+arg)
			if none_element==False:
				query = ("insert into media(media_id,event_id,media_type,media_url) values (%s, %s,%s, %s)")
				cursor.execute(query, (media_id,event_id,media_type,media_url))
				cnx.commit()
				logging.info('Query completed '+ query %(media_id,event_id,media_type,media_url))
		else:
			for arg in vars(args):
				if arg!='subcommand' and arg!='action' and arg!='media_id' and getattr(args,arg)!=None:
					sql = 'UPDATE media SET ' + arg + '=%s WHERE media_id = %s'	
					cursor.execute(sql, (getattr(args,arg),media_id))
					cnx.commit()
					logging.info('Query completed '+ sql %(getattr(args,arg),match_id))
	else:
		print('Wrong argument type. Try again.')
		logging.warning('Did not input correct argument. Select from (match,event,media)')
