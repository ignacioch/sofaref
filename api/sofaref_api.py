from flask import Flask
from flask import jsonify
from flask import request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
#General config


app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = '***'
app.config['MYSQL_DATABASE_PASSWORD'] = '***'
app.config['MYSQL_DATABASE_DB'] = '***'
app.config['MYSQL_DATABASE_HOST'] = '***'
mysql.init_app(app)



@app.route('/')
def hello_world():
	return 'Select from : getActiveMatches, getEventsForMatchId, vote, getVotesForEventId'


@app.route('/getActiveMatches')
def get_active_matches():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute('''SELECT match_id,match_datetime,team_a,team_b,competition,match_status FROM matches WHERE match_status=1''')
	rv = cursor.fetchall()
	conn.close()
	return jsonify(rv)


@app.route('/getEventsForMatchId/<match_id>')
def get_events_for_match(match_id):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute('''SELECT matches.match_id, matches.match_datetime, matches.team_a, matches.team_b, matches.competition, matches.match_status, events.event_id,events.description, events.question_text
		FROM matches
		INNER JOIN events
		ON matches.match_id=events.match_id 
		WHERE matches.match_id = %s''', match_id)
	rv = cursor.fetchall()
	conn.close()
	return jsonify(rv)

#To see in practice how it reacts. The output is the default http 200 for success or any other for error
@app.route('/vote',methods=['POST'])
def vote():
	conn = mysql.connect()
	cursor = conn.cursor()
	if request.method == 'POST':
		try:
			cursor.execute('''INSERT into votes (vote_id, user_id,vote,event_id) values (%s,%s,%s,%s)''',(request.form['vote_id'],request.form['user_id'],request.form['vote'],request.form['event_id']))
			conn.commit()
			conn.close()
			return 'Registered'
		except conn.Error as e:
			conn.close()
			return str(e)
		
		

@app.route('/getVotesForEventId/<event_id>')
def get_votes_for_event(event_id):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute('''SELECT vote_id,user_id,vote,event_id from votes where event_id=%s''', event_id)
	rv = cursor.fetchall()
	conn.close()
	return jsonify(rv)
