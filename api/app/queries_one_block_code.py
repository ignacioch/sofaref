import logging
from datetime import datetime
import mysql.connector


logging.basicConfig(filename=datetime.now().strftime('queries_%d_%m_%Y.log'),level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')



def queries (args,mysql):
	#First we check if the input argument is one of {match, event, media}
	#print(args.Type.data)
	print(args.Match_datetime)
	if args.Type.data=='match':
		print('entered')
		match_id = args.Id.data
		match_datetime = args.Match_datetime.data
		team_a = args.Team_A.data
		team_b = args.Team_B.data
		competition = args.Competition.data
		match_status = args.Match_status.data
		none_element=False
		cnx = mysql.connect()
		cursor = cnx.cursor()
		#Check for add or update operation. Used else and not elif action == update, because the input is allways bound betwen the two of them

		if args.Action.data == 'add':

			#Because the arguments could be variable in either add or update
			#Or between the three basic arguments of match, event, media
			#We need to iterate over the available arguments each time, in order to generate dynamically the query
			#The same is true for all the next for loops in the if statements
			print('entered1')
			for fieldname, value in args.data.items():
				if value==None or value=="":
					none_element = True
					print('entered2')
					logging.error('Forgot an attribute! -'+fieldname)
					raise ValueError('Please input all arguments for the selected action : '+fieldname)

			#Used the boolean varieble none_element to check if any of the elements are empty
			#because some of the arguments are not mandatory and can be NULL in our INSERT query

			if none_element==False:
				print('entered3')
				query = ("INSERT into matches (match_id,match_datetime,team_a,team_b,competition,match_status) values (%s, %s,%s, %s,%s, %s)") 	
				try:
					cursor.execute(query,(match_id,match_datetime, team_a,team_b,competition,match_status))
				except cnx.Error as err:
  					print("Something went wrong111: {}".format(err))
  					print(cursor._last_executed)
  					return format(err)
				print(cursor.statement)
				cnx.commit()
				logging.info(cursor._last_executed)
				logging.info('Query completed '+ query %(match_id,match_datetime, team_a,team_b,competition,match_status))
		else:

			#This is doing multiple queries for each element to update. Should find something to do one query
			#Need to be careful for SQL injection

			for fieldname, value in args.data.items():
				if fieldname!='Type' and fieldname!='Action' and fieldname!='Id' and fieldname!='submit' and fieldname!='csrf_token' and value!=None and value!="":
					print (fieldname, value)
					sql = 'UPDATE matches SET ' + fieldname + '=%s WHERE match_id = %s'
					#The next assignment could be used in a for loop to create all the SET attributes {arg=value , arg1 = value1 etc.}, but could be potentially open to SQL Injection
					#sql = ("Update matches SET "+arg + " = '"+str(getattr(args,arg))+"' WHERE match_id = "+str(match_id))	
					cursor.execute(sql, (value,match_id))
					cnx.commit()
					logging.info('Query completed '+ sql %(value,match_id))


		#The same comments and structure as above

	elif args.Type.data=='event':
		event_id = args.event_id
		match_id = args.match_id
		description = args.description
		question = args.question
		none_element=False
		#Check for add or update operation.
		if args.Action.data == 'add':
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


	elif args.Type.data=='media':
		media_id = args.media_id
		event_id = args.event_id
		media_type = args.media_type
		media_url = args.media_url
		none_element=False
		#Check for add or update operation.
		if args.Action.data == 'add':
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
