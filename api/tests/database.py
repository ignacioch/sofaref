from flaskext.mysql import MySQL
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "C:\\Users\\Vaios\\Desktop\\Dev\\sofaref\\api")
sys.path.append(topdir)
from app import app
import random
import string
#General config
mysql = MySQL()

# MySQL configurations  
app.config.from_object('config.TestingConfig')
mysql.init_app(app)




def create_tables():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute('''CREATE TABLE role (
						    role_id INT,
						    role_name VARCHAR(100),
						    description VARCHAR(100),
						    PRIMARY KEY (role_id)
						);

						CREATE TABLE roles_users (
						    user_id INT,
						    role_id INT,
						    PRIMARY KEY (user_id)
						);

						CREATE TABLE user (
						    user_id INT,
						    email VARCHAR(100),
						    username VARCHAR(100),
						    password VARCHAR(100),
						    role_id INT,
						    active BOOLEAN,
						    PRIMARY KEY (user_id),
						    FOREIGN KEY (role_id)
						        REFERENCES role (role_id),
						    UNIQUE (email)
						);

						CREATE TABLE matches (
						    match_id INT(100),
						    match_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
						    team_a VARCHAR(50),
						    team_b VARCHAR(50),
						    competition VARCHAR(100),
						    match_status TINYINT,
						    PRIMARY KEY (match_id)
						);

						CREATE TABLE events (
						    event_id INT,
						    match_id INT,
						    description VARCHAR(255),
						    question_text VARCHAR(255),
						    PRIMARY KEY (event_id),
						    FOREIGN KEY (match_id)
						        REFERENCES matches (match_id)
						);


						CREATE TABLE votes (
						    vote_id INT,
						    user_id INT,
						    vote BOOL,
						    event_id INT,
						    PRIMARY KEY (user_id , event_id),
						    FOREIGN KEY (user_id)
						        REFERENCES user (user_id),
						    FOREIGN KEY (event_id)
						        REFERENCES events (event_id)
						);

						CREATE TABLE media (
						    media_id INT,
						    event_id INT,
						    media_type TINYINT,
						    media_url VARCHAR(255),
						    PRIMARY KEY (media_id),
						    FOREIGN KEY (event_id)
						        REFERENCES events (event_id)
						);''')
		conn.commit()
		conn.close()
	except conn.Error as e:
		conn.close()
	
def drop_tables():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute('''DROP TABLE votes;
						DROP TABLE media;
						DROP TABLE events;
						DROP TABLE matches;
						DROP TABLE user;
						DROP TABLE role;
						DROP TABLE roles_users;''')
		conn.commit()
		conn.close()
	except conn.Error as e:
		conn.close()

def add_match(mid,status):
    try:        
        conn = mysql.connect()
        cursor = conn.cursor()
        query = ('''insert into matches (match_id,match_datetime,team_a,team_b,competition,match_status)
            values (%s,'2017-01-21 10:10:10', 'Arsenal','Hull','BPL',%s);''')
        cursor.execute(query,(mid,status))
        conn.commit()
        cursor.close()
        #print(cursor._last_executed)
        conn.close()
    except conn.Error as err:
        print(err)


def add_event(eid,mid):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ("INSERT into events (event_id,match_id,description,question_text) values (%s, %s,'Sample description', 'Sample question') ")
		cursor.execute(query,(eid,mid))
		conn.commit()
		cursor.close()
		conn.close()
	except conn.Error as err:
		print(err)

def add_media(meid,eid):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ("INSERT into media (media_id,event_id,media_type,media_url) values (%s, %s,0, 'Sample url') ")
		cursor.execute(query,(meid,eid))
		conn.commit()
		cursor.close()
		conn.close()
	except conn.Error as err:
		print(err)




def update(mid, type_select):
	
	if type_select == 'matches':
		fields = ('match_datetime','team_a', 'team_b', 'competition', 'match_status')
		values = ('2018-01-21 10:10:10', 'Changed team a', 'Changed team b', 'Changed competition',1)
		select = random.randint(0,4)
		prim_key = 'match_id'
	elif type_select == 'events':
		fields = ('match_id','description','question_text')
		values = (1,'Changed description', 'Changed question')
		select = random.randint(0,2)
		prim_key = 'event_id'
	elif type_select == 'media':
		fields = ('event_id','media_type', 'media_url')
		values = (1, 1, 'Changed url')
		select = random.randint(0,2)
		prim_key = 'media_id'
	for i in range(len(fields)):

		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			sql = 'UPDATE '+type_select+' SET '+fields[i]+' = %s WHERE '+prim_key+' = %s '
			cursor.execute(sql,(values[i],mid))
			conn.commit()
			cursor.close()
			conn.close()
		except conn.Error as err:
			print(err)


def vote(vid, uid, eid):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ('''INSERT into votes (vote_id, user_id,vote,event_id) values (%s,%s,1,%s)''')
		cursor.execute(query,(vid,uid,eid))
		conn.commit()
		cursor.close()
		conn.close()
	except conn.Error as err:
		print(err)

def add_user(uid):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()

		query = ('''insert into user(user_id,email,username,password,role_id,active)
					values (%s,%s,'user','password','0',1);''')
		cursor.execute(query,(uid,random.choice(string.ascii_letters)))
		conn.commit()
		query = ('''insert into roles_users(user_id, role_id) values (%s,0);''')
		cursor.execute(query,uid)
		conn.commit()
		cursor.close()
		conn.close()
	except conn.Error as err:
		print(err)

def create_role():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ('''insert into role (role_id,role_name,description)
				values ('0','admin','This is the admin');''')
		cursor.execute(query)
		conn.commit()
		cursor.close()
		conn.close()
	except conn.Error as err:
		print(err)


