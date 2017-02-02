from app import app
from flask import Flask, render_template, Response, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore,UserMixin, RoleMixin, login_required
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session ,scoped_session, sessionmaker, Query, relationship
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from flask_principal import Principal, Permission, RoleNeed
from flaskext.mysql import MySQL
from flask import jsonify
from .forms import pre_modify, first_selection, add_match, update_match, add_event, update_event, add_media,update_media,vote_form
from .queries import add_match_fn, update_match_fn, add_event_fn,update_event_fn, add_media_fn,update_media_fn
import logging
from datetime import datetime



logging.basicConfig(filename=datetime.now().strftime('views_%d_%m_%Y.log'),level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')


#General config
mysql = MySQL()

# MySQL configurations  
app.config.from_object('config.DevelopmentConfig')
mysql.init_app(app)
# Create database connection object
db = SQLAlchemy(app)


# automap base
Base = automap_base()

# reflect
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.prepare(engine, reflect=True)


# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.role_id')))

class Role(db.Model, RoleMixin):
    id = db.Column('role_id',db.Integer(), primary_key=True)
    name = db.Column('role_name',db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column('user_id',db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# load the extension
principals = Principal(app)

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))




# Views

@app.route('/')
def home():
    return render_template('home_page.html')

@app.route('/home')
def home_page():
	return render_template('home_page.html')

@app.route('/getActiveMatches')
def get_active_matches():
	logging.info('/getActiveMatches')
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute('''SELECT match_id,match_datetime,team_a,team_b,competition,match_status FROM matches WHERE match_status=1''')
		rv = cursor.fetchall()
		logging.info('THE QUERY WAS SUCCESFULL: '+cursor._last_executed)
		logging.info(rv)
		conn.close()
		return jsonify(rv)
	except mysql.connect().Error as err:
		logging.error(format(err))
		return format(err)


@app.route('/getEventsForMatchId/<match_id>')
def get_events_for_match(match_id):
	logging.info('/getEventsForMatchId')
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute('''SELECT matches.match_id, matches.match_datetime, matches.team_a, matches.team_b, matches.competition, matches.match_status, events.event_id,events.description, events.question_text
			FROM matches
			INNER JOIN events
			ON matches.match_id=events.match_id 
			WHERE matches.match_id = %s''', match_id)
		rv = cursor.fetchall()
		conn.close()
		logging.info('THE QUERY WAS SUCCESFULL: '+ cursor._last_executed)
		logging.info(rv)
		return jsonify(rv)
	except mysql.connect().Error as err:
			logging.error(format(err))
			return format(err)

@app.route('/getMediaForEventId/<event_id>')
def get_media_for_event(event_id):
	logging.info('/getMediaForEventId')
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute('''select media_id,event_id,media_type,media_url from media where event_id=%s''', event_id)
		rv = cursor.fetchall()
		conn.close()
		logging.info('THE QUERY WAS SUCCESFULL: '+ cursor._last_executed)
		logging.info(rv)
		return jsonify(rv)
	except mysql.connect().Error as err:
			logging.error(format(err))
			return format(err)



#To see in practice how it reacts. The output is the default http 200 for success or any other for error
@app.route('/vote',methods=['GET','POST'])
@login_required
@admin_permission.require()
def vote():
	logging.info('vote')
	conn = mysql.connect()
	cursor = conn.cursor()
	form = vote_form()
	print(form.data.items())
	logging.info('The form was: ' + str(form.data.items()))
	if request.method == 'POST':
		if form.validate() == False:
			print('entered')
			flash('All fields are required.')
			print(form.errors)
			flash(form.errors)
			return render_template('vote.html', form = form)
		else:
			try:
				print('entered try')
				cursor.execute('''INSERT into votes (vote_id, user_id,vote,event_id) values (%s,%s,%s,%s)''',(form.vote_id.data,form.user_id.data,form.vote.data,form.event_id.data))
				conn.commit()
				conn.close()
				print(cursor._last_executed)
				return 'Registered'
			except conn.Error as e:
				conn.close()
				return str(e)
	elif request.method == 'GET':
		return render_template('vote.html', form = form)
		
		

@app.route('/getVotesForEventId/<event_id>')
def get_votes_for_event(event_id):
	logging.info('getVotesForEventId')
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute('''SELECT vote_id,user_id,vote,event_id from votes where event_id=%s''' , event_id)
		rv = cursor.fetchall()
		logging.info('THE QUERY WAS SUCCESFULL: '+ cursor._last_executed)
		logging.info(rv)
		conn.close()
		return jsonify(rv)
	except mysql.connect().Error as err:
		logging.error(format(err))
		return format(err)


@app.route('/modifyItems', methods = ['GET', 'POST'])
@login_required
@admin_permission.require()
def modify_items():
	logging.info('/modifyItems')
	form = first_selection()
	logging.info('The form was: ' + str(form.data.items()))
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('modify_items_home.html', form = form)
		else:
			if form.Type.data=='match':
				if form.Action.data == 'add':
					return redirect(url_for('add_new_match'))
				else:
					return redirect(url_for('update_current_match'))
			elif form.Type.data == 'event':
				if form.Action.data == 'add':
					return redirect(url_for('add_new_event'))
				else:
					return redirect(url_for('update_current_event'))
			else:
				if form.Action.data == 'add':
					return redirect(url_for('add_new_media'))
				else:
					return redirect(url_for('update_current_media'))
	elif request.method == 'GET':
		return render_template('modify_items_home.html', form = form) 


@app.route('/addNewMatch', methods = ['GET', 'POST'])
@login_required
@admin_permission.require()
def add_new_match():
	logging.info('/addNewMatch')
	form = add_match()
	logging.info('The form was: ' + str(form.data.items()))
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			flash(form.errors)
			return render_template('add_new_match.html', form = form)
		else:
			
			return(add_match_fn(form,mysql))
	elif request.method == 'GET':
		return render_template('add_new_match.html', form = form) 



@app.route('/updateMatch', methods = ['GET', 'POST'])
@login_required
@admin_permission.require()
def update_current_match():
	logging.info('/updateMatch')
	form = update_match()
	logging.info('The form was: ' + str(form.data.items()))
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')

			flash(form.errors)
			return render_template('update_match.html', form = form)
		else:

			return(update_match_fn(form,mysql))
	elif request.method == 'GET':
		return render_template('update_match.html', form = form) 


@app.route('/addNewEvent', methods = ['GET', 'POST'])
@login_required
@admin_permission.require()
def add_new_event():
	logging.info('/addNewEvent')
	form = add_event()
	logging.info('The form was: ' + str(form.data.items()))
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			flash(form.errors)
			return render_template('add_new_event.html', form = form)
		else:
			
			return(add_event_fn(form,mysql))
	elif request.method == 'GET':
		return render_template('add_new_event.html', form = form) 


@app.route('/updateEvent', methods = ['GET', 'POST'])
@login_required
@admin_permission.require()
def update_current_event():
	logging.info('/updateEvent')
	form = update_event()
	logging.info('The form was: ' + str(form.data.items()))
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			flash(form.errors)
			return render_template('update_event.html', form = form)
		else:
			
			return(update_event_fn(form,mysql))
	elif request.method == 'GET':
		return render_template('update_event.html', form = form) 


@app.route('/addNewMedia', methods = ['GET', 'POST'])
@login_required
@admin_permission.require()
def add_new_media():
	logging.info('/addNewMedia')
	form = add_media()
	logging.info('The form was: ' + str(form.data.items()))
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			flash(form.errors)
			return render_template('add_new_media.html', form = form)
		else:
			
			return(add_media_fn(form,mysql))
	elif request.method == 'GET':
		return render_template('add_new_media.html', form = form) 


@app.route('/updateMedia', methods = ['GET', 'POST'])
@login_required
@admin_permission.require()
def update_current_media():
	logging.info('/updateMedia')
	form = update_media()
	logging.info('The form was: ' + str(form.data.items()))
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			flash(form.errors)
			return render_template('update_media.html', form = form)
		else:
			
			return(update_media_fn(form,mysql))
	elif request.method == 'GET':
		return render_template('update_media.html', form = form) 


