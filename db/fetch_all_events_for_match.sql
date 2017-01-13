select event_id,match_id,description,question_text from events where match_id='1';

SELECT matches.match_id, matches.match_datetime, matches.team_a, matches.team_b, matches.competition, matches.match_status, events.event_id,events.description, events.question_text
FROM matches
INNER JOIN events
ON matches.match_id=events.match_id 
WHERE matches.match_id = '1';
