import sys
import argparse
from db_handler import queries
import logging
import traceback
from datetime import datetime

logging.basicConfig(filename=datetime.now().strftime('add_to_table_%d_%m_%Y.log'),level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')

def main():
	#Create the top level parser
	parser = argparse.ArgumentParser(description='Add/Update the DB tables.')
	subparsers = parser.add_subparsers(help='Required sub-commands',dest='subcommand')


	#Create subparsers for match
	match_parser = subparsers.add_parser('match' , help='Add to match table')
	match_parser.add_argument('action', type=str,choices=['add', 'update'] ,help='Select either add or update')
	match_parser.add_argument('match_id',type=int , help='The id of the match')
	match_parser.add_argument('-match_datetime', type=str, help='Date and time of the match')
	match_parser.add_argument('-team_a', type=str, help='Home team')
	match_parser.add_argument('-team_b', type=str, help='Away team')
	match_parser.add_argument('-competition', type=str, help='String literal for the competition')
	match_parser.add_argument('-match_status', type=int,choices=[0, 1, 2], help='0 : not started, 1 live , 2 completed')


	#Create subparsers for event
	event_parser = subparsers.add_parser('event' , help='Add to event table')
	event_parser.add_argument('action', type=str,choices=['add', 'update'] , help='Select either add or update')
	event_parser.add_argument('event_id', type=int, help='The id of the event')
	event_parser.add_argument('-match_id', type=int, help='The id of the match')
	event_parser.add_argument('-description', type=str, help='Description of the event')
	event_parser.add_argument('-question', type=str, help='Final question text')


	#Create subparsers for media
	media_parser = subparsers.add_parser('media' , help='Add to media table')
	media_parser.add_argument('action', type=str,choices=['add', 'update'] , help='Select either add or update')
	media_parser.add_argument('media_id', type=int , help='The id of the media')
	media_parser.add_argument('-event_id', type=int , help='The id of the event')
	media_parser.add_argument('-media_type', type=int ,choices=[0, 1, 2], help=' 0 : no media , 1 : image , 2 : video url')
	media_parser.add_argument('-media_url', type=str , help='The url')

	#Parse the arguments
	args = parser.parse_args()
	#Call the db_handler
	queries(args)


try:
	main()
except:
	logging.error(traceback.format_exc())
	print(traceback.format_exc())













