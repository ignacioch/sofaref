CREATE TABLE role (
role_id int,
role_name varchar(100),
description varchar(100),
primary key (role_id)
);

CREATE TABLE roles_users (
user_id int,
role_id int,
primary key (user_id)
);



CREATE TABLE user (
user_id int,
email varchar(100),
username varchar(100),
password varchar(100),
role_id int,
active boolean,
primary key (user_id),
foreign key (role_id) REFERENCES role(role_id),
UNIQUE (email)
);

CREATE TABLE matches (
match_id int(100),
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