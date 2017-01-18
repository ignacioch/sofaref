CREATE TABLE user (
	user_id int,
	username varchar(100),
	primary key (user_id)
);

CREATE TABLE matches (
	match_id int,
	match_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	team_a varchar(50),
	team_b varchar(50),
	competition varchar(100),
	match_status tinyint,
	primary key (match_id)
);

CREATE TABLE events (
	event_id int,
	match_id int,
	description varchar(255),
	question_text varchar(255),
	primary key (event_id),
	foreign key (match_id) REFERENCES matches(match_id)
);


CREATE TABLE votes (
	vote_id int,
	user_id int,
	vote bool,
	event_id int,
	primary key (user_id,event_id),
	foreign key (user_id) REFERENCES user(user_id),
	foreign key (event_id) REFERENCES events(event_id)
);

CREATE TABLE media (
	media_id int,
	event_id int,
	media_type tinyint,
	media_url varchar(255),
	primary key (media_id),
	foreign key (event_id) REFERENCES events(event_id)
);
