insert into user(user_id,username)
values ('0','Vaik');
insert into user(user_id,username)
values ('1','Nacho');


insert into matches (match_id,match_datetime,team_a,team_b,competition,match_status)
values ('1567',NOW(), 'Arsenal','Hull','BPL','0');
insert into matches (match_id,match_datetime,team_a,team_b,competition,match_status)
values ('1478',NOW(), 'Liverpool','Man Utd','BPL','1');

insert into events (event_id,match_id,description,question_text)
values ('15','1567','Penalty', 'Was it a correct decision?');
insert into events (event_id,match_id,description,question_text)
values ('11','1478','Red Card', 'Was it a false decision?');

insert into votes(vote_id, user_id,vote,event_id)
values ('23','1','0','11');
insert into votes(vote_id, user_id,vote,event_id)
values ('27','0','1','15');

insert into media(media_id,event_id,media_type,media_url)
values('678','15','1','www.smth.com/photo.img');
insert into media(media_id,event_id,media_type,media_url)
values('134','11','0',null);